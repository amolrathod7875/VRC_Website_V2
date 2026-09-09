import { GetInTouchSection } from "@/components/GetInTouchSection";

export type CtaBannerProps = {
  eyebrow: string;
  title: string;
  text: string;
  primaryHref?: string;
  primaryLabel?: string;
  secondaryHref?: string;
  secondaryLabel?: string;
};

/**
 * Legacy alias for the shared Get in Touch section.
 *
 * The homepage originally rendered this component directly. It now delegates
 * to the single shared `GetInTouchSection` so every page reuses the exact
 * same implementation, video, overlay and buttons.
 */
export function CtaBanner({
  eyebrow,
  title,
  text,
  primaryHref,
  primaryLabel,
  secondaryHref,
  secondaryLabel,
}: CtaBannerProps) {
  return (
    <GetInTouchSection
      eyebrow={eyebrow}
      title={title}
      text={text}
      primaryHref={primaryHref}
      primaryLabel={primaryLabel}
      secondaryHref={secondaryHref}
      secondaryLabel={secondaryLabel}
    />
  );
}