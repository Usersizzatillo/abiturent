"use client";

import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { StudyMockup } from "@/components/landing/illustrations";
import { cn } from "@/lib/utils";

function CheckCircle() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <circle cx="12" cy="12" r="10" />
      <path d="m8.5 12 2.5 2.5 5-5" />
    </svg>
  );
}

function Logo({ size = 34 }: { size?: number }) {
  return (
    <Link href="/" aria-label="Abiturend home">
      <span
        className="flex items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-primary-hover text-primary-foreground shadow-raised"
        style={{ height: size, width: size }}
      >
        <svg width={size * 0.55} height={size * 0.55} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
          <path d="M22 10v6M2 10l10-5 10 5-10 5z" />
          <path d="M6 12v5c3 3 9 3 12 0v-5" />
        </svg>
      </span>
    </Link>
  );
}

const BENEFITS = [
  { icon: "featPractice", tone: "text-primary" },
  { icon: "featExam", tone: "text-warning" },
  { icon: "featAnalytics", tone: "text-success" },
] as const;

export function AuthShell({
  title,
  subtitle,
  children,
  footer,
  className,
}: {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
  className?: string;
}) {
  const landing = useTranslations("landing");

  return (
    <main className="grid min-h-screen lg:grid-cols-2">
      {/* Brand panel */}
      <div className="hero-bg relative hidden flex-col overflow-hidden p-10 lg:flex lg:p-12">
        <div aria-hidden className="hero-grid pointer-events-none absolute inset-0" />
        <div className="relative flex items-center gap-3">
          <Logo />
          <span className="text-xl font-extrabold tracking-tight">Abiturend</span>
        </div>

        <div className="relative mt-auto flex flex-col gap-8">
          <h1 className="text-4xl font-extrabold leading-tight tracking-tight xl:text-5xl">
            {landing("heroTitle")}
            <span className="text-gradient mt-2 block font-serif text-xl font-medium italic xl:text-2xl">
              {landing("heroHighlight")}
            </span>
          </h1>
          <ul className="flex flex-col gap-3">
            {BENEFITS.map((b) => (
              <li key={b.icon} className="flex items-center gap-3 text-muted">
                <span className={cn("flex h-7 w-7 items-center justify-center rounded-full bg-surface", b.tone)}>
                  <CheckCircle />
                </span>
                {landing(`${b.icon}Title`)}
              </li>
            ))}
          </ul>
          <div className="pointer-events-none opacity-90">
            <StudyMockup className="h-auto w-full" />
          </div>
        </div>

        <p className="relative mt-8 text-sm text-subtle">© {new Date().getFullYear()} Abiturend</p>
      </div>

      {/* Form side */}
      <div className="relative flex min-h-screen flex-col items-center justify-center px-4 py-12">
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 -z-10 lg:hidden"
          style={{
            background: "radial-gradient(36rem circle at 50% -12%, var(--primary-soft) 0%, transparent 60%)",
          }}
        />
        <div className="lg:hidden">
          <Logo size={44} />
        </div>
        <div className={cn("w-full max-w-md", className)}>
          <div className="card rounded-3xl p-8" style={{ boxShadow: "var(--shadow-raised)" }}>
            <div className="mb-6 text-center">
              <h1 className="text-2xl font-extrabold tracking-tight">{title}</h1>
              {subtitle ? (
                <p className="mt-2 text-sm text-muted">{subtitle}</p>
              ) : null}
            </div>
            {children}
          </div>
          {footer ? (
            <div className="mt-6 text-center text-sm text-muted">{footer}</div>
          ) : null}
        </div>
      </div>
    </main>
  );
}