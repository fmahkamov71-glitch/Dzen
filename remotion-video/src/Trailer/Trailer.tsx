import React from "react";
import {
  AbsoluteFill,
  Easing,
  interpolate,
  OffthreadVideo,
  Sequence,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { Atmosphere } from "./Atmosphere";
import { Camera } from "./Camera";
import { Emblem } from "./Emblem";
import {
  EmptyCityScene,
  HeroScene,
  MarsScene,
  TearScene,
  WorldScene,
} from "./Scenes";
import { C, H, sans, serifCaps, T, W } from "./theme";
import { GoldCaps, Kicker, Words } from "./Type";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const easeOut = Easing.out(Easing.cubic);

export type TrailerProps = {
  // Optional photoreal footage per shot (files inside /public). null = built-in procedural shot.
  clips: (string | null)[];
};

const Scrim: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        "linear-gradient(180deg, rgba(0,0,0,0) 52%, rgba(0,0,0,0.78) 100%)",
    }}
  />
);

// One "What if" shot: moving camera, cut flash, lower-third question.
const Shot: React.FC<{
  duration: number;
  clip: string | null;
  line: string;
  accent?: string;
  cam: React.ComponentProps<typeof Camera>;
  children: React.ReactNode;
}> = ({ duration, clip, line, accent, cam, children }) => {
  const f = useCurrentFrame();
  const flash = interpolate(f, [0, 7], [0.45, 0], clamp);
  const out = interpolate(f, [duration - 2, duration], [1, 0.0], clamp);
  return (
    <AbsoluteFill style={{ opacity: Math.max(out, 0.0001) }}>
      <Camera {...cam} duration={duration}>
        {clip ? (
          <OffthreadVideo
            src={staticFile(clip)}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        ) : (
          // lift the subject above the lower-third
          <AbsoluteFill style={{ transform: "translateY(-200px)" }}>{children}</AbsoluteFill>
        )}
      </Camera>
      <Scrim />
      <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 250 }}>
        <div style={{ width: 900, display: "flex", flexDirection: "column", gap: 26, alignItems: "center" }}>
          <Kicker text="WHAT IF" delay={4} />
          <Words text={line} size={104} delay={8} stagger={5} accent={accent} />
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "#e8f1ff", opacity: flash }} />
    </AbsoluteFill>
  );
};

/* ── HOOK ── */
const Hook: React.FC = () => {
  const f = useCurrentFrame();
  const beam = interpolate(f, [0, 40], [0, 1], { ...clamp, easing: easeOut });
  const zoom = interpolate(f, [0, 60], [1, 1.14], clamp);
  const dots = [24, 32, 40].map((s) => interpolate(f, [s, s + 6], [0, 1], clamp));
  const q = interpolate(f, [46, 52], [0, 1], clamp);
  const out = interpolate(f, [54, 60], [1, 0], clamp);
  return (
    <AbsoluteFill style={{ background: C.black, opacity: out }}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse 60% 38% at 50% 100%, rgba(120,170,255,${0.5 * beam}), rgba(0,0,0,0) 70%)`,
        }}
      />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", transform: `scale(${zoom})` }}>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
          <GoldCaps text="WHAT IF" size={170} spacingFrom={0.9} spacingTo={0.12} duration={36} sweepAt={20} weight={400} />
          <div style={{ fontFamily: sans, fontWeight: 300, fontSize: 150, color: C.ice, letterSpacing: "0.12em", display: "flex", height: 170 }}>
            {dots.map((o, i) => (
              <span key={i} style={{ opacity: o, textShadow: "0 0 30px rgba(160,200,255,.9)" }}>.</span>
            ))}
            <span
              style={{
                opacity: q,
                transform: `scale(${1 + (1 - q) * 0.6})`,
                textShadow: "0 0 50px rgba(190,220,255,1)",
                marginLeft: 8,
              }}
            >
              ?
            </span>
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ── "Every impossible question has a story." ── */
const Tagline: React.FC = () => {
  const f = useCurrentFrame();
  const line = interpolate(f, [8, 40], [0, 1], { ...clamp, easing: easeOut });
  const glow = interpolate(f, [20, 55], [0, 1], clamp);
  const out = interpolate(f, [52, 60], [1, 0], clamp);
  return (
    <AbsoluteFill style={{ background: C.black, opacity: out }}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse 70% 30% at 50% 52%, rgba(232,194,122,${0.28 * glow}), rgba(0,0,0,0) 70%)`,
        }}
      />
      <Camera duration={60} zoom={[1, 1.1]} shake={2} seed="tag">
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          <div style={{ width: 880, display: "flex", flexDirection: "column", alignItems: "center", gap: 44 }}>
            <Words text="Every impossible question" size={92} delay={0} stagger={5} />
            <div style={{ width: 760 * line, height: 2, background: `linear-gradient(90deg, transparent, ${C.gold}, transparent)`, boxShadow: `0 0 24px ${C.gold}` }} />
            <Words text="has a story." size={128} delay={22} stagger={7} accent="story" />
          </div>
        </AbsoluteFill>
      </Camera>
    </AbsoluteFill>
  );
};

/* ── VELORIAN CHRONICLES + pillars ── */
const Brand: React.FC = () => {
  const f = useCurrentFrame();
  const draw = interpolate(f, [0, 40], [0, 1], { ...clamp, easing: easeOut });
  const flare = interpolate(f, [8, 20, 40], [0, 1, 0.25], clamp);
  const pillars = ["WHAT IF STORIES", "IMPOSSIBLE WORLDS", "UNEXPECTED CONSEQUENCES"];
  const out = interpolate(f, [82, 90], [1, 0], clamp);
  return (
    <AbsoluteFill style={{ background: C.black, opacity: out }}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse 80% 40% at 50% 44%, rgba(232,194,122,${0.34 * draw}), rgba(0,0,0,0) 70%)`,
        }}
      />
      {/* anamorphic flare */}
      <div
        style={{
          position: "absolute",
          left: 0,
          width: W,
          top: 800,
          height: 4,
          background: "linear-gradient(90deg, transparent, #fff3d1, transparent)",
          opacity: flare,
          transform: `scaleX(${0.2 + flare * 1.2})`,
          boxShadow: "0 0 60px 10px rgba(255,220,160,.7)",
        }}
      />
      <Camera duration={90} zoom={[1, 1.07]} shake={2} seed="brand">
        <AbsoluteFill style={{ alignItems: "center", paddingTop: 330 }}>
          <Emblem size={420} draw={draw} frame={f} />
          <div style={{ marginTop: 70, display: "flex", flexDirection: "column", alignItems: "center", gap: 14 }}>
            <GoldCaps text="VELORIAN" size={132} spacingFrom={0.7} spacingTo={0.1} delay={6} duration={42} sweepAt={18} />
            <GoldCaps text="CHRONICLES" size={84} spacingFrom={0.9} spacingTo={0.26} delay={14} duration={42} sweepAt={26} weight={400} />
          </div>
          <div style={{ marginTop: 90, display: "flex", flexDirection: "column", alignItems: "center", gap: 30 }}>
            {pillars.map((p, i) => {
              const s = 40 + i * 14;
              const o = interpolate(f, [s, s + 14], [0, 1], { ...clamp, easing: easeOut });
              return (
                <div
                  key={p}
                  style={{
                    fontFamily: sans,
                    fontWeight: 300,
                    fontSize: 34,
                    letterSpacing: "0.42em",
                    paddingLeft: "0.42em",
                    color: C.ice,
                    opacity: o,
                    transform: `translateY(${(1 - o) * 18}px)`,
                    textShadow: "0 0 24px rgba(160,200,255,.4)",
                  }}
                >
                  {p}
                </div>
              );
            })}
          </div>
        </AbsoluteFill>
      </Camera>
    </AbsoluteFill>
  );
};

/* ── "Your next story is waiting." — a door of light opens ── */
const Waiting: React.FC = () => {
  const f = useCurrentFrame();
  const open = interpolate(f, [0, 45], [0, 1], { ...clamp, easing: Easing.in(Easing.cubic) });
  const slitW = 6 + open * open * 760;
  const out = interpolate(f, [38, 45], [1, 0], clamp);
  return (
    <AbsoluteFill style={{ background: C.black }}>
      <div
        style={{
          position: "absolute",
          left: W / 2 - slitW * 1.6,
          width: slitW * 3.2,
          top: -100,
          height: H + 200,
          background: `radial-gradient(ellipse 50% 50% at 50% 50%, rgba(255,205,130,${0.55 + open * 0.3}), rgba(255,205,130,0) 70%)`,
          filter: "blur(30px)",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: W / 2 - slitW / 2,
          width: slitW,
          top: 0,
          height: H,
          background: "linear-gradient(180deg, rgba(255,243,209,0.3), #fff3d1 50%, rgba(255,243,209,0.3))",
          filter: "blur(2px)",
        }}
      />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", opacity: out, mixBlendMode: "normal" }}>
        <div style={{ width: 880, display: "flex", flexDirection: "column", alignItems: "center", gap: 6 }}>
          <Words text="Your next story is" size={86} delay={0} stagger={4} color="#fff" />
          <Words text="waiting." size={150} delay={14} stagger={6} accent="waiting" />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* ── Final 3 seconds: brand + CTA ── */
const CTA: React.FC = () => {
  const f = useCurrentFrame();
  const bloom = interpolate(f, [0, 3, 22], [1, 1, 0], clamp);
  const draw = interpolate(f, [4, 38], [0, 1], { ...clamp, easing: easeOut });
  const nameO = interpolate(f, [22, 38], [0, 1], clamp);
  const lineW = interpolate(f, [52, 80], [0, 1], { ...clamp, easing: easeOut });
  const unk = interpolate(f, [56, 74], [0, 1], { ...clamp, easing: easeOut });
  const pulse = 1 + Math.sin(f * 0.16) * 0.06;
  const unkSpacing = 0.8 - 0.4 * unk;
  return (
    <AbsoluteFill style={{ background: C.black }}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse 85% 45% at 50% 40%, rgba(255,214,150,${0.42 * pulse}), rgba(0,0,0,0) 72%)`,
        }}
      />
      <Camera duration={90} zoom={[1.18, 1.0]} shake={3} seed="cta">
        <AbsoluteFill style={{ alignItems: "center" }}>
          <div style={{ marginTop: 250, opacity: nameO }}>
            <GoldCaps text="VELORIAN CHRONICLES" size={46} spacingFrom={0.7} spacingTo={0.3} delay={20} duration={30} sweepAt={30} weight={400} />
          </div>
          <div style={{ marginTop: 80 }}>
            <Emblem size={620} draw={draw} frame={f} glow={pulse} />
          </div>
          <div style={{ position: "absolute", top: 1180, width: W, display: "flex", flexDirection: "column", alignItems: "center", gap: 36 }}>
            <GoldCaps text="SUBSCRIBE" size={116} spacingFrom={0.8} spacingTo={0.2} delay={42} duration={34} sweepAt={56} />
            <div style={{ width: 640 * lineW, height: 2, background: `linear-gradient(90deg, transparent, ${C.gold}, transparent)`, boxShadow: `0 0 20px ${C.gold}` }} />
            <div
              style={{
                fontFamily: serifCaps,
                fontWeight: 400,
                fontSize: 40,
                letterSpacing: `${unkSpacing}em`,
                paddingLeft: `${unkSpacing}em`,
                color: C.white,
                opacity: unk,
                filter: `blur(${(1 - unk) * 10}px)`,
                textShadow: "0 0 30px rgba(255,214,150,.6)",
                whiteSpace: "nowrap",
              }}
            >
              &amp; ENTER THE UNKNOWN
            </div>
          </div>
        </AbsoluteFill>
      </Camera>
      <AbsoluteFill style={{ background: "#fff3d6", opacity: bloom }} />
    </AbsoluteFill>
  );
};

export const Trailer: React.FC<TrailerProps> = ({ clips }) => {
  const s = T.scenes;
  const shots: {
    line: string;
    accent?: string;
    cam: Omit<React.ComponentProps<typeof Camera>, "children" | "duration">;
    el: React.ReactNode;
  }[] = [
    {
      line: "you became a superhero?",
      accent: "superhero",
      cam: { zoom: [1.0, 1.22], y: [60, -60], roll: [-1.5, 0.5], seed: "s1" },
      el: <HeroScene />,
    },
    {
      line: "you woke up alone on Mars?",
      accent: "mars",
      cam: { zoom: [1.45, 1.1], y: [-40, 30], seed: "s2", shake: 3 },
      el: <MarsScene />,
    },
    {
      line: "you were trapped in a world that should not exist?",
      accent: "exist",
      cam: { zoom: [1.05, 1.3], roll: [-2.5, 2], seed: "s3" },
      el: <WorldScene />,
    },
    {
      line: "humanity disappeared overnight?",
      accent: "disappeared",
      cam: { zoom: [1.0, 1.14], seed: "s4", shake: 6 },
      el: <EmptyCityScene duration={s[3].dur} />,
    },
    {
      line: "you discovered something that changed reality?",
      accent: "reality",
      cam: { zoom: [1.0, 1.4], seed: "s5", shake: 10 },
      el: <TearScene duration={s[4].dur} />,
    },
  ];
  return (
    <AbsoluteFill style={{ background: C.black }}>
      <Sequence from={T.hook.from} durationInFrames={T.hook.dur}>
        <Hook />
      </Sequence>
      {shots.map((sh, i) => (
        <Sequence key={i} from={s[i].from} durationInFrames={s[i].dur}>
          <Shot duration={s[i].dur} clip={clips[i] ?? null} line={sh.line} accent={sh.accent} cam={sh.cam as never}>
            {sh.el}
          </Shot>
        </Sequence>
      ))}
      <Sequence from={T.tagline.from} durationInFrames={T.tagline.dur}>
        <Tagline />
      </Sequence>
      <Sequence from={T.brand.from} durationInFrames={T.brand.dur}>
        <Brand />
      </Sequence>
      <Sequence from={T.waiting.from} durationInFrames={T.waiting.dur}>
        <Waiting />
      </Sequence>
      <Sequence from={T.cta.from} durationInFrames={T.cta.dur}>
        <CTA />
      </Sequence>
      <Atmosphere />
    </AbsoluteFill>
  );
};
