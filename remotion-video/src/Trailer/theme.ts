import { continueRender, delayRender, staticFile } from "remotion";

export const W = 1080;
export const H = 1920;
export const FPS = 30;

// Fonts are bundled in /public/fonts so renders work offline.
const FACES: [string, string, string, string][] = [
  ["Cinzel", "cinzel-400", "400", "normal"],
  ["Cinzel", "cinzel-600", "600", "normal"],
  ["Cormorant Garamond", "cormorant-italic-500", "500", "italic"],
  ["Inter", "inter-300", "300", "normal"],
  ["Inter", "inter-400", "400", "normal"],
];
const handle = delayRender("fonts");
Promise.all(
  FACES.map(async ([family, file, weight, style]) => {
    const face = new FontFace(family, `url(${staticFile(`fonts/${file}.woff2`)})`, { weight, style });
    document.fonts.add(await face.load());
  }),
)
  .catch((e) => console.error("font load failed", e))
  .finally(() => continueRender(handle));

export const serifCaps = "Cinzel, serif";
export const serifItalic = '"Cormorant Garamond", serif';
export const sans = "Inter, sans-serif";

export const C = {
  black: "#04050a",
  ice: "#d6e8ff",
  white: "#f6f3ec",
  gold: "#e8c27a",
  goldDeep: "#9b6b2a",
  teal: "#5fd4ff",
  ember: "#ff8a3c",
};

export const goldGradient =
  "linear-gradient(180deg,#fff6dc 0%,#f0cf8a 42%,#b07d35 100%)";

// Section timeline (frames @30fps, 600 total = 20s)
export const T = {
  hook: { from: 0, dur: 60 },
  // accelerating rhythm: 2.0s, 1.8s, 1.67s, 1.53s, 1.5s
  scenes: [
    { from: 60, dur: 60 },
    { from: 120, dur: 54 },
    { from: 174, dur: 50 },
    { from: 224, dur: 46 },
    { from: 270, dur: 45 },
  ],
  tagline: { from: 315, dur: 60 },
  brand: { from: 375, dur: 90 },
  waiting: { from: 465, dur: 45 },
  cta: { from: 510, dur: 90 }, // final 3 seconds
};
