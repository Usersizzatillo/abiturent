"use client";

import { useEffect, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { ProtectedShell } from "@/components/layout/protected-shell";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useAuth } from "@/components/providers/auth-provider";
import { ApiError } from "@/lib/api";
import {
  checkBadges,
  fetchBadges,
  type BadgeState,
} from "@/lib/gamification";
import { localizedName } from "@/lib/catalog";
import { cn } from "@/lib/utils";

const ICON_PATHS: Record<string, string> = {
  footprints: "M4 16v-2a3 3 0 0 1 6 0v2M6 16v4M14 8V6a3 3 0 0 1 6 0v2M16 8v4",
  repeat: "M17 2l4 4-4 4M3 11v-1a4 4 0 0 1 4-4h14M7 22l-4-4 4-4M21 13v1a4 4 0 0 1-4 4H3",
  trophy:
    "M6 9H4.5a2.5 2.5 0 0 1 0-5H6M18 9h1.5a2.5 2.5 0 0 0 0-5H18M4 22h16M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22M18 2H6v7a6 6 0 0 0 12 0V2Z",
  flame:
    "M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z",
  fire: "M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5S12.5 6 12 2c-.5 4-2 6.5-4 8.5S5 13 5 15a7 7 0 0 0 7 7z",
  crown: "M2 4l3 12h14l3-12-6 7-4-7-4 7-6-7zM3 20h18",
  crosshair:
    "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM22 12h-4M6 12H2M12 6V2M12 22v-4",
  star: "M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z",
  shield: "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z",
  graduation:
    "M22 10L12 5 2 10l10 5 10-5zM6 12v5c0 1 3 3 6 3s6-2 6-3v-5",
  compass:
    "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM16.24 7.76l-2.12 6.36-6.36 2.12 2.12-6.36 6.36-2.12z",
  timer: "M10 2h4M12 14l3-3M12 22a8 8 0 1 0 0-16 8 8 0 0 0 0 16z",
};

function BadgeIcon({ name }: { name: string }) {
  return (
    <svg
      width="22"
      height="22"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden
    >
      <path d={ICON_PATHS[name] ?? ICON_PATHS.star} />
    </svg>
  );
}

export default function AchievementsPage() {
  const t = useTranslations("gamification");
  const common = useTranslations("common");
  const plan = useTranslations("premium");
  const nav = useTranslations("nav");
  const locale = useLocale();
  const { user, loading } = useAuth();
  const [state, setState] = useState<BadgeState | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  const fail = (e: unknown) => {
    if (e instanceof ApiError && (e.status === 401 || e.status === 403)) {
      setError(plan("needLogin"));
    } else {
      setError(common("error"));
    }
  };

  useEffect(() => {
    if (loading || !user) return;
    fetchBadges().then(setState).catch(fail);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, loading]);

  const onCheck = async () => {
    setPending(true);
    setError(null);
    try {
      setState(await checkBadges());
    } catch (e) {
      fail(e);
    } finally {
      setPending(false);
    }
  };

  const earned = state?.badges.filter((b) => b.earned).length ?? 0;
  const total = state?.badges.length ?? 0;
  const level = state?.level ?? null;

  return (
    <ProtectedShell>
      <div className="mx-auto w-full max-w-4xl flex-1 px-4 py-8 sm:px-6">
        <div className="bg-navy relative overflow-hidden rounded-3xl p-6 text-white sm:p-8">
          <div aria-hidden className="pointer-events-none absolute -right-14 -top-14 h-48 w-48 rounded-full bg-primary/40 blur-3xl" />
          <div aria-hidden className="pointer-events-none absolute -bottom-16 -left-8 h-40 w-40 rounded-full bg-teal/30 blur-3xl" />
          <div className="relative flex flex-col gap-4">
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div className="flex flex-col gap-1">
                <p className="text-xs font-semibold uppercase tracking-widest text-slate-300">
                  {t("level")} {level?.level ?? 1}
                </p>
                <h1 className="text-2xl font-extrabold tracking-tight sm:text-3xl">
                  {t("title")}
                </h1>
                <p className="text-sm text-slate-300">
                  {t("earnedOf", { earned, total })}
                </p>
              </div>
              <div className="flex flex-col items-end gap-1">
                <span className="badge badge-warning">{t("xp")}</span>
                <span className="text-2xl font-extrabold tabular-nums">
                  {level?.xp ?? 0}
                </span>
              </div>
            </div>

            <div className="flex flex-col gap-1.5">
              <div className="flex items-center justify-between text-xs font-semibold text-slate-300">
                <span>{t("levelProgress")}</span>
                <span>
                  {t("toNextLevel", {
                    xp:
                      (level?.next_level_xp ?? 200) - (level?.level_progress ?? 0),
                  })}
                </span>
              </div>
              <div className="h-2.5 w-full overflow-hidden rounded-full bg-white/15">
                <div
                  className="h-full rounded-full bg-teal transition-all"
                  style={{ width: `${level?.level_progress_pct ?? 0}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        <div className="mt-6 flex flex-col gap-4">
          {error ? <Alert variant="danger">{error}</Alert> : null}

          <div className="flex items-center justify-between">
            <h2 className="text-lg font-extrabold tracking-tight">
              {t("badges")}
            </h2>
            <Button
              size="sm"
              variant="secondary"
              disabled={pending || !user}
              onClick={onCheck}
            >
              {pending ? common("loading") : common("retry")}
            </Button>
          </div>

          {!loading && !user ? (
            <div className="card flex flex-col items-center gap-3 p-10 text-center">
              <p className="text-muted">{plan("needLogin")}</p>
              <Link href="/login" className="btn btn-primary btn-sm">
                {nav("login")}
              </Link>
            </div>
          ) : !state && !error ? (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {[0, 1, 2, 3, 4, 5].map((i) => (
                <Skeleton key={i} className="h-32" />
              ))}
            </div>
          ) : state && state.badges.length === 0 ? (
            <div className="card p-10 text-center text-muted">{t("empty")}</div>
          ) : state ? (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {state.badges.map((b) => (
                <div
                  key={b.code}
                  className={cn(
                    "card flex flex-col gap-3 p-5",
                    !b.earned && "opacity-70"
                  )}
                >
                  <div className="flex items-start justify-between gap-3">
                    <span
                      className={cn(
                        "flex h-11 w-11 items-center justify-center rounded-2xl",
                        b.earned
                          ? "bg-warning-soft text-warning"
                          : "bg-surface-subtle text-subtle"
                      )}
                    >
                      <BadgeIcon name={b.icon} />
                    </span>
                    <span
                      className={cn(
                        "badge",
                        b.earned ? "badge-success" : "badge-neutral"
                      )}
                    >
                      {b.earned ? t("earned") : t("locked")}
                    </span>
                  </div>
                  <div className="flex flex-col gap-1">
                    <p className="font-semibold tracking-tight">
                      {localizedName(b, locale)}
                    </p>
                    <p className="text-sm text-muted">
                      {localizedName(
                        {
                          name_uz: b.description_uz,
                          name_ru: b.description_ru,
                          name_en: b.description_en,
                        },
                        locale
                      )}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ) : null}
        </div>
      </div>
    </ProtectedShell>
  );
}
