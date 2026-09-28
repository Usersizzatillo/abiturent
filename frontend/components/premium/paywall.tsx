"use client";

import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";

export function Paywall({
  onBack,
  backLabel,
}: {
  onBack: () => void;
  backLabel: string;
}) {
  const t = useTranslations("premium");

  return (
    <div className="mx-auto flex w-full max-w-md flex-1 flex-col items-center gap-4 px-4 py-16 text-center">
      <span className="flex h-14 w-14 items-center justify-center rounded-2xl bg-warning-soft text-warning">
        <svg
          width="26"
          height="26"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden
        >
          <rect x="3" y="11" width="18" height="11" rx="2" />
          <path d="M7 11V7a5 5 0 0 1 10 0v4" />
        </svg>
      </span>
      <h2 className="text-xl font-extrabold tracking-tight">
        {t("paywallTitle")}
      </h2>
      <p className="text-sm text-muted">{t("paywallDesc")}</p>
      <div className="flex flex-wrap items-center justify-center gap-3">
        <Link href="/premium" className="btn btn-primary">
          {t("paywallCta")}
        </Link>
        <button type="button" className="btn btn-secondary" onClick={onBack}>
          {backLabel}
        </button>
      </div>
    </div>
  );
}
