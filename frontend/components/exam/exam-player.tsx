"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { startPractice, fetchSessionQuestions, submitAnswer, finishSession, type SessionQuestion, type SessionReport, type SessionOption } from "@/lib/sessions";
import { localizedName, type Subject } from "@/lib/catalog";
import { cn } from "@/lib/utils";

function CheckIcon({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M20 6 9 17l-5-5" />
    </svg>
  );
}

function CrossIcon({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M18 6 6 18M6 6l12 12" />
    </svg>
  );
}

function ClockIcon({ size = 14 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <circle cx="12" cy="12" r="10" />
      <path d="M12 6v6l4 2" />
    </svg>
  );
}

interface ExamSetupProps {
  subjects: Subject[];
  onStart: (subject: Subject, questionCount: number, minutes: number) => void;
  onHistory: () => void;
}

export function ExamSetup({ subjects, onStart, onHistory }: ExamSetupProps) {
  const t = useTranslations("exam");
  const common = useTranslations("common");
  const locale = useLocale();

  const [subject, setSubject] = useState<Subject | null>(null);
  const [count, setCount] = useState(10);
  const [minutes, setMinutes] = useState(10);

  return (
    <div className="mx-auto flex w-full max-w-2xl flex-1 flex-col gap-6 px-4 py-10 sm:px-6">
      <div className="flex flex-col items-center gap-2 text-center">
        <span className="badge badge-primary">DTM</span>
        <h1 className="text-3xl font-bold tracking-tight">{t("title")}</h1>
        <p className="text-muted">{t("chooseSubject")}</p>
      </div>

      <div className="grid gap-3 sm:grid-cols-2">
        {subjects.map((s) => (
          <button
            key={s.id}
            type="button"
            onClick={() => setSubject(s)}
            className={cn(
              "card card-hover flex items-center gap-3 p-4 text-left",
              subject?.id === s.id && "border-primary/50 bg-primary-soft"
            )}
          >
            <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-primary-hover text-sm font-bold text-primary-foreground">
              {(s.code || localizedName(s, locale).charAt(0)).toUpperCase()}
            </span>
            <span className="font-semibold">{localizedName(s, locale)}</span>
            {subject?.id === s.id ? (
              <span className="ml-auto text-primary">
                <CheckIcon />
              </span>
            ) : null}
          </button>
        ))}
      </div>

      <div className="card flex flex-col gap-5 p-6">
        <div className="flex flex-col gap-2">
          <span className="text-sm font-semibold text-subtle">{t("questionCount")}</span>
          <div className="grid grid-cols-3 gap-3">
            {[5, 10, 15].map((n) => (
              <button
                key={n}
                type="button"
                onClick={() => {
                  setCount(n);
                  setMinutes(n);
                }}
                className={cn(
                  "segment-option",
                  count === n && "segment-option-active"
                )}
              >
                {n}
              </button>
            ))}
          </div>
        </div>
        <div className="flex flex-col gap-2">
          <span className="text-sm font-semibold text-subtle">{t("timeLimitMin")}</span>
          <div className="grid grid-cols-3 gap-3">
            {[5, 10, 15].map((m) => (
              <button
                key={m}
                type="button"
                onClick={() => setMinutes(m)}
                className={cn(
                  "segment-option",
                  minutes === m && "segment-option-active"
                )}
              >
                {m} {common("minUnit")}
              </button>
            ))}
          </div>
        </div>

        <button
          type="button"
          disabled={!subject}
          className="btn btn-primary btn-lg w-full"
          onClick={() => subject && onStart(subject, count, minutes)}
        >
          {t("startExam")}
        </button>

        <button
          type="button"
          className="text-sm font-medium text-subtle underline-offset-4 hover:text-primary hover:underline"
          onClick={onHistory}
        >
          {t("history")}
        </button>
      </div>
    </div>
  );
}

function OptionRow({
  option,
  state,
  selected,
  onSelect,
}: {
  option: SessionOption;
  state: "default" | "correct" | "wrong";
  selected: boolean;
  onSelect: () => void;
}) {
  const locale = useLocale();
  const isRevealed = state !== "default";
  const text =
    locale === "ru"
      ? option.text_ru || option.text_uz
      : locale === "en"
        ? option.text_en || option.text_uz
        : option.text_uz;
  return (
    <button
      type="button"
      onClick={onSelect}
      disabled={isRevealed && !selected}
      className={cn(
        "option-card",
        selected && !isRevealed && "option-card-selected",
        state === "correct" && "option-card-correct",
        state === "wrong" && "option-card-wrong"
      )}
    >
      <span
        className={cn(
          "option-key",
          state === "correct" && "bg-success text-white",
          state === "wrong" && "bg-danger text-white",
          selected && !isRevealed && "bg-primary text-white",
          !selected && !isRevealed && "bg-surface-subtle text-muted"
        )}
      >
        {option.sort_order + 1}
      </span>
      <span className="flex-1 text-left text-sm font-medium">{text}</span>
      {state === "correct" ? (
        <span className="flex h-6 w-6 items-center justify-center rounded-full bg-success text-white">
          <CheckIcon />
        </span>
      ) : state === "wrong" ? (
        <span className="flex h-6 w-6 items-center justify-center rounded-full bg-danger text-white">
          <CrossIcon />
        </span>
      ) : null}
    </button>
  );
}

function TimerBadge({ remaining }: { remaining: number }) {
  const t = useTranslations("exam");
  const mm = String(Math.floor(remaining / 60)).padStart(2, "0");
  const ss = String(remaining % 60).padStart(2, "0");
  const danger = remaining <= 60;
  return (
    <span className={cn("badge", danger ? "badge-danger" : "badge-primary")}>
      <ClockIcon />
      {t("timeRemaining")}: {mm}:{ss}
    </span>
  );
}

export function ExamPlayer({
  subject,
  questionCount,
  minutes,
  onExit,
}: {
  subject: Subject;
  questionCount: number;
  minutes: number;
  onExit: () => void;
}) {
  const t = useTranslations("exam");
  const common = useTranslations("common");
  const locale = useLocale();

  const [deadline] = useState(() => Date.now() + minutes * 60 * 1000);
  const [remaining, setRemaining] = useState(minutes * 60);

  const [questions, setQuestions] = useState<SessionQuestion[]>([]);
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [selected, setSelected] = useState<Record<number, number>>({});
  const [index, setIndex] = useState(0);
  const [finished, setFinished] = useState(false);
  const [report, setReport] = useState<SessionReport | null>(null);
  const [pending, setPending] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sessionId = useRef<number | null>(null);
  const timedOut = useRef(false);

  const finish = useCallback(async () => {
    if (finished || !sessionId.current || timedOut.current) return;
    timedOut.current = true;
    setSubmitting(true);
    try {
      const rep = await finishSession(sessionId.current);
      setReport(rep);
      setFinished(true);
    } catch {
      setError(common("error"));
    } finally {
      setSubmitting(false);
    }
  }, [finished, common]);

  useEffect(() => {
    let ignore = false;
    (async () => {
      try {
        const session = await startPractice({
          subject: subject.id,
          question_count: questionCount,
          mode: "exam",
        });
        sessionId.current = session.id;
        const qs = await fetchSessionQuestions(session.id);
        if (!ignore) {
          setQuestions(qs);
          setPending(false);
        }
      } catch {
        if (!ignore) {
          setError(common("error"));
          setPending(false);
        }
      }
    })();
    return () => {
      ignore = true;
    };
  }, [subject.id, questionCount, common]);

  useEffect(() => {
    const interval = setInterval(() => {
      const left = Math.max(0, Math.round((deadline - Date.now()) / 1000));
      setRemaining(left);
      if (left === 0) finish();
    }, 1000);
    return () => clearInterval(interval);
  }, [finish, deadline]);

  const question = questions[index];

  const submitCurrent = async () => {
    const optId = selected[question.id];
    if (optId == null || !sessionId.current || submitting) return;
    setSubmitting(true);
    try {
      await submitAnswer(sessionId.current, question.id, optId);
      setAnswers((prev) => ({ ...prev, [question.id]: optId }));
      if (!(index + 1 < questions.length)) {
        finish();
      } else {
        setIndex((i) => i + 1);
        setSubmitting(false);
      }
    } catch {
      setError(common("error"));
      setSubmitting(false);
    }
  };

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (finished) return;
      if (question && e.key >= "1" && e.key <= "9") {
        const idx = Number(e.key) - 1;
        const opt = question.options[idx];
        if (opt) setSelected((prev) => ({ ...prev, [question.id]: opt.id }));
      } else if (e.key === "Enter" && question) {
        e.preventDefault();
        submitCurrent();
      } else if (e.key >= "a" && e.key <= "z") {
        const idx = e.key.charCodeAt(0) - 97;
        const opt = question?.options[idx];
        if (opt) setSelected((prev) => ({ ...prev, [question.id]: opt.id }));
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  });

  const answeredCount = Object.keys(answers).length;

  const questionLocal = (q: SessionQuestion) =>
    locale === "ru" ? q.text_ru || q.text_uz : locale === "en" ? q.text_en || q.text_uz : q.text_uz;

  if (finished) {
    return (
      <div className="mx-auto flex w-full max-w-2xl flex-1 flex-col gap-6 px-4 py-10 sm:px-6">
        <div className="card flex flex-col items-center gap-4 p-8 text-center">
          <div className="score-ring score-ring-lg">
            <span className="text-2xl font-bold">{report?.score_percent ?? 0}%</span>
          </div>
          <p className="text-lg font-semibold">{t("resultsSummary")}</p>
          <div className="flex items-center gap-3">
            <span className="badge badge-success">{report?.correct_answers ?? 0}</span>
            <span className="badge badge-danger">{report?.incorrect_answers ?? 0}</span>
            <span className="badge badge-neutral">{report?.unanswered ?? 0}</span>
          </div>
          <div className="flex gap-3">
            <button type="button" className="btn btn-secondary" onClick={onExit}>
              {t("history")}
            </button>
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => window.location.reload()}
            >
              {t("startExam")}
            </button>
          </div>
        </div>
        <ReportList report={report} />
      </div>
    );
  }

  if (pending) {
    return (
      <div className="mx-auto flex w-full max-w-2xl flex-1 flex-col items-center justify-center gap-4 px-4">
        <span className="text-muted">{common("loading")}</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mx-auto flex w-full max-w-2xl flex-1 flex-col items-center gap-4 px-4">
        <span className="text-danger">{error}</span>
        <button type="button" className="btn btn-secondary btn-sm" onClick={onExit}>
          {common("back")}
        </button>
      </div>
    );
  }

  if (!question) {
    return (
      <div className="mx-auto flex w-full max-w-2xl flex-1 flex-col items-center gap-4 px-4">
        <span className="text-muted">{t("notStarted")}</span>
      </div>
    );
  }

  return (
    <div className="mx-auto flex w-full max-w-2xl flex-1 flex-col gap-5 px-4 py-8 sm:px-6">
      <div className="flex items-center justify-between gap-3">
        <button type="button" className="btn btn-secondary btn-sm" onClick={onExit}>
          {common("cancel")}
        </button>
        <TimerBadge remaining={remaining} />
      </div>

      {/* progress segments */}
      <div className="flex gap-1.5">
        {questions.map((q, i) => (
          <button
            key={q.id}
            type="button"
            onClick={() => setIndex(i)}
            aria-label={`${t("question")} ${i + 1}`}
            className={cn(
              "h-2 flex-1 rounded-full transition-colors",
              answers[q.id] != null
                ? "bg-primary"
                : i === index
                  ? "bg-subtle"
                  : "bg-surface-subtle"
            )}
          />
        ))}
      </div>

      <div className="flex items-center justify-between">
        <span className="text-sm font-semibold text-subtle">
          {t("question")} {index + 1} {common("of")} {questions.length}
        </span>
        <span className="text-sm font-medium text-subtle">
          {answeredCount}/{questions.length} {t("answered")}
        </span>
      </div>

      <div className="card flex flex-col gap-4 p-6">
        <h2 className="text-lg font-semibold leading-relaxed">{questionLocal(question)}</h2>
        <div className="flex flex-col gap-2.5">
          {question.options.map((opt) => (
            <OptionRow
              key={opt.id}
              option={opt}
              selected={selected[question.id] === opt.id}
              state="default"
              onSelect={() =>
                setSelected((prev) => ({ ...prev, [question.id]: opt.id }))
              }
            />
          ))}
        </div>
        <button
          type="button"
          className={cn("btn btn-primary w-full", !selected[question.id] && "btn-disabled")}
          onClick={submitCurrent}
          disabled={submitting}
        >
          {index + 1 < questions.length ? common("next") : t("finish")}
        </button>
        <p className="text-center text-xs text-subtle">{common("keyboardHints")}</p>
      </div>
    </div>
  );
}

function ReportList({ report }: { report: SessionReport | null }) {
  const t = useTranslations("exam");
  const locale = useLocale();
  if (!report) return null;
  return (
    <div className="flex flex-col gap-4">
      <h3 className="text-xl font-bold tracking-tight">{t("review")}</h3>
      {report.questions.map((row) => {
        const questionText =
          locale === "ru"
            ? row.question.text_ru || row.question.text_uz
            : locale === "en"
              ? row.question.text_en || row.question.text_uz
              : row.question.text_uz;
        const chosen = row.question.options.find((o) => o.id === row.selected_option_id);
        const correct = row.question.options.find((o) => o.is_correct);
        const chosenText =
          locale === "ru"
            ? chosen?.text_ru || chosen?.text_uz
            : locale === "en"
              ? chosen?.text_en || chosen?.text_uz
              : chosen?.text_uz;
        const correctText =
          locale === "ru"
            ? correct?.text_ru || correct?.text_uz
            : locale === "en"
              ? correct?.text_en || correct?.text_uz
              : correct?.text_uz;
        const explanation =
          locale === "ru"
            ? row.question.explanation_ru || row.question.explanation_uz
            : locale === "en"
              ? row.question.explanation_en || row.question.explanation_uz
              : row.question.explanation_uz;
        return (
          <div key={row.question.id} className="card p-5">
            <div className="flex gap-3">
              <span
                className={cn(
                  "badge",
                  row.is_correct ? "badge-success" : "badge-danger"
                )}
              >
                {row.is_correct ? t("correctAnswer") : t("wrongAnswer")}
              </span>
            </div>
            <p className="mt-2 font-medium leading-relaxed">{questionText}</p>
            <div className="mt-3 flex flex-col gap-1.5 text-sm">
              <p className="text-subtle">
                {t("yourAnswer")}: <span className="font-semibold text-foreground">{chosenText ?? "—"}</span>
              </p>
              {!row.is_correct ? (
                <p className="text-subtle">
                  {t("correctAnswer")}: <span className="font-semibold text-success">{correctText}</span>
                </p>
              ) : null}
            </div>
            {explanation ? (
              <p className="mt-3 rounded-lg bg-surface-subtle p-3 text-sm text-muted">
                {t("explanation")}: {explanation}
              </p>
            ) : null}
          </div>
        );
      })}
    </div>
  );
}