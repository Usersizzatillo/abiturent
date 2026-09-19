"use client";

import { useTranslations } from "next-intl";
import { useRouter } from "@/i18n/navigation";
import { useAuth } from "@/components/providers/auth-provider";
import { api } from "@/lib/api";
import { Link } from "@/i18n/navigation";

export function UserMenu() {
  const t = useTranslations("nav");
  const { user, setUser } = useAuth();
  const router = useRouter();

  if (!user) {
    return (
      <div className="flex items-center gap-2">
        <Link href="/login" className="btn btn-secondary btn-sm">
          {t("login")}
        </Link>
        <Link href="/register" className="btn btn-primary btn-sm hidden sm:inline-flex">
          {t("register")}
        </Link>
      </div>
    );
  }

  const onLogout = async () => {
    try {
      await api("/auth/logout/", { method: "POST" });
    } finally {
      setUser(null);
      router.replace("/login");
      router.refresh();
    }
  };

  return (
    <div className="flex items-center gap-2">
      <Link href="/dashboard" className="btn btn-ghost btn-sm">
        {t("dashboard")}
      </Link>
      {user.role === "teacher" || user.role === "admin" || user.is_staff ? (
        <Link href="/teacher/questions" className="btn btn-ghost btn-sm">
          {t("teacherPanel")}
        </Link>
      ) : null}
      <Link
        href="/profile"
        className="hidden items-center gap-2 rounded-full py-1 pl-1 pr-3 text-sm font-medium transition-colors hover:bg-surface-subtle sm:flex"
      >
        <span className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-sm font-semibold text-primary-foreground">
          {(user.first_name || user.username).charAt(0).toUpperCase()}
        </span>
        {user.first_name || user.username}
      </Link>
      <button
        type="button"
        onClick={onLogout}
        className="btn btn-ghost btn-sm"
      >
        {t("logout")}
      </button>
    </div>
  );
}