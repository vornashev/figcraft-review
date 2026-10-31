# Notes for agents

- Remarks come as a `# FigCraft — <file> · N замечаний` Markdown document (or run `agent/review.py` yourself). Each `## N. text` is the instruction; its bullets name the layer (`· #ID`), its path (◇ marks an instance) and the component to edit instead of the instance.
- Map values to the file's design system (variables, text styles, components) rather than raw colours and sizes.
- Work through them with `agent/review.py next` and `show N` (`--shots` for a PNG of the context).
- After a fix: `agent/review.py done N "what changed"` — the remark goes to the designer as «Проверь», who accepts it or sends it back open. A question: `ask N "…" --option "A" --option "B"` (the designer picks an option or answers; the remark comes back open). Won't do: `reject N "why"`. Never edit the `#N ·` labels by hand.
- The export lists only open remarks; questions and «Проверь» wait for the designer — leave them.
- One agent per FigCraft document: the undo history is shared.
