import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";

export function Footer() {
  const t = useTranslations("nav");

  return (
    <footer className="border-t border-border bg-background">
      <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 px-4 py-8 sm:px-6 md:flex-row">
        <div className="flex flex-col items-center gap-1 md:items-start">
          <span className="font-bold tracking-tight">Abiturend</span>
          <span className="text-sm text-subtle">
            DTM / BMB imtihonlariga tayyorgarlik platformasi
          </span>
        </div>
        <div className="flex items-center gap-6 text-sm text-muted">
          <Link href="/subjects" className="transition-colors hover:text-foreground">
            {t("subjects")}
          </Link>
          <Link href="/universities" className="transition-colors hover:text-foreground">
            {t("universities")}
          </Link>
          <Link href="/login" className="transition-colors hover:text-foreground">
            {t("login")}
          </Link>
        </div>
      </div>
    </footer>
  );
}