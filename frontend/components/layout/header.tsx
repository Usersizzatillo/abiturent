"use client";

import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { LocaleSwitcher } from "./locale-switcher";
import { ThemeToggle } from "./theme-toggle";
import { UserMenu } from "./user-menu";

export function Header() {
  const t = useTranslations("nav");

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-background/85 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-4 px-4 sm:px-6">
        <Link href="/" className="flex items-center gap-2">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
              <path d="M22 10v6M2 10l10-5 10 5-10 5z" />
              <path d="M6 12v5c3 3 9 3 12 0v-5" />
            </svg>
          </span>
          <span className="text-lg font-bold tracking-tight">Abiturend</span>
        </Link>

        <nav className="hidden items-center gap-6 text-sm font-medium text-muted md:flex">
          <Link href="/subjects" className="transition-colors hover:text-foreground">
            {t("subjects")}
          </Link>
          <Link href="/mock-exams" className="transition-colors hover:text-foreground">
            {t("mockExams")}
          </Link>
          <Link href="/universities" className="transition-colors hover:text-foreground">
            {t("universities")}
          </Link>
        </nav>

        <div className="flex items-center gap-2">
          <LocaleSwitcher className="hidden sm:block" />
          <ThemeToggle />
          <UserMenu />
        </div>
      </div>
    </header>
  );
}