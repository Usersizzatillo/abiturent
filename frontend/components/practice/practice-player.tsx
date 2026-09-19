"use client";

import { useEffect, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { useAuth } from "@/components/providers/auth-provider";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { ProtectedShell } from "@/components/layout/protected-shell";
import { fetchSubject } from "@/lib/catalog";
import {
  fetchCurrent,
  finishSession,
  startPractice,
  submitAnswer,
  type AnswerResult,
  type SessionOption,
  type SessionQuestion,
} from "@/lib/sessions";
import { cn } from "@/lib/utils";

type LocalizedText = {
  text_uz?: string;
  text_ru?: string;
  text_en?: string;
  explanation_uz?: string;
  explanation_ru?: string;
  explanation_en?: string;
};

function localText(item: LocalizedText, locale: string): string {
  if (locale === "ru") return item.text_ru ?? item.explanation_ru ?? "";
  if (locale === "en") return item.text_en ?? item.explanation_en ?? "";
  return item.text_uz ?? item.explanation_uz ?? "";
}

function shuffleOptions(options: SessionOption[]): SessionOption[] {
  return [...options]
    .map((o) => ({ o, r: Math.random() }))
    .sort((a, b) => a.r - b.r)
    .map((x) => x.o);
}

function optionLabel(n: number): string {
  return String.fromCharCode(65 + n);
}

function CheckIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M20 6 9 17l-5-5" />
    </svg>
  );
}

function CrossIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M18 6 6 18M6 6l12 12" />
    </svg>
  );
}

function Flame({ size = 15 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" aria-hidden>
      <path d="M15.5 11c0-1.5-.7-2.7-1.6-4 .3 1.6-.4 3-1.9 4-1.4 1-2.5 2.3-2.5 4.1A4 4 0 0 0 13.6 19c2.6 0 4.4-2 4.4-4.4 0-1.6-.7-2.8-2.5-3.6zM12 3a2 2 0 1 0-4 0 2 2 0 0 0 4 0z" />
    </svg>
  );
}

export function PracticePlayer({ slug }: { slug: string }) {
  const t = useTranslations("common");
  const exam = useTranslations("exam");
  const res = useTranslations("results");
  const locale = useLocale();
  const { user } = useAuth();

  const [sessionId, setSessionId] = useState<number | null>(null);
  const [question, setQuestion] = useState<SessionQuestion | null>(null);
  const [shuffled, setShuffled] = useState<SessionOption[]>([]);
  const [selected, setSelected] = useState<number | null>(null);
  const [result, setResult] = useState<AnswerResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState({ answered: 0, total: 0 });
  const [score, setScore] = useState<number | null>(null);
  const [correctTotal, setCorrectTotal] = useState(0);
  const [streak, setStreak] = useState(0);
  const [time, setTime] = useState({ correct: 0, wrong: 0 });

  const subjectLink = `/subjects/${slug}`;

  useEffect(() => {
    if (!user) return;
    let ignore = false;
    fetchSubject(slug)
      .then((subject) =>
        startPractice({ subject: subject.id, question_count: 10, mode: "practice" })
      )
      .then((sess) => {
        if (ignore) return;
        setSessionId(sess.id);
        setProgress({ answered: 0, total: sess.question_count });
        if (sess.current_question) {
          setQuestion(sess.current_question);
          setShuffled(shuffleOptions(sess.current_question.options));
        }
      })
      .catch(() => {
        if (!ignore) setError(t("error"));
      })
      .finally(() => {
        if (!ignore) setLoading(false);
      });
    return () => {
      ignore = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, slug]);

  const answer = () => {
    if (!sessionId || !question || selected === null) return;
    submitAnswer(sessionId, question.id, selected)
      .then((r) => {
        setResult(r);
        setProgress((p) => ({ ...p, answered: p.answered + 1 }));
        setCorrectTotal((c) => c + (r.is_correct ? 1 : 0));
        setStreak((s) => (r.is_correct ? s + 1 : 0));
        setTime((x) => (r.is_correct ? { ...x, correct: x.correct + 1 } : { ...x, wrong: x.wrong + 1 }));
      })
      .catch(() => setError(t("error")));
  };

  const next = () => {
    if (!sessionId) return;
    setSelected(null);
    setResult(null);
    setQuestion(null);
    setLoading(true);
    fetchCurrent(sessionId)
      .then((resQ) => {
        if (resQ.question) {
          setQuestion(resQ.question);
          setShuffled(shuffleOptions(resQ.question.options));
        } else {
          return finishSession(sessionId).then((rep) => {
            setScore(rep.score_percent);
            setCorrectTotal(rep.correct_answers);
            setProgress({ answered: rep.question_count, total: rep.question_count });
          });
        }
      })
      .catch(() => setError(t("error")))
      .finally(() => setLoading(false));
  };

  // Keyboard shortcuts: A-D/1-4 select, Enter submits / advances
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (score !== null) return;
      if (result) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          next();
        }
        return;
      }
      const k = e.key.toUpperCase();
      const idx = ["A", "B", "C", "D", "E", "F"].indexOf(k);
      if (idx >= 0 && idx < shuffled.length) {
        e.preventDefault();
        setSelected(shuffled[idx].id);
        return;
      }
      if (e.key === "Enter" && selected !== null) {
        e.preventDefault();
        answer();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [shuffled, selected, result, score]);

  const optionState = (opt: SessionOption) => {
    if (!result) return "idle";
    if (opt.id === result.correct_option_id) return "correct";
    if (opt.id === selected) return "wrong";
    return "idle";
  };

  return (
    <ProtectedShell>
      <div className="mx-auto w-full max-w-3xl flex-1 px-4 py-8 sm:px-6">
        {/* Topbar */}
        <div className="mb-5 flex items-center justify-between gap-3">
          <Link href={subjectLink} className="btn btn-ghost btn-sm">
            ← {t("back")}
          </Link>
          <div className="flex items-center gap-3">
            {streak >= 2 ? (
              <span className="badge badge-warning gap-1 px-2.5 py-1">
                <Flame />
                {streak}
              </span>
            ) : null}
            <span className="text-sm font-semibold tabular-nums text-muted">
              {progress.answered} / {progress.total}
            </span>
          </div>
        </div>

        {/* Segment progress */}
        <div className="mb-6 flex h-2 w-full gap-1 overflow-hidden">
          {Array.from({ length: progress.total }).map((_, i) => (
            <span
              key={i}
              className={cn(
                "h-full flex-1 rounded-full transition-colors duration-300",
                i < progress.answered ? "bg-primary" : "bg-surface-subtle"
              )}
            />
          ))}
        </div>

        {error ? (
          <div className="card flex flex-col items-center gap-4 p-10 text-center">
            <p className="text-muted">{error}</p>
            <Link href={subjectLink} className="btn btn-secondary btn-sm">
              {t("back")}
            </Link>
          </div>
        ) : loading ? (
          <div className="flex flex-col gap-4">
            <Skeleton className="h-24" />
            {[0, 1, 2, 3].map((i) => (
              <Skeleton key={i} className="h-14" />
            ))}
          </div>
        ) : score !== null ? (
          /* Finish — score ring + summary (Quizzler-style) */
          <Card className="pop flex flex-col items-center gap-6 p-10 text-center">
            <div className="relative h-36 w-36" style={{ "--p": score } as React.CSSProperties}>
              <div className="score-ring absolute inset-0" />
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-4xl font-bold tabular-nums">{score}%</span>
                <span className="text-xs font-medium text-muted">{exam("resultsSummary")}</span>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="flex items-center gap-2 rounded-xl bg-success-soft px-4 py-2.5">
                <CheckIcon />
                <span className="text-sm font-semibold text-success">
                  {time.correct || correctTotal} {res("correct").toLowerCase()}
                </span>
              </div>
              <div className="flex items-center gap-2 rounded-xl bg-danger-soft px-4 py-2.5">
                <CrossIcon />
                <span className="text-sm font-semibold text-danger">
                  {time.wrong} {res("incorrect").toLowerCase()}
                </span>
              </div>
            </div>
            <div className="flex w-full max-w-sm flex-col gap-3 sm:flex-row">
              <Link href={`/subjects/${slug}/practice`} className="btn btn-secondary btn-lg flex-1">
                {t("again")}
              </Link>
              <Link href={subjectLink} className="btn btn-primary btn-lg flex-1">
                {t("back")}
              </Link>
            </div>
          </Card>
        ) : question ? (
          <div className="flex flex-col gap-4">
            <Card className="p-6">
              <p className="text-lg font-medium leading-relaxed">{localText(question, locale)}</p>
            </Card>

            <div className="flex flex-col gap-2.5">
              {shuffled.map((opt, i) => {
                const state = optionState(opt);
                const isSelected = state === "idle" && selected === opt.id;
                return (
                  <button
                    key={opt.id}
                    type="button"
                    disabled={!!result}
                    onClick={() => setSelected(opt.id)}
                    className={cn(
                      "group flex items-center gap-3 rounded-xl border px-3.5 py-3 text-left transition-all sm:px-4",
                      state === "idle" &&
                        isSelected &&
                        "border-primary bg-primary-soft shadow-popover",
                      state === "idle" &&
                        !isSelected &&
                        "border-border bg-surface hover:-translate-y-0.5 hover:border-border-strong hover:shadow-raised",
                      state === "correct" && "pop border-success bg-success-soft",
                      state === "wrong" && "pop border-danger bg-danger-soft",
                      "disabled:cursor-default disabled:opacity-100"
                    )}
                  >
                    <span
                      className={cn(
                        "option-key",
                        state === "correct" && "bg-success text-white",
                        state === "wrong" && "bg-danger text-white",
                        state === "idle" && isSelected && "bg-primary text-white",
                        state === "idle" && !isSelected && "bg-surface-subtle text-muted group-hover:bg-primary-muted"
                      )}
                    >
                      {optionLabel(i)}
                    </span>
                    <span className="flex-1 text-sm font-medium">{localText(opt, locale)}</span>
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
              })}
            </div>

            <div className="mt-2 flex items-center justify-between text-xs text-subtle">
              <span>{t("keyboardHints")}</span>
              {selected !== null && !result ? <span className="text-primary">{t("pressEnter")}</span> : null}
            </div>

            {result ? (
              <Card
                className={cn(
                  "pop flex flex-col gap-2 p-5",
                  result.is_correct ? "border-success" : "border-danger"
                )}
              >
                <p
                  className={cn(
                    "flex items-center gap-2 text-lg font-bold",
                    result.is_correct ? "text-success" : "text-danger"
                  )}
                >
                  {result.is_correct ? <CheckIcon /> : <CrossIcon />}
                  {result.is_correct ? exam("correctAnswer") : exam("wrongAnswer")}
                </p>
                {localText(result, locale) ? (
                  <p className="text-sm leading-relaxed text-muted">
                    <span className="font-semibold">{exam("explanation")}: </span>
                    {localText(result, locale)}
                  </p>
                ) : null}
              </Card>
            ) : null}

            {!result ? (
              <Button onClick={answer} disabled={selected === null} className="mt-1">
                {exam("submitAnswer")}
                {selected !== null ? <span className="opacity-70">↵</span> : null}
              </Button>
            ) : (
              <Button variant={result.is_correct ? "primary" : "secondary"} onClick={next} className="mt-1">
                {progress.answered >= progress.total ? exam("finish") : t("next")}
                <span className="opacity-70">↵</span>
              </Button>
            )}
          </div>
        ) : (
          <div className="card flex flex-col items-center gap-4 p-10 text-center">
            <p className="text-muted">{t("empty")}</p>
            <Link href={subjectLink} className="btn btn-secondary btn-sm">
              {t("back")}
            </Link>
          </div>
        )}
      </div>
    </ProtectedShell>
  );
}