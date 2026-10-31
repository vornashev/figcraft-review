// What sidecar/test_ui.mjs reaches into: the store and the composer's functions, on window.__t.
import * as A from "./actions";
import * as ed from "./composer";
import {get, pinned, set, skillOf} from "./store";
import {zoomNow} from "./components/Viewer";

export function exposeForTests() {
  Object.assign(window, {__t: {
    get, set, pinned, skillOf, zoom: () => zoomNow,
    segments: ed.segments, insertChips: ed.insertChips, placeCaret: ed.placeCaret, changed: ed.changed, editor: ed.editor,
    addFile: A.addFile, addFiles: A.addFiles, clearDraft: A.clearDraft, newChat: A.newChat, loadRemarks: A.loadRemarks, openSkill: A.openSkill,
  }});
}
