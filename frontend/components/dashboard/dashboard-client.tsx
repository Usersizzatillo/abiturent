"use client";

import { useCallback, useEffect, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { useAuth } from "@/components/providers/auth-provider";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert } from "@/components/ui/alert";
import { Skeleton } from "@/components/ui/skeleton";
import { fetchStatsSummary, type StatsSummary } from "@/lib/stats";
import { cn } from "@/lib/utils";

function Flame({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" aria-hidden>
      <path d="M8.5 14.5A3.5 3.5 0 0 0 12 18c1.9 0 3.5-1.5 3.5-3.5 0-1.9-1.2-2.8-2.3-3.9C12.2 9.6 12 8.6 12 7.7c0-.6-.5-.9-.9-.6-2 1.8-2.6 3.6-2.6 5.4l.4 1.9-1-.4-.9-.9c-.3-.3-.8-.2-1 .2-.4 1.1-.5 2.6.5 3.2zM12 3a2 2 0 0 1 4 0 2 2 0 0 1-4 0z" />
      <path d="M15.5 11c0-1.5-.7-2.7-1.6-4 .3 1.6-.4 3-1.9 4-1.4 1-2.5 2.3-2.5 4.1A4 4 0 0 0 13.6 19c2.6 0 4.4-2 4.4-4.4 0-1.6-.7-2.8-2.5-3.6z" opacity="0.55" />
    </svg>
  );
}

function Icon({ name, size = 18, className }: { name: string; size?: number; className?: string }) {
  const paths: Record<string, React.ReactNode> = {
    book: <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V2H6.5A2.5 2.5 0 0 0 4 4.5v15A2.5 2.5 0 0 0 6.5 22H20V20H6.5A2.5 2.5 0 0 1 4 17.5z" />,
    target: <><circle cx="12" cy="12" r="10" /><circle cx="12" cy="12" r="6" /><circle cx="12" cy="12" r="2" /></>,
    chart: <><path d="M3 3v18h18" /><rect x="7" y="12" width="3" height="6" /><rect x="12" y="8" width="3" height="10" /><rect x="17" y="4" width="3" height="14" /></>,
    check: <path d="M20 6 9 17l-5-5" />,
    arrowRight: <path d="M5 12h14m-6-6 6 6-6 6" />,
  };
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden
      className={className}
    >
      {paths[name]}
    </svg>
  );
}

function scoreTone(pct: number) {
  if (pct >= 75) return { text: "text-success", bg: "bg-success-soft text-success", bar: "bg-success" };
  if (pct >= 50) return { text: "text-warning", bg: "bg-warning-soft text-warning", bar: "bg-warning" };
  return { text: "text-danger", bg: "bg-danger-soft text-danger", bar: "bg-danger" };
}

const WEEKDAYS = new Intl.DateTimeFormat("en-US", { weekday: "narrow" });

export function DashboardClient() {
  const t = useTranslations("dashboard");
  const res = useTranslations("results");
  const exam = useTranslations("exam");
  const locale = useLocale();
  const { user, loading: authLoading } = useAuth();

  const [stats, setStats] = useState<StatsSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const load = useCallback(() => {
    if (!user) return;
    fetchStatsSummary()
      .then(setStats)
      .catch(() => setError(t("error")))
      .finally(() => setLoading(false));
  }, [user, t]);

  useEffect(() => {
    if (user) load();
  }, [load, user]);

  const dateFmt = new Intl.DateTimeFormat(locale, { day: "2-digit", month: "short" });
  const maxDay = stats ? Math.max(1, ...stats.weekly_activity.map((d) => d.answered)) : 1;
  const subjRows = stats?.subject_breakdown.slice(0, 4) ?? [];

  return (
    <div className="page-enter flex flex-col gap-6">
      {/* Greeting + streak */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-2xl font-bold tracking-tight">
          {t("greeting")}, {user?.first_name || user?.username}
        </h2>
        <span
          className={cn(
            "badge gap-1.5 px-3 py-1.5",
            (stats?.streak ?? 0) > 0 ? "badge-warning" : "badge-neutral"
          )}
        >
          <Flame size={15} />
          {(stats?.streak ?? 0) > 0 ? stats!.streak : 0} {t("streak").toLowerCase()}
        </span>
      </div>

      {/* Quick actions */}
      <div className="flex flex-wrap gap-3">
        <Link href="/subjects" className="btn btn-primary">
          {t("startPractice")}
        </Link>
        <Link href="/mock-exams" className="btn btn-secondary">
          {t("takeMockExam")}
        </Link>
        <Link href="/profile" className="btn btn-ghost">
          {t("viewProfile")}
        </Link>
      </div>

      {loading || (authLoading && !stats) ? (
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {[0, 1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-32" />
          ))}
        </div>
      ) : error ? (
        <Alert variant="danger" className="flex items-center justify-between">
          <span>{error}</span>
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={() => {
              setError(null);
              setLoading(true);
              load();
            }}
          >
            {t("retry")}
          </button>
        </Alert>
      ) : stats ? (
        <>
          {/* Metric cards */}
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle className="text-sm font-medium text-muted">{t("overallProgress")}</CardTitle>
                <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary-soft text-primary">
                  <Icon name="target" size={16} />
                </span>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold tabular-nums">{stats.accuracy}%</p>
                <div className="mt-3 h-1.5 w-full overflow-hidden rounded-full bg-surface-subtle">
                  <div
                    className="h-full rounded-full bg-primary transition-all"
                    style={{ width: `${stats.accuracy}%` }}
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle className="text-sm font-medium text-muted">{t("completedTests")}</CardTitle>
                <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-success-soft text-success">
                  <Icon name="check" size={16} />
                </span>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold tabular-nums">{stats.total_finished}</p>
                <p className="mt-1 text-sm text-muted">{res("correct")} {stats.total_questions}</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle className="text-sm font-medium text-muted">{t("currentScore")}</CardTitle>
                <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-info-soft text-info">
                  <Icon name="chart" size={16} />
                </span>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold tabular-nums">{stats.current_score}%</p>
                <p className="mt-1 text-sm text-muted">{stats.total_answered} {t("answered").toLowerCase()}</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle className="text-sm font-medium text-muted">{t("streak")}</CardTitle>
                <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-warning-soft text-warning">
                  <Flame size={16} />
                </span>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold tabular-nums">{stats.streak}</p>
                <p className="mt-1 text-sm text-muted">{t("streakLabel")}</p>
              </CardContent>
            </Card>
          </div>

          {/* Weekly activity + weak topics + subject breakdown */}
          <div className="grid gap-5 lg:grid-cols-3">
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Icon name="chart" size={18} className="text-primary" />
                  {t("weeklyActivity")}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex h-32 items-end justify-between gap-2 sm:gap-3">
                  {stats.weekly_activity.map((day, i) => {
                    const hPct = Math.round((day.answered / maxDay) * 100);
                    return (
                      <div key={day.date} className="group flex flex-1 flex-col items-center gap-2">
                        <span className="text-[11px] font-medium tabular-nums text-subtle opacity-0 transition-opacity group-hover:opacity-100">
                          {day.answered}
                        </span>
                        <div className="flex w-full max-w-8 flex-1 items-end rounded-lg bg-surface-subtle px-1.5 pb-px pt-1.5">
                          <div
                            className={cn("bar-track w-full", day.correct > 0 ? "bg-success" : "bg-primary")}
                            style={{ height: `${Math.max(hPct || 8, 6)}%` }}
                            title={`${day.answered} ${t("answered").toLowerCase()}`}
                          />
                        </div>
                        <span className="text-[11px] font-medium text-subtle">
                          {i === 6
                            ? new Intl.DateTimeFormat(locale, { weekday: "narrow" }).format(new Date(day.date))
                            : WEEKDAYS.format(new Date(day.date)) || i}
                        </span>
                      </div>
                    );
                  })}
                </div>
                <div className="mt-4 flex flex-wrap gap-4 text-xs text-muted">
                  <span className="flex items-center gap-1.5">
                    <i className="h-2.5 w-2.5 rounded-full bg-primary" /> {exam("practiceTitle")}
                  </span>
                  <span className="flex items-center gap-1.5">
                    <i className="h-2.5 w-2.5 rounded-full bg-success" /> {res("correct")}
                  </span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Icon name="target" size={18} className="text-danger" />
                  {t("weakTitle")}
                </CardTitle>
              </CardHeader>
              <CardContent className="flex flex-col gap-3">
                {stats.weak_topics.length === 0 ? (
                  <p className="py-6 text-center text-sm text-subtle">{t("emptyState")}</p>
                ) : (
                  stats.weak_topics.map((wt) => {
                    const pct = Math.min(100, wt.wrong * 25);
                    return (
                      <div key={wt.topic_id} className="flex flex-col gap-1.5">
                        <div className="flex items-center justify-between gap-2">
                          <span className="truncate text-sm font-medium">{localName(wt, locale)}</span>
                          <span className="shrink-0 badge badge-danger">{wt.wrong}</span>
                        </div>
                        <span className="truncate text-xs text-subtle">{localSubjectName(wt, locale)}</span>
                        <div className="h-1.5 w-full overflow-hidden rounded-full bg-surface-subtle">
                          <div className="h-full rounded-full bg-danger" style={{ width: `${pct}%` }} />
                        </div>
                      </div>
                    );
                  })
                )}
              </CardContent>
            </Card>
          </div>

          {/* Subject breakdown + recent sessions */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Icon name="book" size={18} className="text-primary" />
                {t("subjectsTitle")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              {subjRows.length === 0 ? (
                <p className="py-6 text-center text-sm text-subtle">{t("emptyState")}</p>
              ) : (
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                  {subjRows.map((s) => {
                    const tone = scoreTone(s.accuracy);
                    return (
                      <Link
                        key={s.subject_id}
                        href={`/subjects/${s.slug}`}
                        className="card card-hover flex flex-col gap-2 p-4"
                      >
                        <div className="flex items-center justify-between gap-2">
                          <span className="truncate text-sm font-semibold">{localSubjectName(s, locale)}</span>
                          <span className={cn("badge", tone.bg)}>{s.accuracy}%</span>
                        </div>
                        <div className="h-1.5 w-full overflow-hidden rounded-full bg-surface-subtle">
                          <div className={cn("h-full rounded-full", tone.bar)} style={{ width: `${s.accuracy}%` }} />
                        </div>
                        <span className="text-xs text-subtle">
                          {s.sessions} {t("completedTests").toLowerCase()} · {s.questions} {res("correct").toLowerCase()}
                        </span>
                      </Link>
                    );
                  })}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Recent sessions */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle className="flex items-center gap-2">
                <Icon name="chart" size={18} className="text-primary" />
                {t("recentResults")}
              </CardTitle>
              <Link href="/subjects" className="flex items-center gap-1 text-sm font-semibold text-primary hover:underline">
                {t("startPractice")}
                <Icon name="arrowRight" size={15} />
              </Link>
            </CardHeader>
            <CardContent className="p-0 sm:p-6">
              {stats.recent_sessions.length === 0 ? (
                <p className="py-10 text-center text-sm text-subtle">{t("emptyState")}</p>
              ) : (
                <div className="nice-scroll overflow-x-auto">
                  <table className="table">
                    <thead>
                      <tr>
                        <th>{t("subject")}</th>
                        <th>{t("date")}</th>
                        <th>{res("correct")} / {res("incorrect")}</th>
                        <th className="text-right">{t("score")}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {stats.recent_sessions.map((s) => {
                        const done = s.status === "finished";
                        const tone = scoreTone(s.score_percent);
                        return (
                          <tr key={s.id}>
                            <td>
                              <div className="flex flex-col gap-0.5">
                                <Link
                                  href={`/subjects/${s.subject.slug}/practice`}
                                  className="font-medium hover:text-primary hover:underline"
                                >
                                  {localSubjectOnly(s.subject, locale)}
                                </Link>
                                <span className="badge badge-neutral">
                                  {s.mode === "exam" ? exam("title") : exam("practiceTitle")}
                                </span>
                              </div>
                            </td>
                            <td className="text-muted tabular-nums">
                              {dateFmt.format(new Date(s.started_at))}
                            </td>
                            <td className="tabular-nums">
                              <span className="font-semibold text-success">{s.correct_answers}</span>
                              {" / "}
                              <span className="font-semibold text-danger">{s.incorrect_answers}</span>
                            </td>
                            <td className="text-right">
                              {done ? (
                                <span className={cn("badge", tone.bg)}>{s.score_percent}%</span>
                              ) : (
                                <span className="badge badge-neutral">{t("inProgress")}</span>
                              )}
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              )}
            </CardContent>
          </Card>
        </>
      ) : null}
    </div>
  );
}

function localName(
  o: { topic_name_uz?: string; topic_name_ru?: string; topic_name_en?: string },
  locale: string
): string {
  if (locale === "ru") return o.topic_name_ru || o.topic_name_uz || "";
  if (locale === "en") return o.topic_name_en || o.topic_name_uz || "";
  return o.topic_name_uz || "";
}

function localSubjectName(
  o: { subject_name_uz?: string; subject_name_ru?: string; subject_name_en?: string },
  locale: string
): string {
  if (locale === "ru") return o.subject_name_ru || o.subject_name_uz || "";
  if (locale === "en") return o.subject_name_en || o.subject_name_uz || "";
  return o.subject_name_uz || "";
}

function localSubjectOnly(
  o: { name_uz?: string; name_ru?: string; name_en?: string },
  locale: string
): string {
  if (locale === "ru") return o.name_ru || o.name_uz || "";
  if (locale === "en") return o.name_en || o.name_uz || "";
  return o.name_uz || "";
}