import { getTranslations, setRequestLocale } from "next-intl/server";
import { DashboardClient } from "@/components/dashboard/dashboard-client";
import { ProtectedShell } from "@/components/layout/protected-shell";

export default async function DashboardPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations("dashboard");

  return (
    <ProtectedShell>
      <div className="mx-auto w-full max-w-7xl flex-1 px-4 py-8 sm:px-6">
        <div className="mb-6 flex flex-col gap-1">
          <h1 className="text-3xl font-bold tracking-tight">{t("title")}</h1>
          <p className="text-muted">{t("studyActivity")}</p>
        </div>
        <DashboardClient />
      </div>
    </ProtectedShell>
  );
}