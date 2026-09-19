import { useTranslations } from "next-intl";

export default function NotFound() {
  const t = useTranslations("common");
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 bg-background px-4 text-center">
      <p className="text-6xl font-bold text-primary">404</p>
      <h1 className="text-h2">Sahifa topilmadi</h1>
      <p className="text-muted">{t("empty")}</p>
    </main>
  );
}