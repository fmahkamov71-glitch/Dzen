import React, { useMemo } from "react";
import { AbsoluteFill, interpolate, random, useCurrentFrame } from "remotion";
import { H, W } from "./theme";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/* ───────────────────────── 1. SUPERHERO ───────────────────────── */
export const HeroScene: React.FC = () => {
  const f = useCurrentFrame();
  const layers = useMemo(() => {
    const make = (seed: string, minH: number, maxH: number, base: number, win: boolean) => {
      const out: { x: number; w: number; h: number; wins: [number, number][] }[] = [];
      let x = -40;
      let i = 0;
      while (x < W + 60) {
        const w = 60 + random(`${seed}w${i}`) * 90;
        const h = minH + random(`${seed}h${i}`) * (maxH - minH);
        const wins: [number, number][] = [];
        if (win) {
          for (let wy = base - h + 24; wy < base - 16; wy += 26) {
            for (let wx = x + 10; wx < x + w - 14; wx += 20) {
              if (random(`${seed}${i}${wx}${wy}`) > 0.72) wins.push([wx, wy]);
            }
          }
        }
        out.push({ x, w, h, wins });
        x += w + 2;
        i++;
      }
      return out;
    };
    return [
      { b: make("far", 160, 420, 1230, false), c: "#1a2447", base: 1230, win: false },
      { b: make("mid", 220, 640, 1330, true), c: "#0c1228", base: 1330, win: true },
      { b: make("near", 280, 820, 1440, true), c: "#060912", base: 1440, win: true },
    ];
  }, []);

  const capePts = (side: "top" | "bot") =>
    new Array(9).fill(0).map((_, i) => {
      const k = i / 8;
      const wob = Math.sin(f * 0.28 + i * 0.7) * (6 + i * 4);
      const x = 506 - k * 330;
      const y = side === "top" ? 1258 + k * 70 + wob : 1470 + k * 40 + wob * 1.2;
      return [x, y] as const;
    });
  const top = capePts("top");
  const bot = capePts("bot").reverse();
  const cape =
    "M" + [...top, ...bot].map(([x, y]) => `${x.toFixed(1)} ${y.toFixed(1)}`).join(" L") + " Z";

  const sp = interpolate(f, [14, 34], [-0.2, 1.2], clamp);
  const streakA = interpolate(f, [14, 22, 34], [0, 1, 0], clamp);

  return (
    <AbsoluteFill style={{ background: "#03050d" }}>
      <svg width={W} height={H}>
        <defs>
          <linearGradient id="h-sky" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#03050f" />
            <stop offset="0.45" stopColor="#0d1a3c" />
            <stop offset="0.68" stopColor="#7a4a3c" />
            <stop offset="0.76" stopColor="#e39b55" />
          </linearGradient>
          <radialGradient id="h-glow" cx="0.62" cy="0.7" r="0.5">
            <stop offset="0" stopColor="#ffd9a0" stopOpacity="0.8" />
            <stop offset="1" stopColor="#ffd9a0" stopOpacity="0" />
          </radialGradient>
          <linearGradient id="h-streak" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0" stopColor="#9fd8ff" stopOpacity="0" />
            <stop offset="1" stopColor="#ffffff" />
          </linearGradient>
          <filter id="h-blur"><feGaussianBlur stdDeviation="6" /></filter>
        </defs>
        <rect width={W} height={H} fill="url(#h-sky)" />
        <rect width={W} height={H} fill="url(#h-glow)" />
        {layers.map((L, li) => (
          <g key={li}>
            {L.b.map((b, i) => (
              <g key={i}>
                <rect x={b.x} y={L.base - b.h} width={b.w} height={b.h + 600} fill={L.c} />
                {b.wins.map(([wx, wy], k) => (
                  <rect
                    key={k}
                    x={wx}
                    y={wy}
                    width={8}
                    height={11}
                    fill="#ffd28a"
                    opacity={0.35 + 0.5 * random(`fl${li}${i}${k}${Math.floor(f / 9)}`)}
                  />
                ))}
              </g>
            ))}
          </g>
        ))}
        {/* distant flyer streak */}
        <g opacity={streakA}>
          <line
            x1={-200 + sp * 1500 - 520}
            y1={640 - sp * 220 + 150}
            x2={-200 + sp * 1500}
            y2={640 - sp * 220}
            stroke="url(#h-streak)"
            strokeWidth={5}
            strokeLinecap="round"
          />
          <circle cx={-200 + sp * 1500} cy={640 - sp * 220} r={22} fill="#fff" filter="url(#h-blur)" />
        </g>
        {/* rooftop + hero silhouette, rim-lit from the city glow */}
        <polygon points={`0,1560 ${W},1500 ${W},${H} 0,${H}`} fill="#020308" />
        <rect x={0} y={1552} width={W} height={4} fill="#e39b55" opacity={0.35} />
        <g transform="translate(540 1560) scale(1.35) translate(-540 -1560)">
          <g fill="#04060c" stroke="#ffcf94" strokeWidth={2} strokeOpacity={0.75}>
            <path d={cape} />
            <path d="M518 1405 h22 v158 h-22z M544 1405 h22 v158 h-22z" />
            <path d="M494 1250 L586 1250 L562 1410 L518 1410 Z" />
            <path d="M494 1256 L462 1350 L482 1358 L512 1280 Z M586 1256 L618 1350 L598 1358 L568 1280 Z" />
            <circle cx={540} cy={1218} r={25} />
          </g>
        </g>
      </svg>
    </AbsoluteFill>
  );
};

/* ───────────────────────── 2. MARS ───────────────────────── */
export const MarsScene: React.FC = () => {
  const f = useCurrentFrame();
  const dune = (amp: number, base: number, freq: number, ph: number) => {
    let d = `M0 ${H} L0 ${base}`;
    for (let x = 0; x <= W; x += 20) {
      d += ` L${x} ${base + Math.sin(x * freq + ph) * amp + Math.sin(x * freq * 2.3 + ph * 2) * amp * 0.4}`;
    }
    return d + ` L${W} ${H} Z`;
  };
  const streaks = useMemo(
    () =>
      new Array(46).fill(0).map((_, i) => ({
        y: 900 + random(`my${i}`) * 900,
        x: random(`mx${i}`) * W,
        l: 80 + random(`ml${i}`) * 260,
        v: 260 + random(`mv${i}`) * 520,
        a: 0.08 + random(`ma${i}`) * 0.25,
      })),
    [],
  );
  const t = f / 30;
  return (
    <AbsoluteFill style={{ background: "#2a0f08" }}>
      <svg width={W} height={H}>
        <defs>
          <linearGradient id="m-sky" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#1d0a08" />
            <stop offset="0.35" stopColor="#6e2b16" />
            <stop offset="0.52" stopColor="#e8a15c" />
          </linearGradient>
          <radialGradient id="m-sun">
            <stop offset="0" stopColor="#fff2d6" />
            <stop offset="0.25" stopColor="#ffd199" stopOpacity="0.9" />
            <stop offset="1" stopColor="#ff9a4d" stopOpacity="0" />
          </radialGradient>
          <linearGradient id="m-visor" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="#ffd9a0" />
            <stop offset="1" stopColor="#3b1608" />
          </linearGradient>
        </defs>
        <rect width={W} height={H} fill="url(#m-sky)" />
        <circle cx={540} cy={930} r={760} fill="url(#m-sun)" opacity={0.85} />
        <circle cx={540} cy={930} r={120} fill="#fff4de" />
        <path d={dune(26, 980, 0.006, 0.5)} fill="#7b361b" />
        <path d={dune(34, 1090, 0.005, 2.2)} fill="#4a1d0e" />
        <path d={dune(46, 1260, 0.004, 4.1)} fill="#2a0f08" />
        {/* astronaut, long shadow toward camera */}
        <polygon points="522,1400 558,1400 640,1920 360,1920" fill="#120503" opacity={0.55} />
        <g transform="translate(540 1372)">
          <rect x={-46} y={-130} width={30} height={92} rx={8} fill="#1b0b06" />
          <rect x={-30} y={-132} width={60} height={86} rx={14} fill="#c9b7a6" />
          <rect x={-24} y={-48} width={20} height={50} rx={6} fill="#b19f8f" />
          <rect x={4} y={-48} width={20} height={50} rx={6} fill="#b19f8f" />
          <circle cx={0} cy={-166} r={34} fill="#d9cabb" />
          <ellipse cx={4} cy={-166} rx={24} ry={21} fill="url(#m-visor)" />
          <path d="M30 -140 L30 -50" stroke="#ffd9a0" strokeWidth={3} opacity={0.8} />
        </g>
        {streaks.map((s, i) => {
          const x = (((s.x - s.v * t) % (W + 400)) + W + 400) % (W + 400) - 200;
          return (
            <line key={i} x1={x} y1={s.y} x2={x + s.l} y2={s.y - 4} stroke="#ffc58a" strokeWidth={2} opacity={s.a} />
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};

/* ───────────────────── 3. A WORLD THAT SHOULD NOT EXIST ───────────────────── */
export const WorldScene: React.FC = () => {
  const f = useCurrentFrame();
  const mono = [
    { x: 150, w: 70, h: 520, y: 640, ph: 0 },
    { x: 330, w: 46, h: 300, y: 560, ph: 1.4 },
    { x: 720, w: 90, h: 640, y: 560, ph: 2.1 },
    { x: 900, w: 54, h: 360, y: 700, ph: 0.7 },
  ];
  const HZ = 1010;
  const Mono = ({ m }: { m: (typeof mono)[number] }) => {
    const bob = Math.sin(f * 0.06 + m.ph) * 14;
    return (
      <g transform={`translate(0 ${bob})`}>
        <path
          d={`M${m.x} ${m.y} L${m.x + m.w} ${m.y + 20} L${m.x + m.w} ${m.y + m.h} L${m.x} ${m.y + m.h - 20} Z`}
          fill="#04141c"
          stroke="#5fd4ff"
          strokeWidth={2}
          strokeOpacity={0.8}
        />
      </g>
    );
  };
  return (
    <AbsoluteFill style={{ background: "#02070c" }}>
      <svg width={W} height={H}>
        <defs>
          <linearGradient id="w-sky" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#02070d" />
            <stop offset="0.45" stopColor="#0a2a3a" />
            <stop offset="0.53" stopColor="#52d2cc" />
          </linearGradient>
          <linearGradient id="w-water" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#2a8f93" />
            <stop offset="0.15" stopColor="#06222c" />
            <stop offset="1" stopColor="#010609" />
          </linearGradient>
          <radialGradient id="w-moon" cx="0.4" cy="0.35">
            <stop offset="0" stopColor="#f2fbff" />
            <stop offset="1" stopColor="#6d95a8" />
          </radialGradient>
          <radialGradient id="w-halo">
            <stop offset="0" stopColor="#9be8ff" stopOpacity="0.45" />
            <stop offset="1" stopColor="#9be8ff" stopOpacity="0" />
          </radialGradient>
        </defs>
        <rect width={W} height={HZ} fill="url(#w-sky)" />
        <circle cx={730} cy={420} r={420} fill="url(#w-halo)" />
        <circle cx={730} cy={420} r={150} fill="url(#w-moon)" />
        <circle cx={310} cy={640} r={42} fill="#cfeaf2" opacity={0.9} />
        {/* impossible geometry: tilted rings around the moon */}
        <g transform={`translate(730 420) rotate(${-24 + f * 0.25})`}>
          <ellipse rx={290} ry={64} fill="none" stroke="#bff3ff" strokeWidth={2} opacity={0.7} />
          <ellipse rx={340} ry={92} fill="none" stroke="#bff3ff" strokeWidth={1} opacity={0.4} />
        </g>
        {mono.map((m, i) => <Mono key={i} m={m} />)}
        {/* mirror world */}
        <rect y={HZ} width={W} height={H - HZ} fill="url(#w-water)" />
        <g transform={`translate(0 ${HZ * 2}) scale(1 -1)`} opacity={0.35}>
          {mono.map((m, i) => <Mono key={i} m={m} />)}
          <circle cx={730} cy={420} r={150} fill="url(#w-moon)" />
        </g>
        {new Array(16).fill(0).map((_, i) => (
          <rect
            key={i}
            x={W / 2 - 360 + random(`wl${i}`) * 100 + Math.sin(f * 0.1 + i) * 30}
            y={HZ + 14 + i * 36}
            width={200 + random(`wm${i}`) * 300}
            height={2}
            fill="#9be8ff"
            opacity={0.12 + 0.2 * random(`wo${i}`)}
          />
        ))}
        {/* lone figure on the water */}
        <g transform={`translate(540 ${HZ + 150})`}>
          <ellipse cx={0} cy={4} rx={40} ry={9} fill="#9be8ff" opacity={0.25} />
          <rect x={-10} y={-96} width={20} height={96} rx={8} fill="#02060a" />
          <circle cx={0} cy={-112} r={13} fill="#02060a" />
        </g>
      </svg>
    </AbsoluteFill>
  );
};

/* ───────────────────── 4. HUMANITY DISAPPEARED ───────────────────── */
export const EmptyCityScene: React.FC<{ duration: number }> = ({ duration }) => {
  const f = useCurrentFrame();
  const F = 760;
  const VPX = 540;
  const VPY = 880;
  const cam = interpolate(f, [0, duration], [0, 7.5]);
  const P = (X: number, Y: number, z: number): [number, number] => [VPX + (F * X) / z, VPY + (F * Y) / z];
  const lit = interpolate(f, [0, duration * 0.9], [0.55, 0.05], clamp);

  const els: React.ReactNode[] = [];
  // buildings/ facades far → near
  for (let s = 0; s < 14; s++) {
    for (const side of [-1, 1]) {
      const z0 = s * 3 + 1.2 - (cam % 3) - 0 + 0;
      const zr = z0 + 0; // slice start
      const zz0 = Math.max(0.7, zr);
      const zz1 = zr + 3;
      if (zz1 < 0.7) continue;
      const X = side * 4.2;
      const a = P(X, -16, zz0), b = P(X, -16, zz1), c = P(X, 1.6, zz1), d = P(X, 1.6, zz0);
      const shade = Math.max(0, 0.9 - zz0 / 45);
      const idx = s + Math.floor(cam / 3);
      els.push(
        <polygon
          key={`f${side}${s}`}
          points={`${a} ${b} ${c} ${d}`}
          fill={`rgb(${10 + 14 * shade},${14 + 18 * shade},${28 + 26 * shade})`}
        />,
      );
      for (let wy = -14; wy < 0; wy += 2.4) {
        for (let wz = 0.6; wz < 2.6; wz += 1) {
          const on = random(`win${side}${idx}${wy}${wz}`) < lit;
          const flick = on && random(`fk${idx}${wy}${Math.floor(f / 4)}`) > 0.05;
          if (!flick) continue;
          const zA = zr + wz, zB = zA + 0.55;
          if (zA < 0.8) continue;
          const w1 = P(X, wy, zA), w2 = P(X, wy, zB), w3 = P(X, wy + 1.2, zB), w4 = P(X, wy + 1.2, zA);
          els.push(<polygon key={`w${side}${s}${wy}${wz}`} points={`${w1} ${w2} ${w3} ${w4}`} fill="#ffcf8a" opacity={0.85} />);
        }
      }
      // street lamp
      const lz = zr + 1.5;
      if (lz > 0.9) {
        const [lx, ly] = P(side * 3.3, -4.2, lz);
        const [bx, by] = P(side * 3.3, 1.6, lz);
        const k = F / lz;
        const lampOn = f < duration * 0.55 + side * 4 + (idx % 3) * 3;
        els.push(
          <g key={`l${side}${s}`}>
            <line x1={bx} y1={by} x2={lx} y2={ly} stroke="#0a0f1a" strokeWidth={Math.max(2, 0.16 * k)} />
            {lampOn && <circle cx={lx} cy={ly} r={Math.min(46, Math.max(6, 1.2 * k))} fill="#ffd9a0" opacity={0.55} />}
            {lampOn && <circle cx={lx} cy={ly} r={Math.min(10, Math.max(3, 0.18 * k))} fill="#fff" />}
          </g>,
        );
      }
    }
  }
  const roadL = P(-3.2, 1.6, 0.7), roadR = P(3.2, 1.6, 0.7), roadFL = P(-3.2, 1.6, 60), roadFR = P(3.2, 1.6, 60);

  return (
    <AbsoluteFill style={{ background: "#05070f" }}>
      <svg width={W} height={H}>
        <defs>
          <linearGradient id="c-sky" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#03050c" />
            <stop offset="0.45" stopColor="#101a33" />
            <stop offset="0.5" stopColor="#5b4a58" />
          </linearGradient>
          <linearGradient id="c-road" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#2a2630" />
            <stop offset="1" stopColor="#07080d" />
          </linearGradient>
          <radialGradient id="c-fog" cx="0.5" cy="0.46" r="0.35">
            <stop offset="0" stopColor="#a9a0b5" stopOpacity="0.75" />
            <stop offset="1" stopColor="#a9a0b5" stopOpacity="0" />
          </radialGradient>
        </defs>
        <rect width={W} height={H} fill="url(#c-sky)" />
        <polygon points={`${roadFL} ${roadFR} ${roadR} ${roadL} ${W + 400},${H + 100} -400,${H + 100}`} fill="url(#c-road)" />
        {/* lane dashes */}
        {new Array(14).fill(0).map((_, i) => {
          const z = i * 3 + 1.2 - (cam % 3) + 0.5;
          if (z < 0.8) return null;
          const a = P(-0.08, 1.6, z), b = P(0.08, 1.6, z + 1.2);
          return <polygon key={i} points={`${a} ${P(0.08, 1.6, z)} ${b} ${P(-0.08, 1.6, z + 1.2)}`} fill="#caa86a" opacity={0.6} />;
        })}
        {els}
        <rect width={W} height={H} fill="url(#c-fog)" />
      </svg>
    </AbsoluteFill>
  );
};

/* ───────────────────── 5. DISCOVER SOMETHING THAT CHANGES REALITY ───────────────────── */
export const TearScene: React.FC<{ duration: number }> = ({ duration }) => {
  const f = useCurrentFrame();
  const open = interpolate(f, [4, duration - 6], [0, 1], clamp);
  const flash = interpolate(f, [duration - 8, duration - 1], [0, 1], clamp);
  const jag = useMemo(
    () => new Array(15).fill(0).map((_, i) => ({ dx: (random(`tj${i}`) - 0.5) * 70, dw: 0.6 + random(`tw${i}`) })),
    [],
  );
  const top = 420, bottom = 1380, cx = 540;
  const edge = (side: 1 | -1) =>
    jag.map((j, i) => {
      const k = i / (jag.length - 1);
      const w = Math.sin(Math.PI * k) ** 0.7 * (5 + open * 48) * j.dw;
      return `${(cx + j.dx * (0.4 + open) + side * w).toFixed(1)} ${(top + k * (bottom - top)).toFixed(1)}`;
    });
  const d = "M" + edge(-1).join(" L") + " L" + edge(1).reverse().join(" L") + " Z";
  const rays = interpolate(open, [0, 1], [0.2, 1]);
  return (
    <AbsoluteFill style={{ background: "#03040a" }}>
      <svg width={W} height={H}>
        <defs>
          <radialGradient id="t-bg" cx="0.5" cy="0.5" r="0.7">
            <stop offset="0" stopColor="#1a2335" />
            <stop offset="1" stopColor="#03040a" />
          </radialGradient>
          <linearGradient id="t-core" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#fff" stopOpacity="0.4" />
            <stop offset="0.5" stopColor="#fffaf0" />
            <stop offset="1" stopColor="#fff" stopOpacity="0.4" />
          </linearGradient>
          <filter id="t-b1"><feGaussianBlur stdDeviation="24" /></filter>
          <filter id="t-b2"><feGaussianBlur stdDeviation="8" /></filter>
          <radialGradient id="t-ray" cx="0.5" cy="0.5" r="0.5">
            <stop offset="0" stopColor="#ffe6b0" stopOpacity="0.9" />
            <stop offset="1" stopColor="#ffe6b0" stopOpacity="0" />
          </radialGradient>
        </defs>
        <rect width={W} height={H} fill="url(#t-bg)" />
        {/* god rays */}
        <g transform={`translate(${cx} 900) rotate(${f * 0.5})`} opacity={rays * 0.55}>
          {new Array(14).fill(0).map((_, i) => (
            <polygon key={i} points={`0,0 ${-26 - (i % 3) * 14},-1500 ${26 + (i % 3) * 14},-1500`} fill="url(#t-ray)" transform={`rotate(${i * (360 / 14)})`} />
          ))}
        </g>
        {/* floor reflection */}
        <ellipse cx={cx} cy={1400} rx={120 + open * 300} ry={26 + open * 40} fill="#ffe6b0" opacity={0.35 * open} filter="url(#t-b2)" />
        <path d={d} fill="#ffcf8a" opacity={0.9} filter="url(#t-b1)" />
        <path d={d} fill="#ffe6b0" opacity={0.9} filter="url(#t-b2)" />
        <path d={d} fill="url(#t-core)" />
        {/* shards leaving the tear */}
        {new Array(22).fill(0).map((_, i) => {
          const a = random(`sa${i}`) * 6.28;
          const r = (30 + random(`sr${i}`) * 520) * open * (0.4 + (f % 1000) / 1000);
          const x = cx + Math.cos(a) * r * 0.9;
          const y = 900 + Math.sin(a) * r * 1.3;
          const s = 4 + random(`ss${i}`) * 12;
          return <rect key={i} x={x} y={y} width={s} height={s * 1.8} fill="#fff1d1" opacity={0.7 * (1 - r / 700)} transform={`rotate(${a * 57 + f * 4} ${x} ${y})`} />;
        })}
        {/* the witness */}
        <g transform="translate(540 1560)">
          <path d="M-34 0 L-26 -170 Q0 -190 26 -170 L34 0 Z" fill="#010205" />
          <circle cx={0} cy={-205} r={24} fill="#010205" />
          <path d="M-34 0 L-26 -170" stroke="#ffe6b0" strokeWidth={2.5} opacity={0.6 * open} />
          <path d="M34 0 L26 -170" stroke="#ffe6b0" strokeWidth={2.5} opacity={0.6 * open} />
        </g>
      </svg>
      <AbsoluteFill style={{ background: "#fff6df", opacity: flash }} />
    </AbsoluteFill>
  );
};
