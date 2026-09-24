"use client";

import { useEffect, useMemo, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { ProtectedShell } from "@/components/layout/protected-shell";
import { Alert } from "@/components/ui/alert";
import { Card } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Link } from "@/i18n/navigation";
import { fetchSubjects, localizedName, type Subject } from "@/lib/catalog";

function ArrowIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M5 12h14m-6-6 6 6-6 6" />
    </svg>
  );
}

export default function SubjectsPage() {
  const t = useTranslations("subjects");
  const common = useTranslations("common");
  const locale = useLocale();

  const [subjects, setSubjects] = useState<Subject[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [reloadKey, setReloadKey] = useState(0);
  const [query, setQuery] = useState("");

  useEffect(() => {
    let ignore = false;
    fetchSubjects()
      .then((data) => {
        if (!ignore) setSubjects(data);
      })
      .catch(() => {
        if (!ignore) setError(common("error"));
      });
    return () => {
      ignore = true;
    };
  }, [reloadKey, common]);

  const filtered = useMemo(() => {
    if (!subjects) return null;
    const q = query.trim().toLowerCase();
    if (!q) return subjects;
    return subjects.filter((s) => localizedName(s, locale).toLowerCase().includes(q));
  }, [subjects, query, locale]);

  const retry = () => {
    setError(null);
    setReloadKey((k) => k + 1);
  };

  return (
    <ProtectedShell>
      <div className="mx-auto w-full max-w-7xl flex-1 px-4 py-8 sm:px-6">
        {/* Header */}
        <div className="mb-7 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div className="flex flex-col gap-1.5">
            <h1 className="text-3xl font-extrabold tracking-tight sm:text-4xl">{t("title")}</h1>
            <p className="font-serif text-lg italic text-muted">{t("subtitle")}</p>
          </div>
          {subjects ? (
            <span className="badge badge-neutral self-start px-3 py-1.5">
              {subjects.length} {t("total")}
            </span>
          ) : null}
        </div>

        {/* Search */}
        <div className="relative mb-6 max-w-md">
          <svg
            className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-subtle"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            aria-hidden
          >
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.3-4.3" />
          </svg>
          <input
            className="input pl-10"
            placeholder={t("search")}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            aria-label={t("search")}
          />
        </div>

        {error ? (
          <div className="flex flex-col gap-3">
            <Alert variant="danger">{error}</Alert>
            <button type="button" className="btn btn-secondary btn-sm self-start" onClick={retry}>
              {common("retry")}
            </button>
          </div>
        ) : null}

        {!filtered && !error ? (
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {[0, 1, 2, 3, 4, 5].map((i) => (
              <Skeleton key={i} className="h-44" />
            ))}
          </div>
        ) : filtered && filtered.length === 0 ? (
          <div className="card flex flex-col items-center gap-3 p-14 text-center">
            <p className="text-muted">{common("empty")}</p>
            <button type="button" className="btn btn-secondary btn-sm" onClick={() => setQuery("")}>
              {common("reset")}
            </button>
          </div>
        ) : filtered ? (
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {filtered.map((subject) => (
              <Link key={subject.id} href={`/subjects/${subject.slug}`} className="group">
                <Card className="card-hover relative h-full overflow-hidden p-6">
                  <span
                    aria-hidden
                    className="absolute -right-10 -top-10 h-32 w-32 rounded-full bg-primary-soft opacity-70 transition-transform duration-300 group-hover:scale-150"
                  />
                  <div className="relative flex flex-col">
                    <span className="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-navy text-lg font-bold text-primary-foreground shadow-raised">
                      {(subject.code || localizedName(subject, locale).charAt(0)).toUpperCase()}
                    </span>
                    <h3 className="text-lg font-semibold tracking-tight">
                      {localizedName(subject, locale)}
                    </h3>
                    <div className="mt-3 flex items-center gap-3">
                      <span className="badge badge-neutral">
                        {subject.topic_count} {t("topics")}
                      </span>
                      <span className="badge badge-primary">
                        {subject.question_count} {t("questions")}
                      </span>
                    </div>
                    <span className="mt-5 inline-flex items-center gap-1.5 text-sm font-semibold text-primary">
                      {t("startPractice")}
                      <ArrowIcon />
                    </span>
                  </div>
                </Card>
              </Link>
            ))}
          </div>
        ) : null}
      </div>
    </ProtectedShell>
  );
}