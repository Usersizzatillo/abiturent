"use client";

import { useTranslations } from "next-intl";
import { useState } from "react";
import { ProtectedShell } from "@/components/layout/protected-shell";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/components/providers/auth-provider";
import { api, ApiError, extractFieldError } from "@/lib/api";

export default function ProfilePage() {
  const t = useTranslations("auth");
  const common = useTranslations("common");
  const { user, refresh } = useAuth();

  const [form, setForm] = useState({
    first_name: user?.first_name ?? "",
    last_name: user?.last_name ?? "",
    email: user?.email ?? "",
    phone: user?.phone ?? "",
  });
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  const [pass, setPass] = useState({
    old_password: "",
    new_password: "",
    confirm: "",
  });
  const [passError, setPassError] = useState<string | null>(null);
const [passPending, setPassPending] = useState(false);

  const saveProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setPending(true);
    setSaved(false);
    setError(null);
    try {
      await api("/auth/me/", {
        method: "PATCH",
        body: JSON.stringify(form),
      });
      await refresh();
      setSaved(true);
    } catch (err) {
      setError(
        err instanceof ApiError
          ? extractFieldError(err.detail) ?? t("errorRequired")
          : t("errorRequired")
      );
    } finally {
      setPending(false);
    }
  };

  const changePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setPassPending(true);
    setPassError(null);
    setSaved(false);
    if (pass.new_password !== pass.confirm) {
      setPassError(t("errorRequired"));
      setPassPending(false);
      return;
    }
    try {
      await api("/auth/change-password/", {
        method: "POST",
        body: JSON.stringify({
          old_password: pass.old_password,
          new_password: pass.new_password,
        }),
      });
      setPass({ old_password: "", new_password: "", confirm: "" });
      setSaved(true);
    } catch (err) {
      setPassError(
        err instanceof ApiError
          ? (extractFieldError(err.detail, "old_password") ??
              extractFieldError(err.detail) ??
              t("errorRequired"))
          : t("errorRequired")
      );
    } finally {
      setPassPending(false);
    }
  };

  return (
    <ProtectedShell>
      <div className="mx-auto w-full max-w-3xl flex-1 px-4 py-8 sm:px-6">
        <h1 className="mb-6 text-3xl font-bold tracking-tight">{t("welcomeBack")}</h1>
        <div className="flex flex-col gap-6">
          <Card>
            <CardHeader>
              <CardTitle>{t("profile")}</CardTitle>
              <CardDescription>{t("username")}</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={saveProfile} className="flex flex-col gap-4">
                {saved ? <Alert variant="success">{t("successRegister")}</Alert> : null}
                {error ? <Alert variant="danger">{error}</Alert> : null}
                <div className="grid gap-4 sm:grid-cols-2">
                  <Input
                    label={t("firstName")}
                    name="first_name"
                    value={form.first_name}
                    onChange={(e) => setForm({ ...form, first_name: e.target.value })}
                  />
                  <Input
                    label={t("lastName")}
                    name="last_name"
                    value={form.last_name}
                    onChange={(e) => setForm({ ...form, last_name: e.target.value })}
                  />
                </div>
                <Input
                  label={t("email")}
                  name="email"
                  type="email"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                />
                <Input
                  label={t("phone")}
                  name="phone"
                  type="tel"
                  value={form.phone}
                  onChange={(e) => setForm({ ...form, phone: e.target.value })}
                />
                <div className="flex justify-end">
                  <Button type="submit" disabled={pending}>
                    {pending ? common("loading") : common("save")}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>{t("forgotTitle")}</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={changePassword} className="flex flex-col gap-4">
                {passError ? <Alert variant="danger">{passError}</Alert> : null}
                <Input
                  label={t("oldPassword")}
                  name="old_password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={pass.old_password}
                  onChange={(e) => setPass({ ...pass, old_password: e.target.value })}
                />
                <Input
                  label={t("newPassword")}
                  name="new_password"
                  type="password"
                  autoComplete="new-password"
                  required
                  hint={t("passwordHint")}
                  value={pass.new_password}
                  onChange={(e) => setPass({ ...pass, new_password: e.target.value })}
                />
                <Input
                  label={t("confirmPassword")}
                  name="confirm"
                  type="password"
                  autoComplete="new-password"
                  required
                  value={pass.confirm}
                  onChange={(e) => setPass({ ...pass, confirm: e.target.value })}
                />
                <div className="flex justify-end">
                  <Button type="submit" disabled={passPending} variant="secondary">
                    {passPending ? common("loading") : common("save")}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </ProtectedShell>
  );
}
