"use client";

import { ProtectedShell } from "@/components/layout/protected-shell";
import { TeacherGuard } from "@/components/auth/role-guard";
import { QuestionsManager } from "@/components/teacher/questions-manager";

export default function TeacherQuestionsPage() {
  return (
    <ProtectedShell>
      <div className="mx-auto w-full max-w-7xl flex-1 px-4 py-8 sm:px-6">
        <TeacherGuard>
          <QuestionsManager />
        </TeacherGuard>
      </div>
    </ProtectedShell>
  );
}