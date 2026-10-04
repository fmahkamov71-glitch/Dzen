import React, { useMemo } from "react";
import {
  AbsoluteFill,
  interpolate,
  interpolateColors,
  random,
  useCurrentFrame,
} from "remotion";
import { H, T, W } from "./theme";

const N = 90;

// Global layer on top of every shot: drifting particles, vignette and film grain.
export const Atmosphere: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / 30;

  const dots = useMemo(
    () =>
      new Array(N).fill(0).map((_, i) => ({
        x: random(`x${i}`) * W,
        y: random(`y${i}`) * H,
        r: 1.5 + random(`r${i}`) ** 2 * 7,
        v: 18 + random(`v${i}`) * 70,
        sway: 10 + random(`s${i}`) * 40,
        ph: random(`p${i}`) * 6.28,
        a: 0.2 + random(`a${i}`) * 0.6,
      })),
    [],
  );

  // particles shift from cold dust to warm gold embers toward the brand reveal
  const color = interpolateColors(
    f,
    [0, T.tagline.from, T.brand.from + 20, T.cta.from],
    [
      "rgba(190,220,255,1)",
      "rgba(190,220,255,1)",
      "rgba(255,214,150,1)",
      "rgba(255,214,150,1)",
    ],
  );
  const speed = interpolate(
    f,
    [T.tagline.from, T.brand.from, T.cta.from, 600],
    [1, 1.8, 1.2, 0.8],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {dots.map((d, i) => {
        const y = (((d.y - d.v * t * speed) % (H + 40)) + (H + 40)) % (H + 40) - 20;
        const x = d.x + Math.sin(t * 0.8 + d.ph) * d.sway;
        const tw = 0.6 + 0.4 * Math.sin(t * 2 + d.ph * 3);
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: x,
              top: y,
              width: d.r * 2,
              height: d.r * 2,
              borderRadius: "50%",
              background: color,
              opacity: d.a * tw * 0.7,
              filter: d.r > 5 ? "blur(3px)" : undefined,
              boxShadow: `0 0 ${d.r * 3}px ${color}`,
            }}
          />
        );
      })}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at 50% 48%, rgba(0,0,0,0) 45%, rgba(0,0,0,0.78) 100%)",
        }}
      />
      <svg
        width={W}
        height={H}
        style={{ position: "absolute", inset: 0, mixBlendMode: "overlay", opacity: 0.16 }}
      >
        <filter id="grain">
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.85"
            numOctaves="2"
            seed={Math.floor(f / 2)}
          />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width={W} height={H} filter="url(#grain)" />
      </svg>
    </AbsoluteFill>
  );
};
