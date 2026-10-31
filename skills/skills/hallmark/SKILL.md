---
name: hallmark
description: "Design a landing page or another new marketing page in FigCraft that looks designed, not generated: Hallmark's floor against model defaults, a page shape from the category's anatomy, one theme as the material, one idea per screen. Use only when the designer chooses it or names Hallmark."
metadata:
  origin: hallmark
  group: task
  mode: manual
  title: Hallmark
  summary: лендинг или новая страница
---

# Hallmark in FigCraft

Hallmark makes pages a model draws look made, not generated: a hard floor against the defaults every model was trained into, a page built from what real sites in its category show, one theme as its material, one idea per screen. Above the floor the page is yours: you are a capable designer.

It was written for HTML and CSS with Node scripts; here you draw the page on a FigCraft canvas. The references speak CSS: read `:root` tokens as the file's variables, a `section` as a frame, `px` as page units. Its scripts (`theme.mjs`, `sloplint.mjs`, `capture.mjs`), the CSS stamp, `tokens.css` and `.hallmark/log.json` do not exist here: do their intent by hand, as each step says.

## The Floor

Binds every page, none of it waivable.

1. Every colour and every font goes through the file's variables and text styles (a theme's tokens become them). No raw hex on a layer. (48)
2. Never one italic word inside a roman heading. (38i)
3. Image frames and display heads never push their column wider than the grid: fixed widths, text that wraps. (50)
4. Every interactive element has a visible focus state, as a component variant. (26a, 15)
5. Never an invented metric, testimonial, logo wall or case-study count. (46a)
6. Never an eyebrow, and never a label in tracked capitals or small caps: labels, captions, table heads, tags and nav links are the body face (or the theme's label face), a step smaller, sentence or lower case, untracked. (54, 67)
7. Never middle-dot-joined meta strings, arrows glued to link text, or decorative status dots. (63)
8. Never a purple-to-blue gradient, a card inside a card, an emoji as an icon, or a hand-drawn browser or OS window. (2a, 4, 30a, 47a)
9. The hero's headline, one sentence and primary action fit in the first 1280 × 800 of the page frame. (44b)
10. About 80 words on any one screen; the hero's text is the headline, one sentence and its actions. (58)
11. The container is capped and centred: draw the page at 1440 wide on a 1200-ish container; the gutters grow, the measure does not. (44d)
12. Before handing back, walk `references/gates.md` § 4 against the frames (screenshot them) and fix every open Floor finding.

Above the Floor, a **Reflex** gate is a default a model falls into, waivable on the record with a real reason; a **Finish** check is craft detail, answered, never blocking (`references/gates.md` § 1 and § 2).

## Flow

0. **Pre-flight.** `DESIGN.md` at the project root locks the system: it overrides everything below. A prompt naming a real brand: read `references/brand-truth.md`; never theme a real brand from memory. Look at the file: its variables, text styles, components and the screens already there.
1. **Ask once,** in one message: material (screenshots, photos, real numbers, quotes with names, logos they may use), audience, the one action the page drives, the tone as an extreme (editorial, brutalist, soft, utilitarian, luxury, playful, technical, austere). "Go ahead" or skipped fields: infer, say what you picked in one line. Facts are never inferred: a number, a quote or a logo not given is absent; a picture not given is a placeholder frame.
2. **Shape.** The material inventory in one line (real · pictures · absent). Name what a visitor comes to do and read that job in `references/anatomy.md`; build the page from that anatomy, never from a default run of features, steps and an email band. Pick one of the 21 shapes in `references/macrostructures.md` and load only its file. Compositions, navs and footers: `references/layout.md`. **Signature:** the one thing a visitor would remember, the prompt's strongest real thing shown at its best, on the first screen.
3. **Direction.** A Hallmark style chosen in the chat (a `hallmark-*` skill in this turn) is the theme. Otherwise pick one from `references/themes.md` whose material can carry the prompt, say which and why, and read only its `SKILL.md`. "Custom", "bespoke", "no theme": `references/direction.md` replaces the theme, the shapes and `layout.md`; the Floor and the gates hold. A theme is a material, never a plan: it never sets what the page contains.
4. **Load,** for a page: `references/layout.md`, the job's part of `anatomy.md`, `imagery.md`, `craft.md`, the theme (its genre comes with it), `gates.md` § 1 to § 4. Only when needed: one macrostructure file; `interaction-and-states.md` for forms; `responsive.md` when a mobile frame is asked for; `dark-mode.md`, `data-viz.md`, `texture.md` when the theme or the page needs them.
5. **The Picks block,** once, before drawing; the designer's chance to redirect:

   ```markdown
   **Hallmark**
   - **Shape** · Workbench · genre modern-minimal · job: sign up, the action in the hero and beside the price
   - **Theme** · Coral (warm grey, one coral signal, General Sans, soft pills)
   - **Chrome** · nav: edge-aligned, a wordmark and one action · footer: a mast, the wordmark over the links
   - **Hero** · Stage: head on columns 1 to 5, the picture on 6 to 12
   - **Signature** · the invoice list chasing a late payment, drawn in the hero
   - **Sections** · Hero · Pinned · Switcher · Table (pricing) · Footer
   - **Material** · real: … · pictures: … · absent: logos, quotes, metrics
   ```

6. **Draw.** The theme's variables and text styles first. Then the nav and the hero only, screenshot them and review against `gates.md` § 6 (the hero review) before the sections. One idea per screen, set big: a headline of seven words or fewer, one sentence of twelve or fewer, one or two actions; six to nine sections, hero and footer included; 450 visible words at most. Show, do not describe: the user's pictures or screenshots of the real product; otherwise a placeholder frame in the theme's treatment, named for what belongs there. Never a drawn illustration, an empty wash, a row of counting marks or an invented figure. One primary button style, one container width, one radius per nesting level. Controls are components with their states as variants (`references/patterns.md`, `interaction-and-states.md`).
7. **Sweep.** Screenshot the page frame and walk `gates.md` § 4 and § 5: fix every Floor finding, fix or waive every Reflex one, answer every Finish one. Then the finish review (`gates.md` § 6) as a fresh look at the screenshot. Close with the material ask: every placeholder, its size and what belongs there, then the one piece of material that would most improve the page. Never claim a check you did not do.

## Branches

`references/flow.md`, one section at a time: **component scope** (one element: all eight states as variants, no page), **app screens** (a dashboard, settings, a tool: the theme lends palette, faces, radius and surfaces; no hero, no word budget; four data states), redesign and audit (`references/redesign.md`, only when the designer names Hallmark on an existing page).
