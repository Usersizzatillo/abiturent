/** Premium photo-driven landing illustrations (real photography, theme-aware UI chips). */
import Image from "next/image";

export const PHOTOS = {
  exam: "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1600&q=80",
  study: "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=1600&q=80",
  analytics:
    "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=1600&q=80",
  bank: "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=1200&q=80",
  conditions:
    "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=1200&q=80",
  mentor: "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1200&q=80",
} as const;

function Frame({
  photo,
  className,
  variant = "light",
  priority = false,
  children,
}: {
  photo: string;
  className?: string;
  variant?: "light" | "dark";
  priority?: boolean;
  children?: React.ReactNode;
}) {
  const overlay =
    variant === "dark"
      ? "from-black/60 via-black/20 to-transparent"
      : "from-black/35 via-transparent to-transparent";
  return (
    <div
      className={`relative aspect-[620/460] w-full overflow-hidden rounded-[1.5rem] ring-1 ring-black/10 dark:ring-white/10 ${className ?? ""}`}
    >
      <Image
        src={photo}
        alt=""
        fill
        className="object-cover"
        sizes="(max-width: 1024px) 100vw, 60vw"
        priority={priority}
      />
      <div aria-hidden className={`absolute inset-0 bg-gradient-to-t ${overlay}`} />
      <div aria-hidden className="absolute inset-0 bg-primary/5 mix-blend-multiply" />
      {children}
    </div>
  );
}

/** Windows-chrome + exam player UI over real photography: question, timer, progress. */
export function ExamAppMockup({ className }: { className?: string }) {
  return (
    <div
      className={`relative aspect-[620/460] w-full ${className ?? ""}`}
      role="img"
      aria-label="Imtihon rejimi"
    >
      <Frame photo={PHOTOS.exam} variant="dark" className="ring-0" priority>
        {/* window chrome */}
        <div className="absolute inset-x-0 top-0 flex h-10 items-center gap-1.5 rounded-t-[1.5rem] border-b border-white/15 bg-black/25 px-4 backdrop-blur-md">
          <span className="h-3 w-3 rounded-full bg-[#f97066]" />
          <span className="h-3 w-3 rounded-full bg-[#fdb022]" />
          <span className="h-3 w-3 rounded-full bg-[#32d583]" />
          <span className="mx-auto flex h-6 w-40 items-center justify-center rounded-lg bg-white/10 text-[10px] font-medium text-white/80">
            abiturend.uz — Imtihon
          </span>
        </div>

        {/* timer chip */}
        <div className="absolute left-4 top-16 flex items-center gap-2 rounded-full bg-warning/95 px-3.5 py-1.5 text-xs font-bold text-white shadow-raised backdrop-blur">
          <span className="h-2 w-2 rounded-full bg-white/90" />
          <span className="tabular-nums">24:16</span>
        </div>
        {/* question chip */}
        <div className="absolute right-4 top-16 flex items-center gap-2 rounded-full bg-primary/95 px-3.5 py-1.5 text-xs font-bold text-primary-foreground shadow-raised backdrop-blur">
          Savol 12 / 90
        </div>

        {/* answer row */}
        <div className="absolute inset-x-4 bottom-4 flex items-center justify-between rounded-2xl border border-white/20 bg-white/15 px-5 py-4 backdrop-blur-lg">
          <div className="flex items-center gap-3">
            <span className="flex h-9 w-9 items-center justify-center rounded-full bg-success text-sm font-extrabold text-white">
              A
            </span>
            <span className="flex h-9 w-9 items-center justify-center rounded-full bg-white/20 text-sm font-bold text-white">
              B
            </span>
            <span className="flex h-9 w-9 items-center justify-center rounded-full bg-white/20 text-sm font-bold text-white">
              C
            </span>
            <span className="flex h-9 w-9 items-center justify-center rounded-full bg-white/20 text-sm font-bold text-white">
              D
            </span>
          </div>
          <span className="inline-flex items-center gap-1.5 rounded-xl bg-navy px-5 py-2.5 text-sm font-bold text-primary-foreground shadow-raised">
            Yuborish
            <span aria-hidden>→</span>
          </span>
        </div>
      </Frame>

      {/* floating chip: score up */}
      <div className="anim-float glass-strong absolute left-[-1.5rem] top-1/4 z-10 flex items-center gap-3 rounded-2xl px-4 py-3 shadow-raised">
        <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-success-soft text-success">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
            <path d="M20 6 9 17l-5-5" />
          </svg>
        </span>
        <span>
          <span className="block text-sm font-extrabold tabular-nums">140 ball</span>
          <span className="block text-[11px] text-muted">yuqori natija</span>
        </span>
      </div>

      {/* floating chip: streak */}
      <div className="anim-float-slow glass-strong absolute -right-3 top-1/2 z-10 flex items-center gap-3 rounded-2xl px-4 py-3 shadow-raised">
        <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-warning-soft text-warning">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
            <path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z" />
          </svg>
        </span>
        <span>
          <span className="block text-sm font-extrabold tabular-nums">7 kun</span>
          <span className="block text-[11px] text-muted">seriya (streak)</span>
        </span>
      </div>
    </div>
  );
}

/** Results dashboard over real photography: score ring, trend, subject breakdown. */
export function AnalyticsMockup({ className }: { className?: string }) {
  return (
    <div
      className={`relative aspect-[620/460] w-full ${className ?? ""}`}
      role="img"
      aria-label="Natijalar analitikasi"
    >
      <Frame photo={PHOTOS.analytics} variant="dark" className="ring-0">
        {/* window chrome */}
        <div className="absolute inset-x-0 top-0 flex h-10 items-center gap-1.5 rounded-t-[1.5rem] border-b border-white/15 bg-black/25 px-4 backdrop-blur-md">
          <span className="h-3 w-3 rounded-full bg-[#f97066]" />
          <span className="h-3 w-3 rounded-full bg-[#fdb022]" />
          <span className="h-3 w-3 rounded-full bg-[#32d583]" />
          <span className="mx-auto flex h-6 w-44 items-center justify-center rounded-lg bg-white/10 text-[10px] font-medium text-white/80">
            Mening natijalarim
          </span>
        </div>

        {/* trend card */}
        <div className="absolute inset-x-4 bottom-4 rounded-2xl border border-white/20 bg-white/15 p-4 backdrop-blur-lg">
          <div className="flex items-center justify-between text-xs font-medium text-white/90">
            <span>O‘sish dinamikasi</span>
            <span className="font-bold text-success">+18%</span>
          </div>
          <div className="mt-3 flex h-16 items-end gap-1.5">
            {[34, 52, 44, 66, 58, 80, 92].map((h, i) => (
              <span
                key={i}
                className={`flex-1 rounded-md bg-gradient-to-t ${
                  i === 6
                    ? "from-primary to-primary-hover"
                    : "from-white/30 to-white/10"
                }`}
                style={{ height: `${h}%` }}
              />
            ))}
          </div>
          <div className="mt-2.5 flex gap-2 text-[10px] font-medium text-white/70">
            <span className="rounded-full bg-success px-2 py-0.5 text-white">To‘g‘ri 82%</span>
            <span className="rounded-full bg-warning px-2 py-0.5 text-white">Xato 9%</span>
            <span className="rounded-full bg-white/15 px-2 py-0.5">Bo‘sh 9%</span>
          </div>
        </div>
      </Frame>

      {/* floating card: score ring */}
      <div className="anim-float glass-strong absolute right-[-1.5rem] top-14 z-10 flex flex-col items-center gap-1 rounded-2xl px-5 py-4 shadow-raised">
        <svg width="62" height="62" viewBox="0 0 62 62" aria-hidden>
          <circle cx="31" cy="31" r="26" stroke="var(--surface-subtle)" strokeWidth="8" fill="none" />
          <circle
            cx="31"
            cy="31"
            r="26"
            stroke="var(--success)"
            strokeWidth="8"
            strokeDasharray="122 42"
            strokeLinecap="round"
            transform="rotate(-90 31 31)"
            fill="none"
          />
          <text x="31" y="37" textAnchor="middle" fontSize="15" fontWeight="700" fill="var(--foreground)">
            160
          </text>
        </svg>
        <span className="text-[11px] font-medium text-muted">umumiy ball</span>
      </div>

      {/* floating card: subject breakdown */}
      <div className="anim-float-slow glass-strong absolute left-[-1.5rem] top-1/2 z-10 w-44 rounded-2xl px-4 py-3.5 shadow-raised">
        <span className="block text-xs font-bold">Fanlar bo‘yicha</span>
        <div className="mt-3 flex flex-col gap-2.5">
          {[
            { c: "var(--success)", w: 92, l: "Matematika" },
            { c: "var(--primary)", w: 74, l: "Fizika" },
            { c: "var(--warning)", w: 55, l: "Ingliz tili" },
          ].map((r) => (
            <span key={r.l} className="flex items-center gap-2">
              <span className="w-20 truncate text-[11px] text-muted">{r.l}</span>
              <span className="h-1.5 flex-1 overflow-hidden rounded-full bg-surface-subtle">
                <span className="block h-full rounded-full" style={{ width: `${r.w}%`, background: r.c }} />
              </span>
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

/** Study / mistake-review photo with mastery bars. */
export function StudyMockup({ className }: { className?: string }) {
  return (
    <div
      className={`relative aspect-[620/460] w-full ${className ?? ""}`}
      role="img"
      aria-label="Mavzu bo‘yicha mashq"
    >
      <Frame photo={PHOTOS.study} variant="dark" className="ring-0">
        {/* window chrome */}
        <div className="absolute inset-x-0 top-0 flex h-10 items-center gap-1.5 rounded-t-[1.5rem] border-b border-white/15 bg-black/25 px-4 backdrop-blur-md">
          <span className="h-3 w-3 rounded-full bg-[#f97066]" />
          <span className="h-3 w-3 rounded-full bg-[#fdb022]" />
          <span className="h-3 w-3 rounded-full bg-[#32d583]" />
          <span className="mx-auto flex h-6 w-40 items-center justify-center rounded-lg bg-white/10 text-[10px] font-medium text-white/80">
            Mavzular ustida ishlash
          </span>
        </div>

        {/* mastery list */}
        <div className="absolute inset-x-4 bottom-4 rounded-2xl border border-white/20 bg-white/15 p-4 backdrop-blur-lg">
          {[
            { l: "Trigonometriya", w: 96, c: "var(--success)", p: "100%" },
            { l: "Hosila", w: 72, c: "var(--primary)", p: "75%" },
            { l: "Logarifmlar", w: 48, c: "var(--warning)", p: "50%" },
          ].map((r) => (
            <div key={r.l} className="mb-2.5 flex items-center gap-3 last:mb-0">
              <span className="w-28 truncate text-xs font-medium text-white/90">{r.l}</span>
              <span className="h-2 flex-1 overflow-hidden rounded-full bg-white/20">
                <span
                  className="block h-full rounded-full"
                  style={{ width: `${r.w}%`, background: r.c }}
                />
              </span>
              <span className="w-10 text-right text-[11px] font-bold tabular-nums" style={{ color: r.c }}>
                {r.p}
              </span>
            </div>
          ))}
        </div>
      </Frame>

      {/* floating chip: questions solved */}
      <div className="anim-float glass-strong absolute left-[-1.5rem] top-1/4 z-10 flex items-center gap-3 rounded-2xl px-4 py-3 shadow-raised">
        <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-success-soft text-success">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
            <path d="m8.5 12 2.5 2.5 5-5" />
          </svg>
        </span>
        <span>
          <span className="block text-sm font-extrabold tabular-nums">1 240</span>
          <span className="block text-[11px] text-muted">savol yechildi</span>
        </span>
      </div>

      {/* floating chip: progress */}
      <div className="anim-float-slow glass-strong absolute -right-3 top-1/2 z-10 flex items-center gap-3 rounded-2xl px-4 py-3 shadow-raised">
        <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary-soft text-primary">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
            <path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z" />
          </svg>
        </span>
        <span>
          <span className="block text-sm font-extrabold tabular-nums">68%</span>
          <span className="block text-[11px] text-muted">umumiy progress</span>
        </span>
      </div>
    </div>
  );
}