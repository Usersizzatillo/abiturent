"use client";

import { useTranslations } from "next-intl";
import { useState } from "react";
import { AuthShell } from "@/components/auth/auth-shell";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Link } from "@/i18n/navigation";

export default function ForgotPasswordPage() {
  const t = useTranslations("auth");
  const common = useTranslations("common");
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [pending, setPending] = useState(false);

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setPending(true);
    // Reset link yuborish keyingi fazalarda (email backend) ulangan bo'ladi.
    setTimeout(() => {
      setPending(false);
      setSent(true);
    }, 500);
  };

  return (
    <AuthShell
      title={t("forgotTitle")}
      footer={
        <>
          {t("haveAccount")}{" "}
          <Link href="/login" className="font-semibold text-primary hover:underline">
            {t("loginLink")}
          </Link>
        </>
      }
    >
      {sent ? (
        <Alert variant="success">{t("forgotBtn")}</Alert>
      ) : (
        <form onSubmit={onSubmit} className="flex flex-col gap-4">
          <Input
            label={t("email")}
            name="email"
            type="email"
            autoComplete="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <Button type="submit" disabled={pending} className="w-full">
            {pending ? common("loading") : t("forgotBtn")}
          </Button>
        </form>
      )}
    </AuthShell>
  );
}