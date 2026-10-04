import React from "react";
import { C } from "./theme";

// Brand mark: an orbit of rings around a vertical doorway of light.
export const Emblem: React.FC<{
  size: number;
  draw: number; // 0..1 draw-in
  frame: number;
  glow?: number;
}> = ({ size, draw, frame, glow = 1 }) => {
  const R = 270;
  const circ = 2 * Math.PI * R;
  return (
    <svg width={size} height={size} viewBox="-300 -300 600 600" style={{ overflow: "visible" }}>
      <defs>
        <radialGradient id="emGlow">
          <stop offset="0" stopColor="#fff3d1" stopOpacity={0.9 * glow} />
          <stop offset="0.4" stopColor={C.gold} stopOpacity={0.35 * glow} />
          <stop offset="1" stopColor={C.gold} stopOpacity="0" />
        </radialGradient>
        <linearGradient id="emDoor" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#fff" stopOpacity="0" />
          <stop offset="0.5" stopColor="#fff8e6" />
          <stop offset="1" stopColor="#fff" stopOpacity="0" />
        </linearGradient>
        <filter id="emBlur">
          <feGaussianBlur stdDeviation="8" />
        </filter>
      </defs>
      <circle r={300} fill="url(#emGlow)" opacity={draw} />
      <circle
        r={R}
        fill="none"
        stroke={C.gold}
        strokeWidth={2.5}
        strokeDasharray={circ}
        strokeDashoffset={circ * (1 - draw)}
        transform="rotate(-90)"
        opacity={0.95}
      />
      <g transform={`rotate(${frame * 0.35})`} opacity={draw * 0.8}>
        <circle r={238} fill="none" stroke={C.gold} strokeWidth={5} strokeDasharray="2 17" />
      </g>
      <g transform={`rotate(${-frame * 0.6})`} opacity={draw}>
        <circle
          r={190}
          fill="none"
          stroke={C.gold}
          strokeWidth={1.5}
          strokeDasharray={`${2 * Math.PI * 190 * 0.72} ${2 * Math.PI * 190 * 0.28}`}
        />
        <circle cx={190} cy={0} r={7} fill="#fff3d1" />
      </g>
      {/* doorway of light */}
      <g opacity={draw}>
        <path d="M0 -150 L26 0 L0 150 L-26 0 Z" fill="url(#emDoor)" filter="url(#emBlur)" opacity={0.9 * glow} />
        <path d="M0 -150 L26 0 L0 150 L-26 0 Z" fill="none" stroke="#fff3d1" strokeWidth={2} />
      </g>
    </svg>
  );
};
