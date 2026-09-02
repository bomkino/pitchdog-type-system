export const VERSION = "13.1.1" as const;
export const HEAD_WEIGHTS = [265, 300, 400, 500, 600, 700, 900] as const;
export const BODY_WEIGHTS = [100, 250, 300, 400, 600, 700, 900] as const;
export const EYEBROW_WEIGHTS = [100, 200, 300, 350, 400, 500, 600, 700, 800, 900] as const;
export const EYEBROW_WIDTHS = [87.5, 100] as const;
export const ARROWS = ["←", "↑", "→", "↓", "↔", "↕", "↖", "↗", "↘", "↙", "↩", "↪"] as const;
export const WEB_MEASURES = {
  narrow: "38ch",
  intro: "48ch",
  reading: "45ch",
  default: "48ch",
  wide: "52ch",
  ceiling: "54ch",
} as const;
export const WEB_WRAP_STYLES = ["auto", "balance", "pretty", "stable", "avoid-orphans"] as const;

export type HeadWeight = typeof HEAD_WEIGHTS[number];
export type BodyWeight = typeof BODY_WEIGHTS[number];
export type EyebrowWeight = typeof EYEBROW_WEIGHTS[number];
export type EyebrowWidth = typeof EYEBROW_WIDTHS[number];
export type WebMeasure = keyof typeof WEB_MEASURES;
export type WebWrapStyle = typeof WEB_WRAP_STYLES[number];
export type WebRole = "display.hero" | "display.chapter" | "heading.section" | "heading.subsection" | "title.card" | "title.functional" | "lead.hero" | "lead.section" | "body.reading" | "body.default" | "body.compact" | "body.small" | "quote.feature" | "label" | "metadata" | "data" | "metric";
export type UiRole = "ui.display" | "ui.pageTitle" | "ui.sectionTitle" | "ui.panelTitle" | "ui.body" | "ui.bodyCompact" | "ui.label" | "ui.action" | "ui.input" | "ui.caption" | "ui.badge" | "ui.metadata" | "ui.data" | "ui.code";
export type SocialRole = "social.display" | "social.headline" | "social.subhead" | "social.body" | "social.quote" | "social.metric" | "social.label" | "social.metadata" | "social.credit";
export type YouTubeRole = "youtube.title" | "youtube.titleCompact" | "youtube.kicker" | "youtube.support" | "youtube.badge" | "youtube.credit" | "youtube.arrow";

export function isHeadWeight(value: number): value is HeadWeight { return (HEAD_WEIGHTS as readonly number[]).includes(value); }
export function isBodyWeight(value: number): value is BodyWeight { return (BODY_WEIGHTS as readonly number[]).includes(value); }
export function isEyebrowWeight(value: number): value is EyebrowWeight { return (EYEBROW_WEIGHTS as readonly number[]).includes(value); }
export function isEyebrowWidth(value: number): value is EyebrowWidth { return (EYEBROW_WIDTHS as readonly number[]).includes(value); }
