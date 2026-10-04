import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { noise2D } from "@remotion/noise";

type Range = [number, number];

// Cinematic virtual camera: eased push/pull, drift, roll and handheld shake.
export const Camera: React.FC<{
  duration: number;
  zoom?: Range;
  x?: Range;
  y?: Range;
  roll?: Range;
  shake?: number;
  seed?: string;
  children: React.ReactNode;
}> = ({
  duration,
  zoom = [1.05, 1.2],
  x = [0, 0],
  y = [0, 0],
  roll = [0, 0],
  shake = 4,
  seed = "cam",
  children,
}) => {
  const f = useCurrentFrame();
  const opts = {
    easing: Easing.inOut(Easing.cubic),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  } as const;
  const t = (r: Range) => interpolate(f, [0, duration], r, opts);
  const sx = noise2D(seed + "x", f * 0.06, 0) * shake;
  const sy = noise2D(seed + "y", f * 0.06, 9) * shake;
  const sr = noise2D(seed + "r", f * 0.04, 3) * shake * 0.04;
  return (
    <AbsoluteFill
      style={{
        transform: `translate(${t(x) + sx}px, ${t(y) + sy}px) rotate(${t(roll) + sr}deg) scale(${t(zoom)})`,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};
