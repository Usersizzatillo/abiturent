import { api } from "./api";

export type QuestionStatus = "draft" | "published" | "archived";
export type QuestionType = "single" | "multiple";
export type Difficulty = 1 | 2 | 3;
export type SourceType = "dtm" | "bmb" | "custom" | "unknown";

export interface QuestionOption {
  id?: number;
  text_uz: string;
  text_ru?: string;
  text_en?: string;
  is_correct: boolean;
  sort_order?: number;
}

export interface Question {
  id: number;
  subject: number;
  topic: number | null;
  subtopic: number | null;
  text_uz: string;
  text_ru: string;
  text_en: string;
  question_type: QuestionType;
  difficulty: Difficulty;
  explanation_uz: string;
  explanation_ru: string;
  explanation_en: string;
  source_type: SourceType;
  is_official: boolean;
  is_verified: boolean;
  status: QuestionStatus;
  created_by: number | null;
  options: QuestionOption[];
  created_at: string;
  updated_at: string;
}

export interface QuestionInput {
  subject: number;
  topic: number | null;
  text_uz: string;
  text_en?: string;
  question_type: QuestionType;
  difficulty: Difficulty;
  explanation_uz?: string;
  source_type: SourceType;
  status: QuestionStatus;
  options: QuestionOption[];
}

export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export async function fetchQuestions(params: {
  subject?: number;
  status?: QuestionStatus;
} = {}): Promise<Question[]> {
  const query = new URLSearchParams();
  query.set("page_size", "100");
  if (params.subject) query.set("subject", String(params.subject));
  if (params.status) query.set("status", params.status);
  const data = await api<Paginated<Question>>(`/questions/?${query.toString()}`);
  return data.results;
}

export async function createQuestion(
  input: QuestionInput
): Promise<Question> {
  return api<Question>("/questions/", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function updateQuestion(
  id: number,
  input: Partial<QuestionInput>
): Promise<Question> {
  return api<Question>(`/questions/${id}/`, {
    method: "PATCH",
    body: JSON.stringify(input),
  });
}

export async function deleteQuestion(id: number): Promise<void> {
  await api(`/questions/${id}/`, { method: "DELETE" });
}