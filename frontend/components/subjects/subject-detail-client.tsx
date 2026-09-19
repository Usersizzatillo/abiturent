"use client";

import { useLocale, useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Link } from "@/i18n/navigation";
import { fetchSubject, localizedName, type SubjectDetail } from "@/lib/catalog";

export function SubjectDetailClient({ slug }: { slug: string }) {
  const t = useTranslations("subjects");
  const common = useTranslations("common");
  const locale = useLocale();

  const [subject, setSubject] = useState<SubjectDetail | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let ignore = false;
    fetchSubject(slug)
      .then((data) => {
        if (!ignore) setSubject(data);
      })
      .catch(() => {
        if (!ignore) setError(common("error"));
      });
    return () => {
      ignore = true;
    };
  }, [slug, common]);

  if (error) {
    return (
      <div className="flex flex-col gap-3">
        <div className="card p-6">{error}</div>
        <Link href="/subjects" className="btn btn-secondary btn-sm self-start">
          {common("back")}
        </Link>
      </div>
    );
  }

  if (!subject) {
    return (
      <div className="flex flex-col gap-5">
        <Skeleton className="h-8 w-64" />
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {[0, 1, 2].map((i) => (
            <Skeleton key={i} className="h-28" />
          ))}
        </div>
      </div>
    );
  }

  const topics = subject.topics ?? [];

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">
            {localizedName(subject, locale)}
          </h1>
          <p className="mt-1 text-muted">
            {topics.length} {t("topics")} · {subject.question_count}{" "}
            {t("questions")}
          </p>
        </div>
        <Link
          href={`/subjects/${subject.slug}/practice`}
          className="btn btn-primary btn-md"
        >
          {t("startPractice")}
        </Link>
      </div>

      {topics.length === 0 ? (
        <div className="card flex flex-col items-center gap-3 p-14 text-center">
          <p className="text-muted">{common("empty")}</p>
        </div>
      ) : (
        <div className="grid gap-5 sm:grid-cols-2">
          {topics.map((topic) => (
            <Card key={topic.id} className="card-hover p-6">
              <h3 className="font-semibold">{localizedName(topic, locale)}</h3>
              {topic.subtopics.length > 0 ? (
                <ul className="mt-3 flex flex-col gap-1.5">
                  {topic.subtopics.map((st) => (
                    <li key={st.id} className="text-sm text-muted">
                      {localizedName(st, locale)}
                    </li>
                  ))}
                </ul>
              ) : null}
              <div className="mt-3 flex items-center gap-4 text-sm text-muted">
                <span>
                  {topic.question_count} {t("questions")}
                </span>
                <span>{t("difficulty")}</span>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}