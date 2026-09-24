import { api } from "./api";

export interface Subject {
  id: number;
  name_uz: string;
  name_ru: string;
  name_en: string;
  slug: string;
  code: string;
  icon: string;
  sort_order: number;
  topic_count: number;
  question_count: number;
}

export interface Subtopic {
  id: number;
  name_uz: string;
  name_ru: string;
  name_en: string;
  sort_order: number;
}

export interface Topic {
  id: number;
  name_uz: string;
  name_ru: string;
  name_en: string;
  slug: string;
  sort_order: number;
  question_count: number;
  subtopics: Subtopic[];
}

export interface SubjectDetail extends Subject {
  topics: Topic[];
}

export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export async function fetchSubjects(): Promise<Subject[]> {
  const data = await api<Paginated<Subject>>("/subjects/?page_size=100");
  return data.results;
}

export async function fetchSubject(slug: string): Promise<SubjectDetail> {
  return api<SubjectDetail>(`/subjects/${slug}/`);
}

export async function fetchTopics(subjectSlug: string): Promise<Topic[]> {
  return api<Topic[]>(`/subjects/${subjectSlug}/topics/`);
}

export function localizedName(
  item: { name_uz: string; name_ru: string; name_en: string },
  locale: string
): string {
  if (locale === "ru" && item.name_ru) return item.name_ru;
  if (locale === "en" && item.name_en) return item.name_en;
  return item.name_uz || item.name_ru || item.name_en;
}