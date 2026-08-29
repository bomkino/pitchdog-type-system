# Head italics

## Defect found

The previous release declared the same Head variable file as conventional normal and italic faces, then relied on `font-style: italic` to select the posture. The specimen did not reliably demonstrate a visible axis change.

## Version 13 fix

- Load the Head file once.
- Keep `font-style: normal` so no synthetic slant participates.
- Set the real `ital` axis explicitly.
- Set `font-synthesis: none`.
- Use `ital: 0` and `ital: 1` for static roles.
- Permit continuous values only for an opt-in tested transition.

## Use

```html
<h1 data-pd-type="display.hero">
  Your pitch’s <span data-pd-emphasis="head-italic">best friend.</span>
</h1>
```

## Do not

- italicise several unrelated words in one heading
- use the italic merely to make a layout feel busier
- mix Head italic and Body italic inside one short headline
- rely on browser synthesis
