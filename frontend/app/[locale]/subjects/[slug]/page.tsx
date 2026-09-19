"use client";

import { useParams } from "next/navigation";
import { ProtectedShell } from "@/components/layout/protected-shell";
import { SubjectDetailClient } from "@/components/subjects/subject-detail-client";

export default function SubjectDetailPage() {
  const params = useParams();
  const slug = Array.isArray(params.slug) ? params.slug[0] : params.slug ?? "";
  return (
    <ProtectedShell>
      <main className="mx-auto w-full max-w-7xl flex-1 px-4 py-8 sm:px-6">
        <SubjectDetailClient slug={slug} />
      </main>
    </ProtectedShell>
  );
}