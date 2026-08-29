# UI/UX typography

## Principle

Interfaces should feel generous and modern without becoming cinematic at every level. Body leads. Head appears only when a product moment benefits from story or delight.

## Roles

- `ui.display` — head 500; clamp(2.375rem, 1.86rem + 1.6vi, 3.75rem); Onboarding, empty-state and celebratory display only
- `ui.pageTitle` — body 700; clamp(1.75rem, 1.55rem + .62vi, 2.25rem); Primary title of an application view
- `ui.sectionTitle` — body 600; clamp(1.3125rem, 1.22rem + .29vi, 1.5625rem); Major region within a view
- `ui.panelTitle` — body 600; clamp(1.0625rem, 1.025rem + .12vi, 1.1875rem); Cards, dialogs, toasts and panels
- `ui.body` — body 400; clamp(1rem, .981rem + .06vi, 1.0625rem); Default interface copy
- `ui.bodyCompact` — body 400; clamp(.9375rem, .919rem + .055vi, 1rem); Dense tables, lists and secondary interface copy
- `ui.label` — body 600; clamp(.875rem, .856rem + .055vi, .9375rem); Form labels and compact headings
- `ui.action` — body 600; clamp(.9375rem, .919rem + .055vi, 1rem); Buttons, tabs and primary navigation
- `ui.input` — body 400; clamp(1rem, .981rem + .06vi, 1.0625rem); Input values, selections and editable fields
- `ui.caption` — body 400; clamp(.8125rem, .794rem + .055vi, .875rem); Help, timestamps and non-essential supporting copy
- `ui.badge` — eyebrow 600; clamp(.6875rem, .669rem + .055vi, .75rem); Short status and category badges
- `ui.metadata` — eyebrow 500; clamp(.75rem, .731rem + .055vi, .8125rem); Versions, dates, dimensions and file facts
- `ui.data` — eyebrow 500; clamp(.8125rem, .794rem + .055vi, .875rem); Aligned numbers, prices, counts and durations
- `ui.code` — eyebrow 400; clamp(.8125rem, .794rem + .055vi, .875rem); Literal filenames, code and machine identifiers

## Density

| Mode | Control height | Use |
|---|---:|---|
| Comfortable | 52 px | Touch-first, onboarding, forms and simple tools |
| Default | 48 px | Standard pitch.dog interfaces |
| Compact | 40 px | Pointer-dense tables and professional tools only |

On coarse pointers, compact controls return to 48 px.

## Component mapping

- Buttons, tabs, primary nav: `ui.action`
- Form labels: `ui.label`
- Input values: `ui.input`
- Table headings: `ui.label`
- Table copy: `ui.bodyCompact`
- Aligned numbers: `ui.data`
- Filenames and identifiers: `ui.code`
- Badges: `ui.badge`
- Help and timestamps: `ui.caption`

## State behaviour

Do not change weight on hover, selected or focus states. Weight changes alter width and can produce jitter. Use colour, fill, border, underline, movement or icon treatment instead.

## Copy behaviour

- Sentence case by default
- Labels name the field, not the implementation
- Errors state the problem and the remedy
- Placeholder text never replaces a persistent label
- Button text begins with a verb where the action is not obvious
- Tooltips explain unfamiliar controls, never hide essential instructions
