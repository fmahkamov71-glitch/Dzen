import React from "react";
import { Easing, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { C, goldGradient, sans, serifCaps, serifItalic } from "./theme";

// Words that rise out of blur one by one.
export const Words: React.FC<{
  text: string;
  size: number;
  delay?: number;
  stagger?: number;
  color?: string;
  accent?: string; // words (lowercase match) rendered in gold
  align?: "center" | "left";
}> = ({ text, size, delay = 0, stagger = 5, color = C.white, accent, align = "center" }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div
      style={{
        fontFamily: serifItalic,
        fontStyle: "italic",
        fontWeight: 500,
        fontSize: size,
        lineHeight: 1.12,
        textAlign: align,
        color,
        textShadow: "0 4px 40px rgba(0,0,0,0.8)",
      }}
    >
      {text.split(" ").map((w, i) => {
        const p = spring({
          frame: f - delay - i * stagger,
          fps,
          config: { damping: 200 },
          durationInFrames: 22,
        });
        const isAccent = accent && w.toLowerCase().replace(/[.?]/g, "") === accent;
        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              marginRight: "0.28em",
              opacity: p,
              transform: `translateY(${(1 - p) * 34}px)`,
              filter: `blur(${(1 - p) * 12}px)`,
              color: isAccent ? C.gold : undefined,
            }}
          >
            {w}
          </span>
        );
      })}
    </div>
  );
};

export const Kicker: React.FC<{ text: string; delay?: number; size?: number }> = ({
  text,
  delay = 0,
  size = 30,
}) => {
  const f = useCurrentFrame();
  const p = interpolate(f - delay, [0, 18], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  return (
    <div
      style={{
        fontFamily: sans,
        fontWeight: 400,
        fontSize: size,
        letterSpacing: `${0.3 + (1 - p) * 0.5}em`,
        paddingLeft: `${0.3 + (1 - p) * 0.5}em`,
        color: C.gold,
        opacity: p,
        textAlign: "center",
      }}
    >
      {text}
    </div>
  );
};

// Gold metallic caps with an optional light sweep passing through the letters.
export const GoldCaps: React.FC<{
  text: string;
  size: number;
  spacingFrom: number;
  spacingTo: number;
  delay?: number;
  duration?: number;
  sweepAt?: number;
  weight?: 400 | 600;
}> = ({ text, size, spacingFrom, spacingTo, delay = 0, duration = 40, sweepAt = 30, weight = 600 }) => {
  const f = useCurrentFrame();
  const p = interpolate(f - delay, [0, duration], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const ls = spacingFrom + (spacingTo - spacingFrom) * p;
  const sweep = interpolate(f - sweepAt, [0, 28], [120, -20], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
  return (
    <div
      style={{
        fontFamily: serifCaps,
        fontWeight: weight,
        fontSize: size,
        letterSpacing: `${ls}em`,
        paddingLeft: `${ls}em`,
        whiteSpace: "nowrap",
        textAlign: "center",
        opacity: p,
        filter: `blur(${(1 - p) * 14}px)`,
        backgroundImage: `linear-gradient(105deg, transparent 38%, rgba(255,255,255,0.95) 50%, transparent 62%), ${goldGradient}`,
        backgroundSize: "300% 100%, 100% 100%",
        backgroundPosition: `${sweep}% 0, 0 0`,
        backgroundRepeat: "no-repeat",
        WebkitBackgroundClip: "text",
        backgroundClip: "text",
        color: "transparent",
        textShadow: "none",
        // glow lives on a drop-shadow so the clipped gradient stays crisp
        ["WebkitTextFillColor" as string]: "transparent",
      }}
    >
      {text}
    </div>
  );
};
