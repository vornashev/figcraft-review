// The UI's icons: Material Design Icons as SVG paths, by name. The design file draws the same ones as vectors.
import {mdiAlert, mdiArrowLeft, mdiAsterisk, mdiAutoFix, mdiBookOutline, mdiCellphone, mdiCheck, mdiCheckCircle, mdiChevronDown,
  mdiClose, mdiCogOutline, mdiCommentOutline, mdiContentCopy, mdiDownload, mdiFile, mdiFileDocument, mdiFileOutline, mdiImage, mdiLock, mdiMagnify, mdiPalette, mdiPin,
  mdiPlus, mdiPuzzleOutline, mdiShapeOutline, mdiSourceBranch, mdiStarOutline, mdiStar} from "@mdi/js";

export const ICONS = {
  alert: mdiAlert, back: mdiArrowLeft, claude: mdiAsterisk, fix: mdiAutoFix, book: mdiBookOutline, phone: mdiCellphone, check: mdiCheck,
  done: mdiCheckCircle, chevron: mdiChevronDown, close: mdiClose, gear: mdiCogOutline, comment: mdiCommentOutline, copy: mdiContentCopy, download: mdiDownload, file: mdiFile,
  doc: mdiFileDocument, attach: mdiFileOutline, image: mdiImage, lock: mdiLock, search: mdiMagnify, palette: mdiPalette, pin: mdiPin,
  plus: mdiPlus, puzzle: mdiPuzzleOutline, shape: mdiShapeOutline, branch: mdiSourceBranch,
  star: mdiStarOutline, starred: mdiStar,
};
export type IconName = keyof typeof ICONS;
export const isIcon = (s: unknown): s is IconName => typeof s === "string" && s in ICONS;

// For the composer's chips, which are built as DOM outside React.
export const iconSvg = (n: IconName) => `<svg class="g" viewBox="0 0 24 24" aria-hidden="true"><path d="${ICONS[n]}"/></svg>`;
