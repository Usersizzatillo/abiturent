import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";

const BOT_URL = "https://t.me/AbituriyentUzbekBot";

export function Footer() {
  const t = useTranslations("nav");
  const f = useTranslations("footer");

  return (
    <footer className="border-t border-border bg-surface/60 backdrop-blur-sm">
      <div className="mx-auto w-full max-w-7xl px-4 py-14 sm:px-6">
        <div className="grid gap-10 md:grid-cols-[1.4fr_1fr_1fr]">
          <div className="flex flex-col gap-3">
            <div className="flex items-center gap-3">
              <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-primary-hover text-lg font-bold text-primary-foreground shadow-md shadow-primary/25">
                A
              </span>
              <div className="flex flex-col">
                <span className="text-lg font-extrabold tracking-tight text-foreground">
                  Abiturend
                </span>
                <span className="font-serif italic text-sm text-subtle">
                  {f("brandTagline")}
                </span>
              </div>
            </div>
            <p className="max-w-md text-sm leading-6 text-muted">
              {f("brandDesc")}
            </p>
          </div>

          <div className="flex flex-col gap-2.5">
            <span className="mb-1 text-xs font-semibold uppercase tracking-wider text-subtle">
              {f("platform")}
            </span>
            <Link
              href="/subjects"
              className="text-sm text-muted transition-colors hover:text-foreground"
            >
              {t("subjects")}
            </Link>
            <Link
              href="/mock-exams"
              className="text-sm text-muted transition-colors hover:text-foreground"
            >
              {t("mockExams")}
            </Link>
            <Link
              href="/universities"
              className="text-sm text-muted transition-colors hover:text-foreground"
            >
              {t("universities")}
            </Link>
          </div>

          <div className="flex flex-col gap-2.5">
            <span className="mb-1 text-xs font-semibold uppercase tracking-wider text-subtle">
              {f("services")}
            </span>
            <Link
              href="/login"
              className="text-sm text-muted transition-colors hover:text-foreground"
            >
              {t("login")}
            </Link>
            <Link
              href="/register"
              className="text-sm text-muted transition-colors hover:text-foreground"
            >
              {t("register")}
            </Link>
            <a
              href={BOT_URL}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1.5 text-sm text-muted transition-colors hover:text-foreground"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden>
                <path d="M9.04 15.51 8.9 19.3c.47 0 .68-.2.93-.45l2.24-2.14 4.65 3.4c.85.47 1.46.23 1.69-.79l3.06-14.4c.27-1.2-.43-1.68-1.23-1.38L2.5 9.86c-1.16.46-1.14 1.1-.2 1.4l4.32 1.35L16.6 5.9c.47-.31.9-.14.55.18L9.04 15.51z" />
              </svg>
              {t("telegramBot")}
            </a>
          </div>
        </div>

        <div className="mt-12 flex flex-col items-center justify-between gap-3 border-t border-border pt-6 text-xs text-subtle sm:flex-row">
          <span>© {new Date().getFullYear()} Abiturend. {f("rights")}</span>
          <span>{f("location")}</span>
        </div>
      </div>
    </footer>
  );
}