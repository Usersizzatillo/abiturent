import { api } from "./api";

export interface SubscriptionPlan {
  id: number;
  code: string;
  tier: "free" | "pro";
  name_uz: string;
  name_ru: string;
  name_en: string;
  description_uz: string;
  description_ru: string;
  description_en: string;
  price_uzs: number;
  duration_days: number;
  max_sessions_per_day: number | null;
  unlimited_sessions: boolean;
}

export interface ActiveSubscription {
  id: number;
  plan: string;
  plan_name_uz: string;
  plan_name_ru: string;
  plan_name_en: string;
  starts_at: string;
  ends_at: string | null;
  is_active: boolean;
}

export interface SubscriptionState {
  is_premium: boolean;
  plan: ActiveSubscription | null;
  remaining_sessions_today: number | null;
}

export async function fetchPlans(): Promise<SubscriptionPlan[]> {
  return api<SubscriptionPlan[]>("/premium/plans/");
}

export async function fetchSubscription(): Promise<SubscriptionState> {
  return api<SubscriptionState>("/premium/subscription/");
}

export async function subscribe(planCode: string): Promise<SubscriptionState> {
  return api<SubscriptionState>("/premium/subscribe/", {
    method: "POST",
    body: JSON.stringify({ plan_code: planCode }),
  });
}
