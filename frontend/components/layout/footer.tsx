import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";

export function Footer() {
  const t = useTranslations("nav");

  return (
    <footer className="border-t border-border bg-surface/60 backdrop-blur-sm">
      <div className="mx-auto w-full max-w-7xl px-4 py-10 sm:px-6">
        <div className="grid gap-8 md:grid-cols-[1.2fr_1fr] md:items-center">
          <div className="flex items-center gap-3">
            <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-primary-hover text-lg font-bold text-primary-foreground shadow-md shadow-primary/25">
              A
            </span>
            <div className="flex flex-col">
              <span className="text-lg font-extrabold tracking-tight text-foreground">
                Abiturend
              </span>
              <span className="font-serif italic text-sm text-subtle">
                DTM / BMB imtihonlariga tayyorgarlik platformasi
              </span>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <Link
              href="/subjects"
              className="rounded-full border border-border bg-surface px-4 py-1.5 text-sm font-medium text-muted transition-colors hover:border-border-strong hover:text-foreground"
            >
              {t("subjects")}
            </Link>
            <Link
              href="/universities"
              className="rounded-full border border-border bg-surface px-4 py-1.5 text-sm font-medium text-muted transition-colors hover:border-border-strong hover:text-foreground"
            >
              {t("universities")}
            </Link>
            <Link
              href="/login"
              className="rounded-full border border-border bg-surface px-4 py-1.5 text-sm font-medium text-muted transition-colors hover:border-border-strong hover:text-foreground"
            >
              {t("login")}
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}