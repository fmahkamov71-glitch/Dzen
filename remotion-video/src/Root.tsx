import { Composition } from "remotion";
import { Trailer, TrailerProps } from "./Trailer/Trailer";
import { FPS, H, W } from "./Trailer/theme";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="VelorianTrailer"
      component={Trailer}
      durationInFrames={20 * FPS}
      fps={FPS}
      width={W}
      height={H}
      defaultProps={
        {
          // Drop photoreal clips into /public and list them here, e.g. "clips/shot1.mp4".
          clips: [null, null, null, null, null],
        } satisfies TrailerProps
      }
    />
  );
};
