/** Theme-aware, hand-crafted premium illustrations used on the landing page. */

function Ui() {
  return (
    <defs>
      <linearGradient id="l-grad" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stopColor="var(--primary)" />
        <stop offset="100%" stopColor="#7c3aed" />
      </linearGradient>
      <linearGradient id="l-grad-soft" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stopColor="var(--primary-soft)" stopOpacity="0.9" />
        <stop offset="100%" stopColor="var(--info-soft)" />
      </linearGradient>
      <filter id="l-soft" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="10" stdDeviation="14" floodColor="rgb(16 24 40)" floodOpacity="0.14" />
      </filter>
      <filter id="l-chip" x="-40%" y="-40%" width="180%" height="180%">
        <feDropShadow dx="0" dy="6" stdDeviation="8" floodColor="var(--foreground)" floodOpacity="0.18" />
      </filter>
    </defs>
  );
}

/** Windows-chrome + exam player UI: question card, options, progress, timer. */
export function ExamAppMockup({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 620 460"
      role="img"
      aria-hidden
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <Ui />
      {/* soft backdrop */}
      <rect x="42" y="30" width="536" height="404" rx="22" fill="url(#l-grad-soft)" />
      {/* window */}
      <g filter="url(#l-soft)">
        <rect x="70" y="56" width="480" height="352" rx="16" fill="var(--surface)" stroke="var(--border-strong)" />
        {/* chrome */}
        <rect x="70" y="56" width="480" height="40" rx="16" fill="var(--surface-subtle)" />
        <rect x="70" y="88" width="480" height="8" fill="var(--surface-subtle)" />
        <circle cx="88" cy="76" r="5" fill="#f97066" />
        <circle cx="106" cy="76" r="5" fill="#fdb022" />
        <circle cx="124" cy="76" r="5" fill="#32d583" />
        <rect x="240" y="68" width="140" height="16" rx="8" fill="var(--surface-raised)" stroke="var(--border)" />
        {/* timer chip */}
        <g filter="url(#l-chip)">
          <rect x="96" y="116" width="96" height="24" rx="12" fill="var(--warning-soft)" />
          <circle cx="110" cy="128" r="4" fill="var(--warning)" />
          <rect x="120" y="124" width="56" height="8" rx="4" fill="var(--warning)" opacity="0.85" />
        </g>
        {/* question number */}
        <rect x="216" y="118" width="70" height="20" rx="10" fill="var(--primary-soft)" />
        <rect x="228" y="125" width="46" height="6" rx="3" fill="var(--primary)" opacity="0.7" />
        {/* question text lines */}
        <rect x="96" y="158" width="380" height="10" rx="5" fill="var(--foreground)" opacity="0.9" />
        <rect x="96" y="178" width="300" height="10" rx="5" fill="var(--foreground)" opacity="0.45" />
        <rect x="96" y="198" width="244" height="10" rx="5" fill="var(--foreground)" opacity="0.3" />
        {/* option rows */}
        {/* A — selected correct */}
        <g filter="url(#l-chip)">
          <rect x="96" y="226" width="428" height="38" rx="10" fill="var(--success-soft)" stroke="var(--success)" strokeOpacity="0.5" />
          <circle cx="116" cy="245" r="11" fill="var(--success)" />
          <text x="112" y="249" fontSize="12" fontWeight="700" fill="#ffffff" fontFamily="inherit">A</text>
          <rect x="138" y="239" width="250" height="7" rx="3.5" fill="var(--foreground)" opacity="0.7" />
          <path d="M500 243 l6 -6 8 10 10 -14" stroke="var(--success)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
        </g>
        {/* B */}
        <rect x="96" y="272" width="428" height="38" rx="10" fill="var(--surface)" stroke="var(--border)" />
        <circle cx="116" cy="291" r="11" fill="var(--surface-subtle)" />
        <text x="112" y="295" fontSize="12" fontWeight="700" fill="var(--muted)" fontFamily="inherit">B</text>
        <rect x="138" y="285" width="180" height="7" rx="3.5" fill="var(--foreground)" opacity="0.5" />
        {/* C */}
        <rect x="96" y="318" width="428" height="38" rx="10" fill="var(--surface)" stroke="var(--border)" />
        <circle cx="116" cy="337" r="11" fill="var(--surface-subtle)" />
        <text x="112" y="341" fontSize="12" fontWeight="700" fill="var(--muted)" fontFamily="inherit">C</text>
        <rect x="138" y="331" width="160" height="7" rx="3.5" fill="var(--foreground)" opacity="0.5" />
        {/* submit */}
        <rect x="456" y="366" width="78" height="28" rx="9" fill="url(#l-grad)" />
        <text x="472" y="385" fontSize="11" fontWeight="600" fill="#ffffff" fontFamily="inherit">Yuborish</text>
        {/* progress */}
        <rect x="96" y="368" width="200" height="6" rx="3" fill="var(--surface-subtle)" />
        <rect x="96" y="368" width="120" height="6" rx="3" fill="url(#l-grad)" />
      </g>
      {/* floating chip: score up */}
      <g filter="url(#l-chip)" className="anim-float">
        <rect x="46" y="300" width="132" height="52" rx="14" fill="var(--surface-raised)" stroke="var(--border-strong)" />
        <rect x="58" y="312" width="34" height="28" rx="8" fill="var(--primary-soft)" />
        <path d="M63 334 l7 -7 5 5 9 -11" stroke="var(--primary)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
        <rect x="100" y="310" width="64" height="8" rx="4" fill="var(--foreground)" opacity="0.7" />
        <rect x="100" y="324" width="44" height="7" rx="3.5" fill="var(--muted)" opacity="0.6" />
      </g>
      {/* floating chip: streak */}
      <g filter="url(#l-chip)" className="anim-float-slow">
        <rect x="482" y="110" width="118" height="48" rx="14" fill="var(--surface-raised)" stroke="var(--border-strong)" />
        <circle cx="504" cy="134" r="12" fill="var(--warning-soft)" stroke="var(--warning)" strokeOpacity="0.4" />
        <path d="M500 138 l4 -10 4 6 4 -3 -5 7" fill="var(--warning)" />
        <rect x="524" y="124" width="60" height="7" rx="3.5" fill="var(--foreground)" opacity="0.6" />
        <rect x="524" y="138" width="42" height="7" rx="3.5" fill="var(--muted)" opacity="0.55" />
      </g>
    </svg>
  );
}

/** Results dashboard: score ring, bar chart, trend line. */
export function AnalyticsMockup({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 620 460"
      role="img"
      aria-hidden
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <Ui />
      <rect x="40" y="34" width="540" height="400" rx="22" fill="url(#l-grad-soft)" />
      <g filter="url(#l-soft)">
        {/* main card */}
        <rect x="78" y="62" width="380" height="290" rx="16" fill="var(--surface)" stroke="var(--border-strong)" />
        <rect x="78" y="62" width="380" height="42" rx="16" fill="var(--surface-subtle)" />
        <rect x="78" y="96" width="380" height="8" fill="var(--surface-subtle)" />
        <circle cx="96" cy="83" r="5" fill="#f97066" />
        <circle cx="114" cy="83" r="5" fill="#fdb022" />
        <circle cx="132" cy="83" r="5" fill="#32d583" />
        <rect x="330" y="74" width="112" height="18" rx="9" fill="var(--surface-raised)" stroke="var(--border)" />
        {/* bar chart */}
        <rect x="104" y="122" width="130" height="16" rx="8" fill="var(--foreground)" opacity="0.15" />
        {[0, 1, 2, 3, 4, 5, 6, 7].map((i) => {
          const h = [26, 40, 34, 54, 46, 62, 74, 88][i];
          const x = 108 + i * 40;
          return (
            <rect key={i} x={x} y={278 - h} width="24" height={h} rx="6" fill="url(#l-grad)" opacity={0.45 + i * 0.07} />
          );
        })}
        {/* trend line */}
        <path
          d="M104 236 L144 222 L184 230 L224 198 L264 206 L304 168 L344 178 L384 140"
          stroke="var(--info)"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />
        <path d="M384 140 l-6 -4 14 -8 z" fill="var(--info)" />
        <circle cx="104" cy="236" r="5" fill="var(--info)" />
        <circle cx="384" cy="140" r="5" fill="var(--info)" />
        {/* legend */}
        <rect x="108" y="318" width="10" height="10" rx="3" fill="url(#l-grad)" />
        <rect x="124" y="320" width="56" height="6" rx="3" fill="var(--muted)" opacity="0.6" />
        <circle cx="212" cy="323" r="5" fill="var(--info)" />
        <rect x="224" y="320" width="56" height="6" rx="3" fill="var(--muted)" opacity="0.6" />
      </g>
      {/* side card — subject breakdown */}
      <g filter="url(#l-chip)">
        <rect x="486" y="120" width="126" height="150" rx="14" fill="var(--surface-raised)" stroke="var(--border-strong)" />
        <rect x="500" y="136" width="98" height="8" rx="4" fill="var(--foreground)" opacity="0.7" />
        {[0, 1, 2, 3].map((i) => {
          const w = [74, 60, 82, 50][i];
          const tone = ["var(--success)", "var(--primary)", "var(--warning)", "var(--subtle)"][i];
          return (
            <g key={i}>
              <rect x="500" y={158 + i * 26} width={w} height="9" rx="4.5" fill={tone} opacity="0.85" />
              <rect x="586" y={158.5 + i * 26} width="18" height="7" rx="3.5" fill="var(--muted)" opacity="0.4" />
            </g>
          );
        })}
      </g>
      {/* score ring card */}
      <g filter="url(#l-chip)" className="anim-float">
        <rect x="500" y="300" width="110" height="118" rx="14" fill="var(--surface-raised)" stroke="var(--border-strong)" />
        <circle cx="555" cy="340" r="30" stroke="var(--surface-subtle)" strokeWidth="9" />
        <circle cx="555" cy="340" r="30" stroke="var(--success)" strokeWidth="9" strokeDasharray="141 38" strokeLinecap="round" transform="rotate(-90 555 340)" />
        <text x="555" y="346" textAnchor="middle" fontSize="16" fontWeight="700" fill="var(--foreground)" fontFamily="inherit">140</text>
        <rect x="512" y="384" width="86" height="7" rx="3.5" fill="var(--muted)" opacity="0.55" />
      </g>
    </svg>
  );
}

/** Study / mistake-review topics with mastery bars. */
export function StudyMockup({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 620 460"
      role="img"
      aria-hidden
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <Ui />
      <rect x="40" y="44" width="540" height="380" rx="22" fill="url(#l-grad-soft)" />
      <g filter="url(#l-soft)">
        <rect x="92" y="72" width="436" height="320" rx="16" fill="var(--surface)" stroke="var(--border-strong)" />
        {/* header */}
        <rect x="92" y="72" width="436" height="48" rx="16" fill="var(--surface-subtle)" />
        <rect x="92" y="112" width="436" height="8" fill="var(--surface-subtle)" />
        <rect x="112" y="88" width="120" height="10" rx="5" fill="var(--foreground)" opacity="0.75" />
        <rect x="392" y="88" width="112" height="20" rx="10" fill="var(--primary-soft)" />
        <rect x="402" y="95" width="90" height="7" rx="3.5" fill="var(--primary)" opacity="0.7" />
        {/* topic rows with mastery bars */}
        {[
          { label: 156, bar: 96, w: [186, 110], tone: "var(--success)", tag: 0 },
          { label: 156, bar: 78, w: [188, 88], tone: "var(--primary)", tag: 1 },
          { label: 156, bar: 60, w: [182, 66], tone: "var(--warning)", tag: 2 },
          { label: 156, bar: 42, w: [184, 48], tone: "var(--danger)", tag: 3 },
        ].map((row, i) => {
          const top = 140 + i * 62;
          return (
            <g key={i}>
              <circle cx="122" cy={top + 14} r="12" fill="var(--surface-subtle)" stroke="var(--border)" />
              <rect x="116" y={top + 10} width="12" height="8" rx="4" fill={row.tone} opacity="0.8" />
              <rect x="142" y={top + 11} width={row.label / 2} height="7" rx="3.5" fill="var(--foreground)" opacity="0.7" />
              <rect x="142" y={top + 23} width="92" height="6" rx="3" fill="var(--muted)" opacity="0.4" />
              <rect x="150" y={top + 40} width="292" height="8" rx="4" fill="var(--surface-subtle)" />
              <rect x="150" y={top + 40} width={row.bar} height="8" rx="4" fill={row.tone} opacity="0.9" />
              <text x="452" y={top + 17} fontSize="11" fontWeight="600" fill={row.tone} fontFamily="inherit">{Math.round((row.bar / 96) * 100)}%</text>
              {/* tag chip */}
              <rect x="420" y={top + 26} width="46" height="16" rx="8" fill={["var(--success-soft)", "var(--primary-soft)", "var(--warning-soft)", "var(--danger-soft)"][row.tag]} />
              <rect x="426" y={top + 32} width="34" height="5" rx="2.5" fill={row.tone} opacity="0.75" />
            </g>
          );
        })}
        {/* footer CTA */}
        <rect x="150" y="350" width="320" height="26" rx="13" fill="url(#l-grad)" />
        <rect x="242" y="359" width="136" height="7" rx="3.5" fill="#ffffff" opacity="0.9" />
      </g>
      {/* floating chip: + questions solved */}
      <g filter="url(#l-chip)" className="anim-float">
        <rect x="56" y="230" width="128" height="52" rx="14" fill="var(--surface-raised)" stroke="var(--border-strong)" />
        <circle cx="78" cy="256" r="12" fill="var(--success-soft)" stroke="var(--success)" strokeOpacity="0.45" />
        <path d="M72 256 l4 4 8 -9" stroke="var(--success)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
        <rect x="98" y="246" width="70" height="7" rx="3.5" fill="var(--foreground)" opacity="0.65" />
        <rect x="98" y="259" width="48" height="7" rx="3.5" fill="var(--muted)" opacity="0.55" />
      </g>
      {/* floating chip: streak book */}
      <g filter="url(#l-chip)" className="anim-float-slow">
        <rect x="492" y="180" width="110" height="66" rx="14" fill="var(--surface-raised)" stroke="var(--border-strong)" />
        <rect x="508" y="194" width="78" height="8" rx="4" fill="var(--foreground)" opacity="0.7" />
        {[0, 1, 2, 3, 4, 5, 6].map((i) => (
          <rect key={i} x={508 + i * 12} y={210 + (i % 2) * 6} width="8" height={14 + (i % 3) * 6} rx="3" fill="url(#l-grad)" opacity={0.5 + (i % 4) * 0.12} />
        ))}
        <rect x="508" y="236" width="60" height="6" rx="3" fill="var(--muted)" opacity="0.5" />
      </g>
    </svg>
  );
}