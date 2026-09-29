# Subtitles

Subtitles are a governed layer over PD Body. They set dialogue in films, showreels, interviews, product videos, web video and short-form vertical clips, burned in or as a styled text track.

Research checked: 29 September 2026. Sources are listed at the end.

## Styles

| Style | Text | Box | Use it for |
| --- | --- | --- | --- |
| `broadcast` | White `#FFFFFF` | Black at 75 % | The default. Legible over any footage |
| `cinema` | Cinema yellow `#FFD84A` | Black at 70 % | Films, trailers, showreels, and any video that wants the cinema look |
| `clean` | White with a soft black outline | None | Dark or controlled footage only |

The box sits behind each line, as wide as that line, and the lines of a two-line subtitle touch with no gap. Over a pure white picture, broadcast keeps 10.4:1 contrast and cinema 6.2:1; the validator holds both at 4.5:1 or more. Any style may be used on any video; the last column is advice, not a restriction. Clean has no box, so its contrast depends on the picture: check every shot where it sits over sky, paper, snow or a white wall, and switch to broadcast or cinema where it fails.

## Voices

| Role | Family | Use |
| --- | --- | --- |
| `subtitle.line` | PD Body SemiBold (600) | Dialogue and on-screen speech |
| `subtitle.italic` | PD Body SemiBold Italic | Narration, inner voice, sung lyrics, off-screen or remote speakers, unfamiliar foreign words and titles of works |
| `subtitle.punch` | PD Body Alt Bold (700) | Short-form burned-in captions of one to six words and at most 18 characters per cue |

PD Body at 600 is the subtitle voice: open counters, even colour and clear figures survive a translucent box, compression and a small phone. Head is too condensed and too expressive for text people read while watching, and Eyebrow is for labels, not sentences. Punch is for vertical social clips where each cue is a few words; it is not for films.

## Frames

Sizes are measured from the frame, so a subtitle keeps its proportion at any resolution. Pixel values are for the frame sizes listed; at 4K, double them.

| Frame | Size | Text | Line | Distance from bottom | Line width | Characters per line |
| --- | --- | --- | --- | --- | --- | --- |
| `landscape` 16:9 | 1920 × 1080 | 64 px (5.9 % of height) | 76 px | 8 % | 68 % | 42 |
| `standard` 4:3 | 1440 × 1080 | 64 px | 76 px | 8 % | 90 % | 42 |
| `square` 1:1 | 1080 × 1080 | 64 px | 76 px | 9 % | 90 % | 30 |
| `vertical` 9:16 | 1080 × 1920 | 67 px (3.5 % of height) | 80 px | 30 % | 76 % | 24 |

Punch captions are 71 px on landscape, standard and square frames and 91 px on vertical. Every subtitle sets with a line height of 1.2 and tracking of 0.01em (punch: 1.1 and −0.01em), so the boxes of two lines touch.

The distance from the bottom is measured from the bottom edge of the frame to the bottom edge of the lowest line's box. On vertical video, Reels, Shorts, Stories and TikTok draw their caption, audio credit and progress bar over the bottom of the frame and a column of buttons down the right edge, so the vertical cue sits 30 % up and stays within the middle 76 % of the width. That is narrower than the BBC's 90 % for 9:16. Platform interfaces change, so check an exported frame in the app before publishing.

Move a cue to the top of the frame when the picture carries text, a lower third or a chart at the bottom. Keep it there for the whole shot.

## Writing subtitles

- One line when the text fits. Two lines at most.
- A line holds at most the characters its frame allows above: 42 on landscape and 4:3, 30 on square, 24 on vertical. The roles' own limit of 42 is the ceiling on any frame; the frame's limit wins. Count every character, spaces and punctuation included.
- A subtitle holds at most 16 words (a punch caption 6).
- When a subtitle needs two lines, prefer a short top line and a longer bottom line, but never one or two words alone on top.
- Break a line after punctuation, or before a conjunction or a preposition. Keep together an article and its noun, an adjective and its noun, a first and last name, a pronoun and its verb, and a verb with its auxiliary, preposition or negation.
- Two speakers in one subtitle: one line each, each starting with a hyphen and no space (`-Is it ready?`).
- Show each subtitle for at least five-sixths of a second and at most seven seconds.
- Reading speed: at most 20 characters per second for adults, 17 for children, counting every character on screen, spaces included, over the time the subtitle is shown. When the text is too long for the time, cut words or split the subtitle; never shrink the type.
- Italics only for narration, inner voice, sung lyrics, off-screen voices, unfamiliar foreign words and titles of works. Use `subtitle.italic` for a whole line, and `<i>` inside a `subtitle.line` for a word.
- Centre subtitles, at the bottom or the top of the frame.

## At delivery size

A subtitle is read at the size of the screen it plays on. A vertical video full screen on a phone about 390 px wide shows vertical subtitles at about 24 px. Landscape video in a phone held upright is about 390 px wide, so its subtitles show at about 13 px, and at about 23 px when the phone is turned sideways. These are the smallest sizes the roles are meant for; never set subtitles smaller than the frame table to fit more words.

## On the web

```html
<link rel="stylesheet" href="pitchdog-system.css">

<div data-pd-subtitle-frame="landscape" data-pd-subtitle-style="cinema">
  <video src="film.mp4"></video>
  <p data-pd-subtitle-cue>
    <span data-pd-subtitle="line">We didn’t want a better deck.</span>
    <span data-pd-subtitle="line">We wanted to walk out with the money.</span>
  </p>
</div>
```

Each line is its own element, so each line gets its own box. Add `data-pd-subtitle-cue="top"` to move a cue to the top. The style can sit on the frame or on a single cue. Import only the subtitle layer with `@pitchdog/type-system/subtitle.css` after `fonts.css` and `typography.css`; like the other media layers it uses variables that `typography.css` declares.

### Native text tracks

A `<video>` with a WebVTT `<track>` takes the family, weight, colour and box of a style from `::cue`:

```html
<video controls data-pd-subtitle-style="cinema">
  <source src="film.mp4" type="video/mp4">
  <track kind="subtitles" src="film.en.vtt" srclang="en" label="English" default>
</video>
```

The browser and the viewer's own caption settings keep control of size and position, and a viewer's settings can override the style. That is correct for accessibility. For an exact look, burn the subtitles in.

## Burned in

To burn subtitles into a video in Premiere Pro, DaVinci Resolve, Final Cut Pro or CapCut, set the caption track to:

- Font: PD Body SemiBold (italic lines: PD Body SemiBold Italic; punch: PD Body Alt Bold)
- Size: 64 px on a 1080-high landscape frame, 67 px on a 1080 × 1920 vertical frame; double both at 4K
- Line height 1.2 and tracking 0.01em (1 % in editors that use percentages), with the boxes of two lines touching
- Colour and background: the style's text colour, with a black background at the style's opacity, drawn per line
- Background padding: 0.4 em left and right (26 px at 64 px), none above or below
- Position: centred, the distance from the bottom in the frames table

Or render overlays from `subtitle/subtitle-starter.html`: give a frame the `data-overlay` attribute and its full width in pixels, and screenshot it with a transparent background.

## Platforms

- YouTube: uploaded caption files are drawn by the YouTube player in its own font, and each viewer can restyle them. Upload captions for accessibility and search; burn subtitles in only when the look matters, and then also upload the caption file.
- Reels, Shorts, Stories and TikTok: many people watch without sound, so burn in punch or line captions on the vertical frame, 30 % up and inside the middle 76 %.
- A burned-in subtitle cannot be turned off, translated or read by a screen reader. Publish a caption file or transcript alongside it.

## Sources

- BBC Subtitle Guidelines, sections 3.1 (line length), 9.2.1 (line height 7–8 % of video height for 16:9, 4:3 and 1:1, 3.9–4.5 % for 9:16) and 9.2.4 (a background behind each line, with no gap between lines): <https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles/>
- Netflix Timed Text Style Guide, General Requirements (duration, two lines, centred at top or bottom): <https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements>
- Netflix English (USA) Timed Text Style Guide (42 characters per line, line breaks, dual speakers, italics, reading speed): <https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-USA-Timed-Text-Style-Guide>
- WebVTT `::cue` styling: <https://www.w3.org/TR/webvtt1/#the-cue-pseudo-element>
- Vertical placement: third-party safe-zone guides for Reels and TikTok, which agree that a column of buttons takes about the right 11 % of the width and the caption and audio credit take the bottom 17 to 35 %. These guides are not platform documentation, so the vertical cue is the system's own choice inside their ranges.
