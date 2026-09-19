"use client";

import { useParams } from "next/navigation";
import { PracticePlayer } from "@/components/practice/practice-player";

export default function SubjectPracticePage() {
  const params = useParams();
  const slug = Array.isArray(params.slug) ? params.slug[0] : params.slug ?? "";
  return <PracticePlayer slug={slug} />;
}