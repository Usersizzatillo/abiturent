import { api } from "./api";

export type SessionMode = "practice" | "exam";
export type SessionStatus = "in_progress" | "finished";

export interface SessionOption {
  id: number;
  text_uz: string;
  text_ru: string;
  text_en: string;
  sort_order: number;
}

export interface SessionQuestion {
  id: number;
  text_uz: string;
  text_ru: string;
  text_en: string;
  question_type: "single" | "multiple";
  difficulty: number;
  options: SessionOption[];
}

export interface PracticeSession {
  id: number;
  mode: SessionMode;
  subject: number;
  topic: number | null;
  status: SessionStatus;
  question_count: number;
  progress_index: number;
  correct_answers: number;
  incorrect_answers: number;
  started_at: string;
  finished_at: string | null;
  current_question?: SessionQuestion | null;
}

export interface CurrentResponse {
  question: SessionQuestion | null;
  unanswered_count: number;
}

export interface AnswerResult {
  is_correct: boolean;
  correct_option_id: number;
  explanation_uz: string;
  explanation_ru: string;
  explanation_en: string;
  correct_count: number;
  total_count: number;
}

export interface FinishedReport {
  id: number;
  mode: SessionMode;
  subject: number;
  status: SessionStatus;
  question_count: number;
  correct_answers: number;
  incorrect_answers: number;
  unanswered: number;
  score_percent: number;
  started_at: string;
  finished_at: string | null;
}

export interface ReviewOption extends SessionOption {
  is_correct: boolean;
}

export interface ReviewQuestion {
  id: number;
  text_uz: string;
  text_ru: string;
  text_en: string;
  question_type: "single" | "multiple";
  difficulty: number;
  explanation_uz: string;
  explanation_ru: string;
  explanation_en: string;
  options: ReviewOption[];
}

export interface QuestionReview {
  question: ReviewQuestion;
  selected_option_id: number | null;
  is_correct: boolean;
}

export interface SessionReport extends FinishedReport {
  questions: QuestionReview[];
}

export async function startPractice(input: {
  subject: number;
  topic?: number | null;
  question_count?: number;
  mode?: SessionMode;
}): Promise<PracticeSession> {
  return api<PracticeSession>("/sessions/", {
    method: "POST",
    body: JSON.stringify({ topic: input.topic ?? null, ...input }),
  });
}

export async function fetchCurrent(sessionId: number): Promise<CurrentResponse> {
  return api<CurrentResponse>(`/sessions/${sessionId}/current/`);
}

export async function submitAnswer(
  sessionId: number,
  questionId: number,
  optionId: number
): Promise<AnswerResult> {
  return api<AnswerResult>(`/sessions/${sessionId}/answer/`, {
    method: "POST",
    body: JSON.stringify({ question_id: questionId, option_id: optionId }),
  });
}

export async function finishSession(sessionId: number): Promise<SessionReport> {
  return api<SessionReport>(`/sessions/${sessionId}/finish/`, {
    method: "POST",
  });
}

export async function fetchSessionReport(sessionId: number): Promise<SessionReport> {
  return api<SessionReport>(`/sessions/${sessionId}/report/`);
}

export async function fetchSessionQuestions(
  sessionId: number
): Promise<SessionQuestion[]> {
  const data = await api<{ questions: SessionQuestion[] }>(
    `/sessions/${sessionId}/questions/`
  );
  return data.questions;
}

export interface SessionListItem {
  id: number;
  mode: SessionMode;
  subject: {
    id: number;
    name_uz: string;
    name_ru: string;
    name_en: string;
    slug: string;
  };
  topic: null | { id: number; name_uz: string; name_ru: string; name_en: string };
  status: SessionStatus;
  question_count: number;
  correct_answers: number;
  incorrect_answers: number;
  unanswered: number;
  score_percent: number;
  started_at: string;
  finished_at: string | null;
}

export async function fetchSessionList(): Promise<SessionListItem[]> {
  const data = await api<{ results: SessionListItem[] }>("/sessions/");
  return data.results;
}