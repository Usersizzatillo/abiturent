import type { MetadataRoute } from "next";
import { routing } from "@/i18n/routing";

const base = "https://abituriyent.orgtrace.uz";

export default function sitemap(): MetadataRoute.Sitemap {
  const locales = routing.locales;
  const paths = ["", "/subjects", "/universities", "/mock-exams", "/login", "/register"];

  return paths.flatMap((path) =>
    locales.map((locale) => ({
      url: `${base}/${locale}${path}`,
      lastModified: new Date(),
      changeFrequency: "weekly" as const,
      priority: path === "" ? 1 : 0.8,
    }))
  );
}