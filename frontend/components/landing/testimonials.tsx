import Image from "next/image";
import { useTranslations } from "next-intl";
import { Reveal } from "./reveal";

const AVATARS = [
  "https://randomuser.me/api/portraits/women/44.jpg",
  "https://randomuser.me/api/portraits/men/32.jpg",
  "https://randomuser.me/api/portraits/women/68.jpg",
];

export function Testimonials() {
  const t = useTranslations("landing");
  const items = [1, 2, 3] as const;

  return (
    <section className="border-t border-border bg-surface-subtle/50">
      <div className="mx-auto max-w-7xl px-4 py-24 sm:px-6">
        <Reveal>
          <div className="mx-auto mb-14 max-w-2xl text-center">
            <span className="badge badge-primary mb-4">{t("testimonialsTag")}</span>
            <h2 className="text-display-sm text-balance">{t("testimonialsTitle")}</h2>
            <p className="mt-4 text-lg text-muted">{t("testimonialsSubtitle")}</p>
          </div>
        </Reveal>

        <div className="grid gap-6 md:grid-cols-3">
          {items.map((n, i) => (
            <Reveal key={n} delay={i * 110}>
              <figure className="bento-card flex h-full flex-col p-8">
                <div className="mb-5 flex gap-1 text-accent" aria-label="5/5">
                  {[1, 2, 3, 4, 5].map((s) => (
                    <svg key={s} width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden>
                      <path d="M12 2l2.9 6.26 6.6.68-4.94 4.4 1.42 6.48L12 16.42l-5.98 3.4 1.42-6.48L2.5 8.94l6.6-.68L12 2z" />
                    </svg>
                  ))}
                </div>
                <blockquote className="flex-1">
                  <p className="text-[15px] leading-7 text-foreground">
                    “{t(`testimonial${n}Quote`)}”
                  </p>
                </blockquote>
                <figcaption className="mt-7 flex items-center gap-3 border-t border-border pt-6">
                  <Image
                    src={AVATARS[i]}
                    alt={t(`testimonial${n}Name`)}
                    width={48}
                    height={48}
                    className="h-12 w-12 shrink-0 rounded-full object-cover shadow-raised ring-2 ring-white/60 dark:ring-white/10"
                  />
                  <div className="flex flex-col">
                    <span className="font-semibold">{t(`testimonial${n}Name`)}</span>
                    <span className="text-sm text-muted">{t(`testimonial${n}Role`)}</span>
                  </div>
                </figcaption>
              </figure>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}