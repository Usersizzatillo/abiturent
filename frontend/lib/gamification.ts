import { api } from "./api";

export interface LevelInfo {
  xp: number;
  level: number;
  level_progress: number;
  level_progress_pct: number;
  next_level_xp: number;
}

export interface BadgeItem {
  code: string;
  name_uz: string;
  name_ru: string;
  name_en: string;
  description_uz: string;
  description_ru: string;
  description_en: string;
  icon: string;
  earned: boolean;
}

export interface BadgeState {
  level: LevelInfo;
  earned_count?: number;
  badges: BadgeItem[];
}

export async function fetchBadges(): Promise<BadgeState> {
  return api<BadgeState>("/gamification/badges/");
}

export async function checkBadges(): Promise<BadgeState> {
  return api<BadgeState>("/gamification/badges/check/", { method: "POST" });
}
