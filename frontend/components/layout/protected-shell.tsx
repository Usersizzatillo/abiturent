"use client";

import { Header } from "@/components/layout/header";
import { Footer } from "@/components/layout/footer";
import { useAuth } from "@/components/providers/auth-provider";
import { Skeleton } from "@/components/ui/skeleton";

export function ProtectedShell({ children }: { children: React.ReactNode }) {
  const { loading } = useAuth();

  return (
    <>
      <Header />
      <main className="flex flex-1 flex-col">
        {loading ? (
          <div className="mx-auto flex w-full max-w-7xl flex-col gap-5 px-4 py-8 sm:px-6">
            <Skeleton className="h-8 w-64" />
            <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
              {[0, 1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-32" />
              ))}
            </div>
          </div>
        ) : (
          <div className="flex flex-1 flex-col">{children}</div>
        )}
      </main>
      <Footer />
    </>
  );
}