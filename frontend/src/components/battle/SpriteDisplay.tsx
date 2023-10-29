interface Props {
  src: string;
  name: string;
  animationClass: string;
  flipped?: boolean;
}

export default function SpriteDisplay({ src, name, animationClass, flipped }: Props) {
  return (
    <div
      className={animationClass}
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <img
        src={src}
        alt={name}
        style={{
          width: '96px',
          height: '96px',
          imageRendering: 'pixelated',
          transform: flipped ? 'scaleX(-1)' : undefined,
        }}
      />
    </div>
  );
}
