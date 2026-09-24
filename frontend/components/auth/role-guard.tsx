"use client";

import { useEffect } from "react";
import { useRouter } from "@/i18n/navigation";
import { Skeleton } from "@/components/ui/skeleton";
import { useAuth } from "@/components/providers/auth-provider";

export function TeacherGuard({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  const allowed = (() => {
    if (!user) return false;
    return user.role === "teacher" || user.role === "admin" || user.is_staff;
  })();

  useEffect(() => {
    if (loading) return;
    if (!user) {
      router.replace("/login?next=/teacher/questions");
    } else if (!allowed) {
      router.replace("/dashboard");
    }
  }, [loading, user, allowed, router]);

  if (loading || !user || !allowed) {
    return (
      <div className="flex flex-col gap-4">
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-40 w-full" />
      </div>
    );
  }

  return <>{children}</>;
}