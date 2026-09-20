"use client";

import { useEffect, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { localizedName, type Subject } from "@/lib/catalog";
import { fetchSubjects } from "@/lib/catalog";
import { Reveal } from "./reveal";

export function SubjectsGrid() {
  const t = useTranslations("landing");
  const locale = useLocale();
  const [subjects, setSubjects] = useState<Subject[] | null>(null);

  useEffect(() => {
    let cancelled = false;
    fetchSubjects()
      .then((data) => {
        if (!cancelled) setSubjects(data);
      })
      .catch(() => {
        if (!cancelled) setSubjects([]);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  if (!subjects) {
    return (
      <div className="mx-auto max-w-7xl px-4 pb-24 sm:px-6">
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {[0, 1, 2, 3].map((i) => (
            <div key={i} className="skeleton h-36 w-full" />
          ))}
        </div>
      </div>
    );
  }
  if (subjects.length === 0) return null;

  const featured = subjects.slice(0, 8);

  return (
    <section className="mx-auto max-w-7xl px-4 pb-24 sm:px-6">
      <Reveal>
        <div className="mx-auto mb-14 max-w-2xl text-center">
          <span className="badge badge-neutral mb-4">{t("directionsTag")}</span>
          <h2 className="text-display-sm text-balance">{t("directionsTitle")}</h2>
          <p className="mt-4 text-lg text-muted">{t("directionsSubtitle")}</p>
        </div>
      </Reveal>

      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {featured.map((s, i) => (
          <Reveal key={s.slug} delay={i * 70}>
            <Link
              href={`/subjects/${s.slug}`}
              className="bento-card group flex h-full flex-col p-6"
            >
              <span className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-primary-soft text-2xl transition-colors group-hover:bg-primary">
                {s.icon || s.code || "📘"}
              </span>
              <h3 className="font-semibold">{localizedName(s, locale)}</h3>
              <p className="mt-1 text-sm text-muted">
                {s.question_count > 0
                  ? t("directionsQuestions", { count: s.question_count.toLocaleString() })
                  : t("directionsTopics", { count: s.topic_count.toLocaleString() })}
              </p>
              <span className="mt-5 inline-flex items-center gap-1.5 text-sm font-semibold text-primary">
                {t("directionsStart")}
                <span aria-hidden className="transition-transform group-hover:translate-x-1">→</span>
              </span>
            </Link>
          </Reveal>
        ))}
      </div>
    </section>
  );
}