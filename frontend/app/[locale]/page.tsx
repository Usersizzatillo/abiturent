import { getTranslations, setRequestLocale } from "next-intl/server";
import { Header } from "@/components/layout/header";
import { Footer } from "@/components/layout/footer";
import { Link } from "@/i18n/navigation";
import { Reveal } from "@/components/landing/reveal";
import {
  AnalyticsMockup,
  ExamAppMockup,
  StudyMockup,
} from "@/components/landing/illustrations";

const STATS = [
  { key: "statsStudents", value: "12 000+", icon: "users" },
  { key: "statsQuestions", value: "25 000+", icon: "book" },
  { key: "statsExams", value: "120+", icon: "clock" },
  { key: "statsUniversities", value: "40+", icon: "building" },
] as const;

const FEATURES = [
  { key: "featPractice", icon: "pencil", feature: "practice" },
  { key: "featExam", icon: "timer", feature: "exam" },
  { key: "featAnalytics", icon: "chart", feature: "analytics" },
  { key: "featUni", icon: "building", feature: "university" },
] as const;

function Icon({ name, size = 22 }: { name: string; size?: number }) {
  const paths: Record<string, React.ReactNode> = {
    users: <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" />,
    book: <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V2H6.5A2.5 2.5 0 0 0 4 4.5v15A2.5 2.5 0 0 0 6.5 22H20V20H6.5A2.5 2.5 0 0 1 4 17.5z" />,
    clock: <><circle cx="12" cy="12" r="10" /><path d="M12 6v6l4 2" /></>,
    building: <><rect x="4" y="2" width="16" height="20" rx="2" /><path d="M9 22v-4h6v4M8 6h.01M16 6h.01M12 6h.01M8 10h.01M16 10h.01M12 10h.01M8 14h.01M16 14h.01M12 14h.01" /></>,
    pencil: <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z" />,
    timer: <><circle cx="12" cy="13" r="8" /><path d="M12 9v4l2 2M9 2h6" /></>,
    chart: <><path d="M3 3v18h18" /><rect x="7" y="12" width="3" height="6" /><rect x="12" y="8" width="3" height="10" /><rect x="17" y="4" width="3" height="14" /></>,
    check: <path d="M20 6 9 17l-5-5" />,
    rocket: <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09zM12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2zM9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5" />,
    checkCircle: <><circle cx="12" cy="12" r="10" /><path d="m8.5 12 2.5 2.5 5-5" /></>,
    sparkles: <><path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9L12 3z" /><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8L19 15z" /></>,
    arrowRight: <path d="M5 12h14m-6-6 6 6-6 6" />,
    command: <><rect x="3" y="3" width="18" height="18" rx="6" /><circle cx="9" cy="9" r="1.5" /><circle cx="15" cy="15" r="1.5" /><path d="M9 15h6M15 9H9" /></>,
    layers: <path d="m12 2 9 5-9 5-9-5 9-5zM3 12l9 5 9-5M3 17l9 5 9-5" />,
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
    >
      {paths[name]}
    </svg>
  );
}

export default async function LandingPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations("landing");

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    name: "Abiturend",
    url: "https://abituriyent.orgtrace.uz",
    applicationCategory: "EducationalApplication",
    operatingSystem: "Any",
    availableLanguage: ["uz", "ru", "en"],
    description: t("heroSubtitle"),
    about: {
      "@type": "Organization",
      name: "Abiturend",
      description: "DTM / BMB imtihonlariga tayyorgarlik platformasi",
    },
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <Header />
      <main className="page-enter flex-1">
        {/* ============ HERO ============ */}
        <section className="hero-bg relative overflow-hidden">
          <div aria-hidden className="hero-grid pointer-events-none absolute inset-0" />
          <div aria-hidden className="hero-glow pointer-events-none absolute inset-x-0 top-0 h-[36rem]" />
          <div className="relative mx-auto max-w-7xl px-4 pb-16 pt-16 text-center sm:px-6 sm:pt-24">
            <Reveal>
              <span className="badge badge-primary gap-2 px-4 py-1.5 text-sm">
                <Icon name="sparkles" size={16} />
                {t("badge")}
              </span>
            </Reveal>
            <Reveal delay={60}>
              <p className="mt-6 font-serif text-xl italic text-muted sm:text-2xl">
                {t("heroTagline")}
              </p>
            </Reveal>
            <Reveal delay={100}>
              <h1 className="mx-auto mt-3 max-w-4xl text-balance text-5xl font-extrabold leading-[1.05] tracking-tight sm:text-7xl">
                {t("heroTitle")}
              </h1>
            </Reveal>
            <Reveal delay={160}>
              <span className="text-gradient mt-4 block font-serif text-2xl font-medium italic leading-snug sm:text-4xl">
                {t("heroHighlight")}
              </span>
            </Reveal>
            <Reveal delay={220}>
              <p className="mx-auto mt-5 max-w-2xl text-lg leading-8 text-muted sm:text-xl">
                {t("heroSubtitle")}
              </p>
            </Reveal>
            <Reveal delay={280}>
              <div className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row">
                <Link href="/register" className="btn btn-primary btn-lg w-full shadow-raised sm:w-auto">
                  <Icon name="rocket" size={18} />
                  {t("ctaStart")}
                </Link>
                <Link href="/login" className="btn btn-secondary btn-lg w-full sm:w-auto">
                  {t("ctaLogin")}
                </Link>
              </div>
              <p className="mt-5 flex items-center justify-center gap-2 text-sm text-subtle">
                <Icon name="checkCircle" size={16} />
                {t("heroProof")}
              </p>
            </Reveal>
          </div>

          {/* Product shot */}
          <Reveal delay={340} className="relative mx-auto max-w-5xl px-4 sm:px-6">
            <div aria-hidden className="accent-blob pointer-events-none absolute -inset-8 -z-10 rounded-[3rem] opacity-70 blur-2xl" />
            <div className="lift relative overflow-hidden rounded-3xl border border-border-strong bg-surface shadow-popover ring-1 ring-black/5 dark:ring-white/10">
              <ExamAppMockup className="h-auto w-full" />
            </div>
          </Reveal>
        </section>

        {/* ============ STATS ============ */}
        <section className="mx-auto -mt-0 max-w-7xl px-4 pb-4 pt-10 sm:px-6">
          <Reveal>
            <div className="grid grid-cols-2 gap-4 rounded-3xl border border-border bg-surface p-4 shadow-raised sm:grid-cols-4 sm:p-6">
              {STATS.map((s, i) => (
                <div key={s.key} className="flex flex-col items-center px-2 py-3 text-center">
                  <div className={`mb-2 flex h-10 w-10 items-center justify-center rounded-2xl ${i % 2 ? "bg-accent-soft text-accent" : "bg-primary-soft text-primary"}`}>
                    <Icon name={s.icon} size={19} />
                  </div>
                  <p className="text-2xl font-extrabold tabular-nums">{s.value}</p>
                  <p className="text-sm text-muted">{t(s.key)}</p>
                </div>
              ))}
            </div>
          </Reveal>
        </section>

        {/* ============ SHOWCASE — Practice ============ */}
        <section className="mx-auto max-w-7xl px-4 py-24 sm:px-6">
          <Reveal>
            <div className="mb-16 text-center">
              <span className="badge badge-neutral mb-4">
                <Icon name="command" size={15} />
                01
              </span>
              <h2 className="text-h2 mx-auto max-w-2xl text-balance">{t("showcaseTitle")}</h2>
            </div>
          </Reveal>
          <div className="grid items-center gap-12 lg:grid-cols-2">
            <Reveal>
              <div className="lift overflow-hidden rounded-3xl border border-border-strong bg-surface shadow-raised">
                <StudyMockup className="h-auto w-full" />
              </div>
            </Reveal>
            <Reveal delay={120}>
              <div>
                <span className="badge badge-primary mb-4">
                  <Icon name="pencil" size={15} />
                  {t("showcasePracticeTag")}
                </span>
                <h3 className="text-3xl font-bold tracking-tight">
                  {t("showcasePracticeTitle")}
                </h3>
                <p className="mt-4 text-lg leading-7 text-muted">
                  {t("showcasePracticeDesc")}
                </p>
                <ul className="mt-7 flex flex-col gap-3.5">
                  {[1, 2, 3].map((i) => (
                    <li key={i} className="flex items-start gap-3">
                      <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-success-soft text-success">
                        <Icon name="checkCircle" size={15} />
                      </span>
                      <span className="font-medium">
                        {t(`showcasePracticeP${i}`)}
                      </span>
                    </li>
                  ))}
                </ul>
                <Link href="/subjects" className="btn btn-primary btn-sm mt-9">
                  {t("ctaStart")}
                  <Icon name="arrowRight" size={16} />
                </Link>
              </div>
            </Reveal>
          </div>
        </section>

        {/* ============ SHOWCASE — Analytics ============ */}
        <section className="border-t border-border bg-surface-subtle">
          <div className="mx-auto max-w-7xl px-4 py-24 sm:px-6">
            <div className="grid items-center gap-12 lg:grid-cols-2">
              <Reveal className="lg:order-2">
                <div className="lift overflow-hidden rounded-3xl border border-border-strong bg-surface shadow-raised">
                  <AnalyticsMockup className="h-auto w-full" />
                </div>
              </Reveal>
              <Reveal delay={120} className="lg:order-1">
                <div>
                  <span className="badge badge-info mb-4">
                    <Icon name="chart" size={15} />
                    {t("showcaseAnalyticsTag")}
                  </span>
                  <h3 className="text-3xl font-bold tracking-tight">
                    {t("showcaseAnalyticsTitle")}
                  </h3>
                  <p className="mt-4 text-lg leading-7 text-muted">
                    {t("showcaseAnalyticsDesc")}
                  </p>
                  <ul className="mt-7 flex flex-col gap-3.5">
                    {[1, 2, 3].map((i) => (
                      <li key={i} className="flex items-start gap-3">
                        <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-success-soft text-success">
                          <Icon name="checkCircle" size={15} />
                        </span>
                        <span className="font-medium">
                          {t(`showcaseAnalyticsP${i}`)}
                        </span>
                      </li>
                    ))}
                  </ul>
                  <Link href="/register" className="btn btn-secondary btn-sm mt-9">
                    {t("ctaStart")}
                    <Icon name="arrowRight" size={16} />
                  </Link>
                </div>
              </Reveal>
            </div>
          </div>
        </section>

        {/* ============ FEATURES ============ */}
        <section className="mx-auto max-w-7xl px-4 py-24 sm:px-6">
          <Reveal>
            <div className="mb-14 text-center">
              <h2 className="text-h2">{t("featuresTitle")}</h2>
              <p className="mt-3 text-lg text-muted">{t("featuresSubtitle")}</p>
            </div>
          </Reveal>
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {FEATURES.map((f, i) => (
              <Reveal key={f.key} delay={i * 90}>
                <div className="card card-hover group h-full rounded-3xl p-6">
                  <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-2xl bg-primary-soft text-primary transition-colors group-hover:bg-primary group-hover:text-primary-foreground">
                    <Icon name={f.icon} />
                  </div>
                  <h3 className="mb-2 font-semibold">{t(`${f.feature}Title`)}</h3>
                  <p className="text-sm leading-6 text-muted">{t(`${f.feature}Desc`)}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </section>

        {/* ============ HOW IT WORKS ============ */}
        <section className="border-t border-border bg-surface-subtle">
          <div className="mx-auto max-w-7xl px-4 py-24 sm:px-6">
            <Reveal>
              <div className="mb-14 text-center">
                <h2 className="text-h2">{t("howItWorksTitle")}</h2>
                <p className="mt-3 text-lg text-muted">{t("howItWorksSubtitle")}</p>
              </div>
            </Reveal>
            <div className="relative grid gap-10 md:grid-cols-3 md:gap-8">
              <div
                aria-hidden
                className="absolute left-1/2 top-8 hidden h-px w-2/3 -translate-x-1/2 border-t border-dashed border-border-strong md:block"
              />
              {([1, 2, 3] as const).map((step, i) => (
                <Reveal key={step} delay={i * 120}>
                  <div className="card relative rounded-3xl p-7 text-center">
                    <span className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-primary-hover text-2xl font-bold text-primary-foreground shadow-raised">
                      {step}
                    </span>
                    <h3 className="mb-2 text-lg font-semibold">{t(`step${step}Title`)}</h3>
                    <p className="text-sm leading-6 text-muted">{t(`step${step}Desc`)}</p>
                  </div>
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        {/* ============ FINAL CTA ============ */}
        <section className="mx-auto max-w-7xl px-4 py-24 sm:px-6">
          <Reveal>
            <div className="hero-bg relative overflow-hidden rounded-3xl border border-border p-10 text-center sm:p-16">
              <div aria-hidden className="hero-grid pointer-events-none absolute inset-0 opacity-70" />
              <div aria-hidden className="accent-blob pointer-events-none absolute -inset-16 opacity-60 blur-3xl" />
              <div className="relative flex flex-col items-center gap-6">
                <span className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-primary-hover text-primary-foreground shadow-raised">
                  <Icon name="layers" size={26} />
                </span>
                <h2 className="text-h2 max-w-xl text-balance sm:text-3xl">{t("ctaStart")}</h2>
                <div className="flex flex-col gap-3 sm:flex-row">
                  <Link href="/register" className="btn btn-primary btn-lg">
                    <Icon name="rocket" size={18} />
                    {t("ctaStart")}
                  </Link>
                  <Link href="/login" className="btn btn-secondary btn-lg">
                    {t("ctaLogin")}
                  </Link>
                </div>
              </div>
            </div>
          </Reveal>
        </section>
      </main>
      <Footer />
    </>
  );
}