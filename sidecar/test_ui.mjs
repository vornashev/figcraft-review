// node sidecar/test_ui.mjs [shot.png] — drives the built chat (web/dist/index.html) in headless Chromium through the DevTools protocol.
// The server is stubbed in the page (fetch and EventSource), so neither FigCraft nor an agent is needed.
import {spawn, execFileSync} from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const shot = process.argv[2];
const page = "file://" + path.join(path.dirname(new URL(import.meta.url).pathname), "web/dist/index.html");
const port = 9300 + Math.floor(Math.random() * 600);
const profile = fs.mkdtempSync(path.join(os.tmpdir(), "figcraft-agent-ui-"));
const chrome = spawn(process.env.CHROMIUM || "chromium", ["--headless=new", `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`,
  "--window-size=420,860", "--no-first-run", ...(process.env.CI ? ["--no-sandbox"] : []), "about:blank"], {stdio: "ignore"});
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let targets;
for (let i = 0; i < 50 && !targets; i++) {
  await sleep(200);
  targets = await fetch(`http://127.0.0.1:${port}/json`).then((r) => r.json()).catch(() => null);
}
if (!targets) { chrome.kill(); throw new Error(`${process.env.CHROMIUM || "chromium"} didn't open its debugging port`); }
const ws = new WebSocket(targets.find((t) => t.type === "page").webSocketDebuggerUrl);
await new Promise((r) => ws.onopen = r);
let n = 0;
const wait = new Map();
ws.onmessage = (m) => { const d = JSON.parse(m.data);
  const params = d.method === "Fetch.requestPaused" && d.params.request.url.includes("api/skill-image") && new URL(d.params.request.url).searchParams;
  const image = params && new URL(`../skills/skills/${params.get("name")}/${params.get("file")}`, import.meta.url);
  // Imported collections (opendesign-*) live outside the repo: their images get the stub below.
  if (image && fs.existsSync(image)) {
    send("Fetch.fulfillRequest", {requestId: d.params.requestId, responseCode: 200, responseHeaders: [{name: "Content-Type", value: "image/webp"}],
      body: fs.readFileSync(image).toString("base64")});
  } else if (d.method === "Fetch.requestPaused") send("Fetch.fulfillRequest", {requestId: d.params.requestId, responseCode: 200,
    responseHeaders: [{name: "Content-Type", value: "image/svg+xml"}], body: Buffer.from('<svg xmlns="http://www.w3.org/2000/svg" width="536" height="418"><rect width="536" height="418" fill="#24211e"/><rect x="24" y="24" width="488" height="44" rx="8" fill="#2f2b27"/><text x="40" y="52" fill="#ede7dc" font-family="sans-serif" font-size="18">FigCraft — Image preview</text><rect x="24" y="84" width="130" height="310" rx="8" fill="#1c1a17"/><rect x="172" y="84" width="340" height="310" rx="8" fill="#1f3a35"/></svg>').toString("base64")}); if (wait.has(d.id)) { wait.get(d.id)(d.result); wait.delete(d.id); } };
const send = (method, params = {}) => new Promise((r) => { const id = ++n; wait.set(id, r); ws.send(JSON.stringify({id, method, params})); });
const js = async (expr) => {
  const r = await send("Runtime.evaluate", {expression: expr, returnByValue: true, awaitPromise: true});
  if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
  return r.result.value;
};
const key = async (k, code, vk, mods = 0) => {
  await send("Input.dispatchKeyEvent", {type: "rawKeyDown", key: k, code, windowsVirtualKeyCode: vk, modifiers: mods});
  await send("Input.dispatchKeyEvent", {type: "keyUp", key: k, code, windowsVirtualKeyCode: vk, modifiers: mods});
};
const press = (ch) => send("Input.dispatchKeyEvent", {type: "keyDown", key: ch, text: ch, code: "Digit" + ch, windowsVirtualKeyCode: ch.charCodeAt(0)});
const type = (t) => send("Input.insertText", {text: t});
const segs = () => js("JSON.stringify(segments().map(s => s.kind === 'text' ? s.text : '[' + s.label + ']'))").then(JSON.parse);
const calls = (p) => js(`JSON.stringify(__api.filter(([u]) => u.split("?")[0] === ${JSON.stringify(p)}).map(([, b]) => b))`).then(JSON.parse);
let failed = 0;
function check(name, got, want) {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  failed += !ok;
  console.log(`${ok ? "✓" : "✗"} ${name}${ok ? "" : `\n    got  ${JSON.stringify(got)}\n    want ${JSON.stringify(want)}`}`);
}

// the stubbed server: answers from window.__replies by path prefix, records every call in window.__api
try {
await send("Page.enable");
await send("Emulation.setDeviceMetricsOverride", {width: 400, height: 860, deviceScaleFactor: 1, mobile: false});
await send("Fetch.enable", {patterns: [{urlPattern: "*api/image*"}, {urlPattern: "*api/skill-image*"}]});
await send("Page.addScriptToEvaluateOnNewDocument", {source: `
  window.__api = [];
  window.__replies = {};
  window.EventSource = class { constructor() { window.__es = this; } close() {} };
  window.__emit = (e) => window.__es.onmessage({data: JSON.stringify(e)});
  window.fetch = async (url, opts) => {
    __api.push([url, opts?.body ? JSON.parse(opts.body) : null]);
    const k = Object.keys(__replies).find((p) => url.startsWith(p));
    const body = k ? (typeof __replies[k] === "function" ? __replies[k](url) : __replies[k]) : {ok: true};
    return {ok: true, json: async () => body};
  };
  // the page's state and the composer's functions under the names the checks use (web/src/testHooks.ts)
  const live = (k, f) => Object.defineProperty(window, k, {get: f, configurable: true});
  live("ed", () => __t.editor()); live("menu", () => document.querySelector(".menu"));
  for (const k of ["view", "chat", "library", "S"]) live(k, () => __t.get()[k]);
  live("zoom", () => __t.zoom()); live("uploads", () => ({size: __t.get().uploads}));
  for (const f of ["segments", "insertChips", "placeCaret", "changed", "addFile", "addFiles", "clearDraft", "newChat", "loadRemarks", "openSkill", "pinned", "skillOf"])
    window[f] = (...a) => __t[f](...a);`});
await send("Page.navigate", {url: page});
await sleep(800);

const STATE = {doc: {path: "/d/x.figcraft", name: "x"}, selection: [], stale: false, running: [], chats: [], modes: ["figcraft", "terminal"],
  settings: {mode: "figcraft", agent: "claude", model: "claude-opus-5-5", shots: false},
  agents: [{id: "claude", name: "Claude Code", ok: true, path: "/bin/claude", version: "2.1", models: [{id: "claude-opus-5-5", name: "Opus 5.5"}]}]};
await js(`__emit({type: "state", state: ${JSON.stringify(STATE)}}); true`);

// Check the font Chromium actually uses for the text (the bundled Golos, not a system fallback); icons are SVG.
await js("document.fonts.ready.then(() => true)");
await send("DOM.enable"); await send("CSS.enable");
const rootNode = (await send("DOM.getDocument")).root.nodeId;
for (const [selector, font] of [["#docName", /Golos/], ["#chatTitle", /Golos/]]) {
  const {nodeId} = await send("DOM.querySelector", {nodeId: rootNode, selector});
  const {fonts} = await send("CSS.getPlatformFontsForNode", {nodeId});
  check(`text in ${selector} uses ${font.source}`, fonts.some(f => font.test(f.familyName) && f.glyphCount > 0), true);
}
check("icons are SVG", await js(`!!document.querySelector("#newBtn svg.g path") && !!document.querySelector("#pickerBtn .mark svg.g")`), true);

if (shot) {
  const r = await send("Page.captureScreenshot", {format: "png"});
  fs.writeFileSync(shot + ".icons.png", Buffer.from(r.data, "base64"));
}

// ---- composer: chips inline ----
const select = (list) => js(`__emit({type: "selection", selection: ${JSON.stringify(list)}}); true`);
await js("ed.focus(); true");
await select([{id: 12, name: "Heading", type: "FRAME", size: "320×40"}]);
check("selected layers are suggested above the input", await js("[document.querySelector('#selectionSuggestion .chip').textContent, document.getElementById('selectionSuggestion').compareDocumentPosition(document.getElementById('box')) & Node.DOCUMENT_POSITION_FOLLOWING]"), ["@Heading", 4]);
await type("Сделай");
await key("Tab", "Tab", 9);
check("Tab inserts the selection at the caret", await segs(), ["Сделай ", "[Heading]"]);
check("inserted layers leave the suggestion", await js("document.getElementById('selectionSuggestion') === null"), true);
await type("крупнее, как");
await select([{id: 34, name: "Grid", type: "FRAME", size: "600×400"}, {id: 56, name: "Title", type: "TEXT", size: "80×20"}]);
await js("const c = document.getElementById('selectionSuggestion'); c.dispatchEvent(new MouseEvent('mousedown', {bubbles: true})); c.click(); true");
check("a click inserts the new selection", await segs(), ["Сделай ", "[Heading]", " крупнее, как ", "[Grid]", " ", "[Title]"]);
await type("и выровняй");
for (let i = 0; i < 12; i++) await key("ArrowLeft", "ArrowLeft", 37);
await type("<");
check("← steps over a chip like one character", await segs(), ["Сделай ", "[Heading]", " крупнее, как ", "[Grid]", " <", "[Title]", " и выровняй"]);
await js("const r = document.createRange(); r.selectNodeContents(ed); r.collapse(false); placeCaret(r); true");
for (let i = 0; i < 12; i++) await key("Backspace", "Backspace", 8);
check("Backspace deletes a chip whole", await segs(), ["Сделай ", "[Heading]", " крупнее, как ", "[Grid]", " <"]);

// ---- @: layers and remarks ----
await js(`__replies["/api/search"] = (u) => ({indexing: false,
  layers: [{id: 77, name: "Button", type: "INSTANCE", path: "Окно › Footer"}],
  remarks: decodeURIComponent(u).includes("q=Bu") ? [] : [{num: 7, text: "Кнопка налезает на край", status: "open"}]}); true`);
await type(" по @Bu");
await sleep(400);
check("@ opens the search", await js("menu?.dataset.kind === 'mention' && [...menu.querySelectorAll('[data-k]')].map(b => [...b.children].map(c => c.textContent).join('|'))"), ["◇|Button|instance · Окно › Footer|↵"]);
await key("Enter", "Enter", 13);
check("Enter puts the layer in place of @query", await segs(), ["Сделай ", "[Heading]", " крупнее, как ", "[Grid]", " < по ", "[Button]"]);
await type("и @");
await sleep(400);
await key("ArrowDown", "ArrowDown", 40);
await key("ArrowDown", "ArrowDown", 40);
await key("Tab", "Tab", 9);
check("↓ and Tab pick a remark", await js("JSON.stringify(segments().filter(s => s.kind === 'remark').map(s => [s.num, s.label]))").then(JSON.parse),
      [[7, "#7 Кнопка налезает на край"]]);
check("no menu is left open", await js("menu === null"), true);

// ---- images ----
await js(`__replies["/api/upload"] = {path: "/state/images/a.png"};
  addFile(new File([new Uint8Array([137, 80, 78, 71])], "a.png", {type: "image/png"})).then(() => true)`);
check("a pasted image becomes a chip", await js("segments().filter(s => s.kind === 'image').map(s => s.path)"), ["/state/images/a.png"]);
check("and was uploaded as base64", (await calls("/api/upload"))[0].data.startsWith("data:image/png;base64,"), true);

// ---- send ----
const CHAT = {id: "c1", file: "/d/x.figcraft", title: "Сделай", agent: "claude", model: "claude-opus-5-5", updated: 1, messages: []};
await js(`__replies["/api/send"] = ${JSON.stringify(CHAT)}; true`);
await key("Enter", "Enter", 13);
await sleep(100);
const sent = (await calls("/api/send"))[0];
check("Enter sends the segments", sent.segments.map((s) => s.kind), ["text", "layer", "text", "layer", "text", "layer", "text", "remark", "text", "image"]);
check("the editor is emptied", await segs(), []);

// ---- a sent message, copied and pasted back: the same segments, chips and all ----
await js(`__emit({type: "chat", chat: ${JSON.stringify({...CHAT, messages: [{role: "user", segments: sent.segments}]})}}); true`);
const copied = await js(`(() => {
  const real = document.execCommand, dt = new DataTransfer();
  document.execCommand = () => document.dispatchEvent(new ClipboardEvent("copy", {clipboardData: dt, cancelable: true})) || true;
  document.querySelector(".umsg .copy").click();
  document.execCommand = real;
  document.getElementById("input").dispatchEvent(new ClipboardEvent("paste", {clipboardData: dt, bubbles: true, cancelable: true}));
  return dt.getData("text/plain");
})()`);
check("a copied message is text elsewhere", copied, "Сделай @Heading крупнее, как @Grid < по @Button и [#7 Кнопка налезает на край]");
check("and pastes back as the message", JSON.stringify(await js("segments()")), JSON.stringify(sent.segments));
await js("clearDraft(); true");

// ---- ×N: variants by an orchestrator and lanes ----
await js("document.getElementById('timesBtn').click(); true");
check("×N opens the variants menu at ×1", await js("[menu?.dataset.kind, !!menu.querySelector('.vnote'), document.getElementById('timesBtn').textContent]"), ["variants", true, "×1"]);
await js("menu.querySelector('[data-times=\"3\"]').click(); true");
check("×3: an orchestrator and three lanes", await js("[menu.querySelectorAll('.vrow[data-lane]').length, document.getElementById('timesBtn').textContent]"), [3, "×3"]);
await js("menu.querySelector('[data-vmodel=\"1\"]').click(); true");
await js("menu.querySelector('[data-pick-model]').click(); true");
await sleep(50);
check("a lane's agent and model are kept for every chat", (await calls("/api/settings")).pop(), {variants: {lanes: [null, {agent: "claude", model: "claude-opus-5-5"}]}});
check("and the menu is back at the lanes", await js("menu.querySelectorAll('.vrow[data-lane]').length"), 3);
await js(`__replies["/api/settings"] = (u) => ({variants: __api.filter(([x]) => x === "/api/settings").pop()[1].variants}); true`);
await js("menu.querySelector('[data-axis=structure]').click(); true");
await sleep(30);
check("what the lanes differ in", (await calls("/api/settings")).pop().variants.axis, "structure");
await js("menu.querySelector('[data-limit=\"20\"]').click(); true");
await sleep(30);
check("how long a lane may take", [(await calls("/api/settings")).pop().variants.limit, await js("menu.querySelector('[data-limit=\"20\"]').getAttribute('aria-checked')")], [20, "true"]);
await js("menu.querySelector('[data-preset-save]').click(); true");
await sleep(30);
check("a preset is named after who draws", (await calls("/api/settings")).pop().variants.presets.map((p) => [p.name, p.count, p.axis]), [["Claude ×3", 3, "structure"]]);
await js("menu.querySelector('[data-times=\"2\"]').click(); menu.querySelector('[data-preset]').click(); true");
check("a preset brings its count back", await js("document.getElementById('timesBtn').textContent"), "×3");
if (shot) { const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".variants.png", Buffer.from(r.data, "base64")); }
await key("Escape", "Escape", 27);
await js("ed.focus(); true");
await type("Главная");
await key("Enter", "Enter", 13);
await sleep(100);
check("the message asks for ×3, then ×N is back at 1", [(await calls("/api/send")).pop().variants, await js("document.getElementById('timesBtn').textContent")], [3, "×1"]);
const LANES = {...CHAT, messages: [
  {role: "user", text: "Главная", segments: [{kind: "text", text: "Главная"}], times: 3},
  {role: "assistant", agent: "claude", model: "claude-opus-5-5", parts: [{kind: "text", text: "План"}], variants: {run: "r1", count: 2, frames: [11, 12]}},
  {role: "assistant", agent: "claude", model: "claude-opus-5-5", running: true, parts: [{kind: "step", id: "a", label: "build · Hero", status: "run"}],
   lane: {run: "r1", n: 1, of: 2, title: "Журнал", styleTitle: "Almanac", frame: 11}},
  {role: "assistant", agent: "claude", model: "claude-opus-5-5", parts: [], took: 200, changes: {steps: 4, top: [], ids: [12]},
   lane: {run: "r1", n: 2, of: 2, title: "Инструмент", frame: 12}}]};
await js(`__emit({type: "running", running: [{chat: "c1", file: "/d/x.figcraft", lane: 1}]}); __emit({type: "chat", chat: ${JSON.stringify(LANES)}}); true`);
check("lanes are cards: who, direction, style, frame", await js("[...document.querySelectorAll('.lane')].map(l => [l.className, l.querySelector('.idea').textContent, l.querySelector('.lmeta').textContent])"),
      [["lane run", "Журнал", "Opus 5.5Almanac#11"], ["lane done", "Инструмент", "Opus 5.5#12"]]);
check("a running lane shows its step, a finished one its own undo", await js("[!!document.querySelector('.lane.run .step'), [...document.querySelectorAll('.lane.done .lfoot button')].map(b => b.textContent)]"),
      [true, ["Подробнее", "Показать", "Отменить"]]);
check("the working row counts the lanes", await js("document.getElementById('working').textContent.startsWith('Работают 1 дорожка')"), true);
check("the message says ×3", await js("document.querySelector('.times-note').textContent"), "×3 варианта · оркестратор и дорожки");
if (shot) { const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".lanes.png", Buffer.from(r.data, "base64")); }
await js("document.querySelector('.lane.done [data-act=undo]').click(); true");
await sleep(50);
check("undo goes to the lane's own answer", (await calls("/api/undo")).pop(), {chat: "c1", index: 3});
// VF–VI: what comes after a lane
check("a finished lane can be refined or taken", await js("[...document.querySelectorAll('.lane.done .lnext button')].map(b => b.textContent)"), ["Доработать", "Беру этот"]);
check("the run's bar counts the lanes still working", await js("[document.querySelectorAll('.runbar').length, document.querySelector('.runbar .rhead').textContent]"), [1, "Варианты ×2работают 1"]);
await js(`__replies["/api/lane"] = ${JSON.stringify(LANES)}; __replies["/api/pick"] = ${JSON.stringify(LANES)}; __replies["/api/compare"] = ${JSON.stringify(LANES)}; true`);
await js("document.querySelector('.lane.done [data-lane-act=more]').click(); true");
check("«Доработать» aims the next message at the lane", await js("document.getElementById('laneTarget').textContent"), "В вариант 2 · ИнструментOpus 5.5×");
await type("плотнее");
await key("Enter", "Enter", 13);
await sleep(50);
check("it goes into the lane at once, not into the queue", [(await calls("/api/lane")).pop(), await js("!!document.getElementById('laneTarget')"), await js("__t.get().queued.c1?.length || 0")],
      [{chat: "c1", run: "r1", n: 2, kind: "more", segments: [{kind: "text", text: "плотнее"}]}, false, 0]);
await js("document.querySelector('.lane.done [data-lane-act=pick]').click(); true");
await sleep(50);
check("«Беру этот» keeps that one", (await calls("/api/pick")).pop(), {chat: "c1", run: "r1", n: 2});
const BROKEN = {...LANES, messages: [...LANES.messages.slice(0, 2),
  {...LANES.messages[2], running: false, error: "Codex: лимит запросов исчерпан", parts: []}, LANES.messages[3],
  {role: "user", text: "плотнее", segments: [{kind: "text", text: "плотнее"}], toLane: {run: "r1", n: 2, title: "Инструмент"}},
  {...LANES.messages[3], lane: {...LANES.messages[3].lane, kind: "more", note: "плотнее"}, cost: 0.5},
  {role: "user", auto: true, text: "сравни", segments: []}, {role: "assistant", agent: "claude", parts: [{kind: "text", text: "Беру 2"}], compare: "r1", cost: 0.25}]};
BROKEN.messages[1] = {...BROKEN.messages[1], cost: 0.1, variants: {...BROKEN.messages[1].variants, started: 1000, ended: 1660}};
await js(`__emit({type: "running", running: []}); __emit({type: "chat", chat: ${JSON.stringify(BROKEN)}}); true`);
check("a message into a lane says so", await js("document.querySelector('.to-lane').textContent"), "в вариант 2 · Инструмент");
check("a refinement is a card of its own", await js("[...document.querySelectorAll('.lane .idea')].map(x => x.textContent)"), ["Журнал", "Инструмент", "Доработка · Инструмент"]);
check("only the latest attempt of a lane acts", await js("[...document.querySelectorAll('.lane')].map(l => !!l.querySelector('.lnext'))"), [true, false, true]);
check("a broken lane runs again, by any agent", await js("[document.querySelector('.lane.error .lnext select').value, document.querySelector('.lane.error [data-lane-act=retry]').textContent]"),
      ["claude/claude-opus-5-5", "Повторить"]);
await js("document.querySelector('.lane.error [data-lane-act=retry]').click(); true");
await sleep(50);
check("«Повторить» sends the agent and model", (await calls("/api/lane")).pop(), {chat: "c1", run: "r1", n: 1, kind: "retry", agent: "claude", model: "claude-opus-5-5"});
await js(`__emit({type: "chat", chat: ${JSON.stringify(BROKEN)}}); true`);  // the stub answered with the running chat
check("one bar under the run's last answer: time and cost", await js("[document.querySelectorAll('.runbar').length, document.querySelector('#main > :last-child').className, document.querySelector('.runbar .rhead').textContent]"),
      [1, "runbar", "Варианты ×2 · 11 мин$0.85 · Claude Code без цены"]);
check("before a pick: mix or compare again", await js("[...document.querySelectorAll('.runbar .row button')].map(b => b.textContent)"), ["Смешать…", "Сравнить снова"]);
await js("document.querySelector('[data-run-act=mix]').click(); true");
check("«Смешать…» drafts the message to the orchestrator", await segs(), ["Смешай варианты в новой рамке: из 1 «Журнал» — …; из 2 «Инструмент» — …"]);
await js("clearDraft(); document.querySelector('[data-run-act=compare]').click(); true");
await sleep(50);
check("«Сравнить снова»", (await calls("/api/compare")).pop(), {chat: "c1", run: "r1"});
const PICKED = {...BROKEN, messages: BROKEN.messages.map((m, i) => i === 1 ? {...m, variants: {...m.variants, picked:
  {n: 2, title: "Инструмент", frame: 12, frames: [11], collections: 1, styles: 3, collection: "Инструмент", ownStyles: 2}}} : m)};
await js(`__emit({type: "chat", chat: ${JSON.stringify(PICKED)}}); true`);
check("after a pick: what went, and carry it on", await js("[document.querySelector('.runbar .caption').textContent, [...document.querySelectorAll('.runbar .row button')].map(b => b.textContent), !!document.querySelector('[data-lane-act=pick]')]"),
      ["Взят вариант 2 «Инструмент»: убрано: 1 рамка, 1 коллекция, 3 стиля; «Инструмент» теперь коллекция файла.", ["Перенести на экраны", "Адаптив", "Отменить"], false]);
if (shot) { const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".picked.png", Buffer.from(r.data, "base64")); }
await js("document.querySelector('[data-run-act=spread]').click(); true");
await sleep(50);
check("«Перенести на экраны» goes to the winner's lane", (await calls("/api/lane")).pop(), {chat: "c1", run: "r1", n: 2, kind: "spread"});
await js(`window.__api = __api.filter(([u]) => !["/api/undo", "/api/lane", "/api/pick", "/api/compare"].includes(u)); true`);

// ---- an answer: streaming, changes, denials ----
const reply = (parts, extra = {}) => ({...CHAT, messages: [{role: "user", text: "x", segments: [{kind: "text", text: "x"}]},
  {role: "assistant", agent: "claude", model: "claude-opus-5-5", parts, ...extra}]});
await js(`__emit({type: "running", running: [{chat: "c9", file: "/d/other.figcraft"}]}); true`);
check("agents in other files are named", await js("document.getElementById('banner').textContent.includes('Агенты работают ещё в 1 файле')"), true);
await js(`__emit({type: "running", running: [{chat: "c1", file: "/d/x.figcraft"}]});
  __emit({type: "chat", chat: ${JSON.stringify(reply([{kind: "text", text: "Смотр", streaming: true}], {running: true}))}}); true`);
check("streaming text shows a cursor", await js("!!document.querySelector('.text.streaming')"), true);
check("stopping is its own button; send queues", await js("[!!document.getElementById('stopBtn'), document.getElementById('sendBtn').classList.contains('stop')]"), [true, false]);
await key("Escape", "Escape", 27);
check("one Esc only arms the stop", [(await calls("/api/stop")).length, await js("document.getElementById('stopBtn').textContent.startsWith('Esc ещё раз')")], [0, true]);
await key("Escape", "Escape", 27);
check("the second Esc stops the agent", await calls("/api/stop"), [{chat: "c1"}]);
await select([{id: 91, name: "Выделенная область с очень длинным названием для проверки переноса", type: "FRAME"}, {id: 92, name: "Footer", type: "FRAME"}]);
check("selection suggestions remain visible while the agent works", await js("[document.querySelectorAll('#selectionSuggestion .chip').length, document.getElementById('working').textContent.includes('Работает'), document.documentElement.scrollWidth <= innerWidth]"), [2, true, true]);
if (shot) { const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".selection.png", Buffer.from(r.data, "base64")); }
await js("document.getElementById('selectionSuggestion').click(); true");
check("suggestion clicks insert layers during a turn", await segs(), ["[Выделенная область с очень длинным названием для проверки переноса]", " ", "[Footer]"]);
await js("clearDraft(); true");
check("removing chips restores the suggestion", await js("document.querySelectorAll('#selectionSuggestion .chip').length"), 2);
await select([]);
check("clearing the FigCraft selection hides the suggestion", await js("document.getElementById('selectionSuggestion') === null"), true);
await js(`__emit({type: "running", running: []});
  __emit({type: "chat", chat: ${JSON.stringify(reply([{kind: "step", id: "t", label: "set_properties", status: "ok", mut: true, ids: [5]},
    {kind: "text", text: "Готово"}], {running: false, changes: {steps: 2, top: ["a", "b"], ids: [5]},
    denied: [{tool: "Bash", label: "Bash · ls"}]}))}}); true`);
check("remarks the agent marked", await js(`__emit({type: "chat", chat: ${JSON.stringify(reply([{kind: "text", text: "✓ #3 ок"}], {running: false, marked: [{num: 3, status: "review"}]}))}});
  [...document.querySelectorAll('.changes')].map(c => c.textContent.replace(/\\s+/g, ' ').trim())`), ["✓#3 → ПроверьЗамечания ›"]);
await js(`__emit({type: "chat", chat: ${JSON.stringify(reply([{kind: "text", text: "Готово"}], {running: false, cost: 2.76821, took: 380,
  usage: {input: 42, output: 17100, cacheRead: 2200000, cacheWrite: 119700, turns: 21, context: 131100, window: 1000000}, phases: {prep: 2.4, first: 6.1}}))}}); true`);
check("what the turn took, folded", await js("[document.querySelector('.stats summary').textContent, document.querySelector('.stats').open]"), ["Работал 6 мин 20 с · $2.77", false]);
await js("document.querySelector('.stats summary').click(); true");
await sleep(50);
check("its numbers", await js("[...document.querySelectorAll('.stats dt, .stats dd')].map(e => e.textContent)"),
  ["Стоимость", "$2.77", "Входящие токены", "2.3M", "Исходящие токены", "17.1k", "Чтение кэша", "2.2M", "Запись в кэш", "119.7k",
   "Контекст", "131.1k из 1.0M", "Запросов к модели", "21", "Подготовка", "2.4 с", "До первого ответа", "6.1 с"]);
await js(`__emit({type: "chat", chat: ${JSON.stringify(reply([{kind: "text", text: "Ещё"}], {running: false, took: 5, usage: {output: 3}}))}}); true`);
check("the next answer stays open", await js("[document.querySelector('.stats').open, document.querySelector('.stats summary').textContent]"), [true, "Работал 5 с"]);
await js(`__emit({type: "chat", chat: ${JSON.stringify(reply([{kind: "text", text: "Старый"}], {running: false, cost: 1.5}))}}); true`);
check("an older answer still shows its cost", await js("document.querySelector('.stats summary').textContent"), "Готово · $1.50");
if (shot) { await js(`__emit({type: "chat", chat: ${JSON.stringify(reply([{kind: "text", text: "Готово"}], {running: false, cost: 2.76821, took: 380, usage: {input: 42, output: 17100, cacheRead: 2200000, cacheWrite: 119700, turns: 21, context: 131100, window: 1000000}}))}}); true`); const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".stats.png", Buffer.from(r.data, "base64")); }
check("a small context says nothing", await js("!!document.querySelector('.bigctx')"), false);
await js(`__emit({type: "chat", chat: ${JSON.stringify(reply([{kind: "text", text: "Перерисовал 14 экранов."}], {running: false, usage: {output: 9, context: 341167, window: 1000000}}))}}); true`);
check("a big one offers a new chat", await js("document.querySelector('.bigctx b').textContent"), "Контекст 341.2k");
if (shot) { const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".bigctx.png", Buffer.from(r.data, "base64")); }
await js("document.querySelector('[data-act=fresh]').click(); true");
await sleep(50);
check("which starts with what was done", await js("[chat, segments().map(s => s.text).join('')]").then(([c, t]) => [c, t.includes("Что сделано в прошлом чате:") && t.includes("Перерисовал 14 экранов.") && t.trim().endsWith("Дальше:")]), [null, true]);
await js(`clearDraft(); __t.set({chat: ${JSON.stringify(CHAT)}}); true`);  // back to the chat the next checks answer in
await js(`__emit({type: "chat", chat: ${JSON.stringify(reply([{kind: "step", id: "t", label: "set_properties", status: "ok", mut: true, ids: [5]},
    {kind: "text", text: "Готово"}], {running: false, changes: {steps: 2, top: ["a", "b"], ids: [5]},
    denied: [{tool: "Bash", label: "Bash · ls"}]}))}}); true`);
check("the changes bar", await js("document.querySelector('.changed .chead').textContent.replace(/\\s+/g, ' ').trim()"), "Изменено на холсте2 шагаПоказатьОтменить");
await js("document.querySelector('[data-act=undo]').click(); document.querySelector('[data-act=show]').click(); true");
await sleep(50);
check("Отменить and Показать name the answer", [await calls("/api/undo"), await calls("/api/show")], [[{chat: "c1", index: 1}], [{chat: "c1", index: 1}]]);
await js("document.querySelector('[data-act=allow]').click(); true");
await sleep(50);
check("the denial offers to allow and go on", await calls("/api/allow"), [{chat: "c1", tools: ["Bash"]}]);
await js(`__t.set({chat: ${JSON.stringify(reply([{kind: "text", text: "Готово"}], {running: false, denied: [{tool: "Bash", label: "Bash · ls"}]}))}}); ed.focus(); true`);
await key("Enter", "Enter", 13);
await sleep(50);
check("↵ in an empty input grants nothing", (await calls("/api/allow")).length, 1);

// ---- a broken turn, a chat's actions, settings from the keyboard ----
await js(`__t.set({chat: ${JSON.stringify(reply([{kind: "step", id: "a", label: "set_properties", status: "ok"}, {kind: "step", id: "b", label: "set_properties", status: "error"}],
  {running: false, error: "FigCraft не ответил за 30 с"}))}}); true`);
check("a broken turn says where it stopped and goes on from there", await js("[document.querySelector('.notice b').textContent, document.querySelector('[data-act=continue]').textContent]"),
      ["Ход прервался на шаге 2", "Продолжить с шага 2"]);
await js(`__t.set({chat: ${JSON.stringify(reply([], {running: false, error: "Claude usage limit reached"}))}}); true`);
check("a spent limit offers another model", await js("[document.querySelector('.notice').classList.contains('warn'), !!document.querySelector('[data-act=model]')]"), [true, true]);
await js(`__t.set({chat: null}); __replies["/api/rename"] = ${JSON.stringify({...CHAT, title: "Кнопки"})};
  document.getElementById('chatsBtn').click(); menu.querySelector('[data-more-chat=c1]').click(); true`);
await sleep(20); await js("menu.querySelector('[data-chat-act=rename]').click(); true"); await sleep(20);
await js("const f = menu.querySelector('[data-rename]'); f.value = 'Кнопки'; f.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', bubbles: true})); true");
await sleep(50);
check("a chat is renamed in place", [(await calls("/api/rename")).at(-1), await js("S.chats.find(c => c.id === 'c1').title")], [{chat: "c1", title: "Кнопки"}, "Кнопки"]);
await js("if (!menu) document.getElementById('chatsBtn').click(); menu.querySelector('[data-more-chat=c1]').click(); true"); await sleep(20);
await js("menu.querySelector('[data-del=c1]').click(); true");
check("deleting hides the chat and waits with «Вернуть»", [await js("document.querySelector('#toasts .toast:last-child button').textContent"), (await calls("/api/delete")).length], ["Вернуть", 0]);
await js("document.querySelector('#toasts .toast:last-child button').click(); document.getElementById('chatsBtn').click(); true");
check("«Вернуть» keeps it", await js("[!!menu.querySelector('[data-id=c1]'), __t.get().gone]"), [true, []]);
await key("Escape", "Escape", 27);
await key(",", "Comma", 188, 2);
check("Ctrl+, opens the settings", await js("!document.getElementById('settings').hidden"), true);
await key("Escape", "Escape", 27);
await key("б", "Comma", 188, 2);
check("settings shortcut works in the Russian layout", await js("!document.getElementById('settings').hidden"), true);
await key("Escape", "Escape", 27);
await js(`__t.set({chat: ${JSON.stringify(CHAT)}}); ed.focus(); document.dispatchEvent(new KeyboardEvent('keydown', {key: 'ν', code: 'KeyN', ctrlKey: true, bubbles: true})); true`);
check("new chat shortcut uses the physical key in other layouts", await js("chat === null && document.activeElement === ed"), true);
await key(",", "Comma", 188, 2);
await key("Escape", "Escape", 27);
await js(`__t.set({chat: null, S: {...S, chats: S.chats.map(c => ({...c, title: "Сделай"}))}}); document.querySelectorAll(".toast").forEach(t => t.remove()); true`);

// ---- remarks ----
const R = [
  {num: 3, text: "Какой отступ у карточки?", status: "question", layer: 1, name: "Card", page: "Главная", replies: [["Claude", "q"]],
   question: "16 или 24?", options: ["16", "24"], before: false, after: ""},
  {num: 4, text: "Заголовок крупнее", status: "review", layer: 2, name: "Title", page: "Главная", replies: [["Claude", "22 → 28"]],
   question: "", options: [], before: true, after: "abc"},
  {num: 5, text: "Иконка мелкая", status: "open", layer: 3, name: "Icon", page: "Главная", replies: [], question: "", options: [], before: true, after: ""},
  {num: 1, text: "Цвет фона", status: "done", layer: 4, name: "Bg", page: "Главная", replies: [], question: "", options: [], before: false, after: ""}];
await js(`__replies["/api/remarks"] = {remarks: ${JSON.stringify(R)}}; loadRemarks().then(() => true)`);
check("the title says what waits", await js("[document.getElementById('badge').textContent, document.getElementById('badge').title]"), ["2", "2 ждёт ответа"]);
check("the start card counts the remarks", await js("document.querySelector('[data-start=\"0\"] small').textContent"), "1 открыто · 2 ждёт ответа");
await js("document.getElementById('chatsBtn').click(); true");
check("the title opens the remarks and the chats", await js("[...menu.querySelectorAll('[data-remarks], [data-id]')].map(r => r.querySelector('.grow').firstChild.textContent)"), ["Замечания", "Сделай"]);
await js("menu.querySelector('[data-remarks]').click(); true");
await sleep(100);
check("groups by what they wait for, the closed ones folded", await js("[...document.querySelectorAll('#remarks .rgroup')].map(g => g.textContent.trim())"),
      ["Открыто1", "Ждёт вашего ответа1", "Проверь1", "Закрыто1"]);
check("the remarks' own top bar", await js("[document.getElementById('chatTitle').textContent, document.getElementById('fixAll').hidden, document.getElementById('newBtn').hidden]"), ["Замечания", false, true]);
check("a question shows its options; the selected open remark its actions", await js("[document.querySelectorAll('[data-opt]').length, !!document.querySelector('[data-fix]'), document.querySelectorAll('.shots img').length]"), [2, true, 0]);
await js("document.activeElement.blur(); true");
await key("ArrowDown", "ArrowDown", 40);
await press("2");
await key("ArrowDown", "ArrowDown", 40);
check("the review opens with было/стало", await js("[...document.querySelectorAll('.shots img')].map(i => i.getAttribute('src'))"),
      ["/api/shot?num=4&kind=before&key=", "/api/shot?num=4&kind=after&key=abc"]);
await key("Enter", "Enter", 13);
await sleep(50);
check("↓ 2 answers the question, ↓ Enter accepts the review", await calls("/api/remark"), [{num: 3, action: "answer", text: "24"}, {num: 4, action: "accept"}]);
await js("document.querySelector('[data-back]').click(); true");
await type("всё ещё мелко");
await key("Enter", "Enter", 13);
await sleep(50);
check("Вернуть sends the remark back with a comment, and only that", (await calls("/api/remark")).slice(2), [{num: 4, action: "reopen", text: "всё ещё мелко"}]);
await js("document.getElementById('fixAll').click(); true");
await sleep(50);
check("Отдать агенту sends the open remarks", (await calls("/api/send")).at(-1).segments.map((s) => s.kind), ["remarks", "text"]);
check("and goes to the chat", await js("view"), "chat");

// ---- FigCraft's comment threads under the remarks ----
const C = [{id: 11, text: "@Claude кнопка мелкая", author: "Тёма", page: "Главная", frame: "Шапка", replies: 0, last: null, answered: false, unread: true, mentions: ["Claude"]},
  {id: 12, text: "Заголовок жирнее", author: "Тёма", page: "Главная", frame: "", replies: 1, last: ["Claude (agent)", "Сделал Bold"], answered: true, unread: false, mentions: []}];
await js(`__replies["/api/remarks"] = {remarks: ${JSON.stringify(R)}, comments: ${JSON.stringify(C)}}; loadRemarks().then(() => true)`);
check("an answered thread waits for you too", await js("document.getElementById('badge').textContent"), "3");
await js("__t.set({view: 'remarks'}); true");
await sleep(100);
check("the threads follow the remarks, the answered one first", await js("[document.querySelector('#remarks .rgroup.comments').textContent, [...document.querySelectorAll('[data-comment]')].map(c => c.dataset.comment), document.querySelector('[data-comment=\"12\"] .says').textContent]"),
      ["Комментарии FigCraft2", ["12", "11"], "Claude (agent): Сделал Bold"]);
if (shot) { const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".comments.png", Buffer.from(r.data, "base64")); }
await js("document.querySelector('[data-comment=\"12\"] .primary').click(); true");
await js("document.querySelector('[data-comment=\"11\"] [data-reply-open]').click(); true");
await sleep(50);
await type("про левую");
await key("Enter", "Enter", 13);
await sleep(50);
check("Решить and a reply in the thread", await calls("/api/comment"), [{id: 12, action: "resolve"}, {id: 11, action: "reply", text: "про левую"}]);
await js("document.querySelector('[data-comment=\"11\"] .primary').click(); true");
await sleep(50);
check("Исправить hands the thread to the agent", (await calls("/api/send")).at(-1).segments.map((s) => [s.kind, s.id ?? null]), [["comment", 11], ["text", null]]);
await js(`__replies["/api/remarks"] = {remarks: ${JSON.stringify(R)}}; loadRemarks().then(() => true)`);

// ---- skills: / ticks some for the message, Ctrl+Enter pins one in the chat, the answer names them ----
const SK = [{name: "figcraft-design", title: "figcraft-design", summary: "продуктовый UI", group: "base", mode: "always", source: "builtin"},
  {name: "graphite", title: "Graphite", summary: "тихий", group: "style", mode: "manual", source: "builtin", preview: {colors: ["#1C1D21"]}},
  {name: "paper", title: "Paper", summary: "светлый", group: "style", mode: "manual", source: "project"},
  {name: "android", title: "Android", summary: "360 dp", group: "platform", mode: "auto", source: "mine"},
  {name: "better-typography", title: "better-typography", summary: "шкала", group: "quality", mode: "auto", source: "builtin"}];
await js(`__t.set({view: "chat"});
  __emit({type: "state", state: ${JSON.stringify({...STATE, skills: SK, skillDefaults: []})}}); ed.innerHTML = ""; changed(); ed.focus(); true`);
check("a new chat: nothing pinned, no row", await js("chat === null && document.getElementById('pinnedBtn').hidden"), true);
await type("см. a/b");
check("/ inside a word is text", await js("menu?.dataset.kind ?? null"), null);
await js(`ed.innerHTML = ""; changed(); ed.focus(); true`);
await type("Экран входа /");
const menuItems = () => js("[...menu.querySelectorAll('[data-skill-title]')].map(b => b.textContent)");
check("/ lists the skills to choose (not the always-on ones), by group", [await js("menu?.dataset.kind"), await menuItems(),
  await js("[...menu.querySelectorAll('.head')].map(h => h.firstChild.textContent.trim())")],
  ["slash", ["Graphite", "Paper", "Android", "better-typography"], ["Стиль", "Платформа", "Качество"]]);
await key(" ", "Space", 32);
await key("ArrowDown", "ArrowDown", 40);
await key(" ", "Space", 32);
check("Space keeps multiple styles, with their chips before /", await segs(), ["Экран входа ", "[Graphite]", " ", "[Paper]", " /"]);
await key("ArrowDown", "ArrowDown", 40);
await key("Enter", "Enter", 13, 2);
await sleep(50);
check("Ctrl+Enter pins it in the chat-to-be", [await js("pinned()"), await js("document.getElementById('pinnedBtn').textContent")],
      [["android"], "Закреплено в чатеAndroid⌃"]);
await key("Enter", "Enter", 13);
check("Enter closes the menu and takes the /", [await js("menu"), await segs()], [null, ["Экран входа ", "[Graphite]", " ", "[Paper]"]]);
const CHAT2 = {...CHAT, id: "c2", skills: ["android"], autoSkills: true};
await js(`__replies["/api/send"] = ${JSON.stringify(CHAT2)}; true`);
await key("Enter", "Enter", 13);
await sleep(100);
const sent2 = (await calls("/api/send")).at(-1);
check("the new chat starts with the pinned skills, the message carries its own",
      [sent2.skills, sent2.autoSkills, sent2.segments.filter((x) => x.kind === "skill").map((x) => [x.name, x.group])],
      [["android"], true, [["graphite", "style"], ["paper", "style"]]]);
await js(`__emit({type: "chat", chat: ${JSON.stringify({...CHAT2, messages: [{role: "user", text: "x", segments: [{kind: "text", text: "x"}]},
  {role: "assistant", agent: "claude", model: "claude-opus-5-5", parts: [{kind: "text", text: "Готово"}], skills: [
    {name: "figcraft-design", title: "figcraft-design", group: "base", level: "always"}, {name: "android", title: "Android", group: "platform", level: "chat"},
    {name: "paper", title: "Paper", group: "style", level: "message"}, {name: "better-ui", title: "better-ui", group: "quality", level: "auto"}]}]})}}); true`);
check("the answer names its skills and why", await js("document.querySelector('.skills').textContent.replace(/\\s+/g, ' ').trim()"),
      "Навыкиfigcraft-designAndroidPaperbetter-uiсам");
await js(`__replies["/api/skills"] = ${JSON.stringify({...CHAT2, skills: []})}; document.querySelector('#pinnedBtn b').click(); true`);
check("the pinned row opens the chat's skills", await js("menu?.dataset.kind + ': ' + [...menu.querySelectorAll('.item .t')].map(g => g.textContent.trim()).join(', ')"),
      "pinned: figcraft-design, Android, Добавить навык, Агент может взять ещё");
await js("menu.querySelector('[data-unpin]').click(); true");
await sleep(50);
check("× unpins it", [(await calls("/api/skills")).at(-1), await js("document.getElementById('pinnedBtn').hidden")],
      [{chat: "c2", skills: []}, true]);
const MANY = Array.from({length: 10}, (_, k) => ({name: `s${k}`, title: `S${k}`, summary: "тема", description: k === 7 ? "Cobalt: api, sdk" : "paper",
  group: "style", mode: "manual", source: "builtin"}));
await js(`__emit({type: "state", state: ${JSON.stringify({...STATE, skills: [...SK.slice(0, 3), ...MANY, ...SK.slice(3)], skillDefaults: []})}});
  ed.innerHTML = ""; changed(); ed.focus(); true`);
await type("/");
const moreRow = () => js("[...menu.querySelectorAll('[data-more]')].map(b => b.textContent.replace(/\\s+/g, ' ').trim())");
check("a big group shows five and «ещё N»", [(await menuItems()).length, await moreRow()], [7, ["Ещё 7прокрутите или нажмите ↓"]]);
await js("menu.querySelector('[data-more]').click(); true");
check("«ещё» shows the whole group", [(await menuItems()).length, await moreRow()], [14, []]);
await key("Escape", "Escape", 27);
await js("clearDraft(); ed.focus(); true"); await type("/");
for (let i = 0; i < 5; i++) await key("ArrowDown", "ArrowDown", 40);
check("moving below the fifth row reveals and selects the sixth skill", await js("[__t.get().slash.items.length, __t.get().slash.items[__t.get().slash.i].name]"), [14, "s3"]);
await key("Escape", "Escape", 27);
await js("clearDraft(); ed.focus(); true"); await type("/");
await js("menu.querySelector('.slash-list').dispatchEvent(new WheelEvent('wheel', {deltaY: 100, bubbles: true})); true");
check("scrolling down reveals the remaining skills without clicking More", [(await menuItems()).length, await moreRow()], [14, []]);
await type("sdk");
check("a query of three letters finds a skill by its description too", await menuItems(), ["S7"]);
await key("Escape", "Escape", 27);

// ---- model picker: agent tabs, filtering, selection and keyboard ----
const MODEL_STATE = {...STATE, agents: [
  {...STATE.agents[0], models: [{id: "claude-fable-5-1", name: "Fable 5.1"}, {id: "claude-opus-5-5", name: "Opus 5.5"},
    {id: "claude-sonnet-5-5", name: "Sonnet 5.5"}, {id: "claude-haiku-5-5", name: "Haiku 5.5"}]},
  {id: "codex", name: "Codex", ok: true, models: [{id: "gpt-6.1-sol", name: "GPT-6.1 Sol"}]},
  {id: "pi", name: "pi", ok: true, models: []}, {id: "offline", name: "Offline", ok: false, models: []}]};
await js(`__emit({type: "state", state: ${JSON.stringify(MODEL_STATE)}}); clearDraft(); ed.focus(); true`);
await type("Сохрани этот черновик");
await key("Tab", "Tab", 9);
check("Tab changes the agent without leaving the draft", await js("[S.settings.agent, S.settings.model, ed.textContent, document.activeElement === ed]"), ["codex", "gpt-6.1-sol", "Сохрани этот черновик", true]);
await key("Tab", "Tab", 9, 8);
check("Shift+Tab restores the previous agent and its model", await js("[S.settings.agent, S.settings.model]"), ["claude", "claude-opus-5-5"]);
await key("Tab", "Tab", 9); await key("Tab", "Tab", 9);
check("Tab reaches pi even when it uses its default model", await js("[S.settings.agent, S.settings.model ?? null]"), ["pi", null]);
await key("Tab", "Tab", 9);
check("Tab wraps through agents and remembers Claude's model", await js("[S.settings.agent, S.settings.model]"), ["claude", "claude-opus-5-5"]);
await key("Tab", "Tab", 9, 8);
check("reverse agent cycling wraps too", await js("S.settings.agent"), "pi");
await select([{id: 123, name: "Selected", type: "FRAME"}]);
await key("Tab", "Tab", 9);
check("selected layers take priority over agent cycling", await js("[S.settings.agent, segments().filter(s => s.kind === 'layer').map(s => s.id)]"), ["pi", [123]]);
await select([]);
await js(`clearDraft(); __t.set({S: ${JSON.stringify(MODEL_STATE)}}); document.getElementById('pickerBtn').focus(); true`);
await key("Tab", "Tab", 9);
check("Tab also cycles agents from the model button", await js("[S.settings.agent, S.settings.model, document.activeElement.id]"), ["codex", "gpt-6.1-sol", "pickerBtn"]);
await key("Tab", "Tab", 9, 8);
await js("ed.focus(); true");
const pickerRect = await js("(() => {const r = document.getElementById('pickerBtn').getBoundingClientRect(); return {x: r.x + r.width / 2, y: r.y + r.height / 2};})()");
await send("Input.dispatchMouseEvent", {type: "mouseMoved", ...pickerRect});
await sleep(400);
check("model hover explains the agent and both shortcuts without overflowing", await js("(() => {const t = document.getElementById('modelTooltip'), r = t.getBoundingClientRect(); return [getComputedStyle(t).visibility, t.textContent.includes('Claude Code'), t.textContent.includes('Shift+Tab'), r.left >= 0 && r.right <= innerWidth];})()"), ["visible", true, true, true]);
if (shot) { const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".model-hover.png", Buffer.from(r.data, "base64")); }
await send("Input.dispatchMouseEvent", {type: "mouseMoved", x: 1, y: 1});
await js("document.getElementById('pickerBtn').click(); true");
check("Linux shortcuts use Ctrl instead of the Mac glyph", await js("document.querySelector('#toSettings kbd').textContent"), "Ctrl+,");
await key("Tab", "Tab", 9);
check("Tab in the picker switches the agent tab", await js("[menu.querySelector('[aria-selected=true]').dataset.agent, document.activeElement.dataset.agent, S.settings.agent]"), ["codex", "codex", "claude"]);
await key("Tab", "Tab", 9);
check("Tab reaches an agent with no listed models", await js("[menu.querySelector('[aria-selected=true]').dataset.agent, menu.querySelector('.model-list').textContent]"), ["pi", "Модели не найдены"]);
await key("Tab", "Tab", 9, 8);
check("Shift+Tab returns to the previous agent tab", await js("menu.querySelector('[aria-selected=true]').dataset.agent"), "codex");
await key("ArrowDown", "ArrowDown", 40);
check("arrows select a model within the agent tab", await js("document.activeElement.dataset.model"), "gpt-6.1-sol");
await key("Enter", "Enter", 13);
check("Enter confirms the agent and model selected with Tab and arrows", await js("[S.settings.agent, S.settings.model, menu]"), ["codex", "gpt-6.1-sol", null]);
await js(`__t.set({S: ${JSON.stringify(MODEL_STATE)}}); document.getElementById('pickerBtn').click(); true`);
check("picker has agent tabs and selected model", await js("[menu.querySelectorAll('[role=tab]').length, menu.querySelector('[aria-pressed=true]').dataset.model]"), [3, "claude-opus-5-5"]);
check("model descriptions follow the design", await js("menu.querySelector('[data-model=claude-opus-5-5] small').textContent"), "Для экранов и дизайн-системы");
if (shot) { const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".models.png", Buffer.from(r.data, "base64")); }
await type("no-such-model");
check("picker shows an empty search", await js("menu.querySelector('.model-list').textContent"), "Модели не найдены");
await js("menu.querySelector('input').value = ''; menu.querySelector('input').dispatchEvent(new Event('input', {bubbles: true})); menu.querySelector('[data-agent=codex]').click(); true");
check("agent tab filters its models without selecting", await js("[menu.querySelectorAll('[data-model]').length, S.settings.agent]"), [1, "claude"]);
await js("menu.querySelector('input').focus(); true");
await key("ArrowDown", "ArrowDown", 40); await key("Enter", "Enter", 13);
check("keyboard selects a model for sending", await js("[S.settings.agent, S.settings.model, menu]"), ["codex", "gpt-6.1-sol", null]);
await js("document.getElementById('pickerBtn').click(); menu.querySelector('[data-agent=pi]').click(); true");
check("agent with no models shows an empty state", await js("menu.querySelector('.model-list').textContent"), "Модели не найдены");
await key("Escape", "Escape", 27);
await js("document.getElementById('pickerBtn').click(); menu.querySelector('[data-m=terminal]').click(); true");
await sleep(50);
check("the model menu sets the agent's access", (await calls("/api/settings")).at(-1), {mode: "terminal"});
await key("Escape", "Escape", 27);
check("Esc closes it", await js("menu"), null);

// ---- image thumbnails, gallery and async upload lifecycle ----
const IMAGES = [{kind: "image", path: "/state/images/one.png", label: "Картинка 1", title: "one.png"},
  {kind: "image", path: "/state/images/two.png", label: "Картинка 2", title: "two.png"}];
await js(`__t.set({chat: ${JSON.stringify({...CHAT, messages: [{role: "user", segments: [...IMAGES, {kind: "text", text: "Сделай как на картинке 1"}]}]})}}); true`);
check("sent images have numbered 112×84 previews", await js("[document.querySelectorAll('.thumbs .picture').length, document.querySelector('.thumbs .picture').offsetWidth, document.querySelector('.thumbs .picture').offsetHeight, [...document.querySelectorAll('.thumbs .pic-number')].map(b => b.textContent)]"), [2, 112, 84, ["1", "2"]]);
await js("document.querySelector('.thumbs .picture').click(); true"); await sleep(150);
check("click opens the gallery with dimensions and download", await js("[document.getElementById('viewer').open, document.getElementById('viewerTitle').textContent, document.getElementById('viewerMeta').textContent, document.getElementById('viewerDownload').download]"), [true, "Картинка 1", "536×418 · 1 из 2", "one.png"]);
const fitted = await js("zoom");
await js("document.getElementById('zoomIn').click(); true");
check("zoom increases image size", await js(`zoom > ${fitted}`), true);
await js("document.getElementById('zoomFit').click(); true");
check("fit restores zoom", await js("zoom"), fitted);
await key("ArrowRight", "ArrowRight", 39); await sleep(100);
check("arrow key selects next image", await js("[document.getElementById('viewerTitle').textContent, document.getElementById('viewerNext').disabled, document.querySelector('.viewer-strip .current').dataset.gallery]"), ["Картинка 2", true, "1"]);
if (shot) { const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".viewer.png", Buffer.from(r.data, "base64")); }
await key("Escape", "Escape", 27);
check("Escape closes the image viewer", await js("document.getElementById('viewer').open"), false);
await js(`ed.innerHTML = ''; insertChips(${JSON.stringify(IMAGES)}); true`);
check("draft images have 56×56 previews", await js("[document.querySelectorAll('#attachments .picture').length, document.querySelector('#attachments .picture').offsetWidth]"), [2, 56]);
await js("document.querySelector('[data-remove]').click(); true");
check("remove deletes both preview and image segment", await js("[document.querySelectorAll('#attachments .picture').length, segments().filter(s => s.kind === 'image').map(s => s.path)]"), [1, ["/state/images/two.png"]]);
await js("__replies['/api/upload'] = () => new Promise(r => window.finishUpload = r); window.pendingImage = addFile(new File(['x'], 'new.png', {type: 'image/png'})); true");
await sleep(50);
check("upload shows progress and prevents sending", await js("[document.querySelectorAll('.uploading').length, document.getElementById('sendBtn').disabled]"), [1, true]);
await js("finishUpload({path: '/state/images/new.png'}); pendingImage.then(() => true)");
check("upload success replaces progress with a thumbnail", await js("[document.querySelectorAll('.uploading').length, document.querySelectorAll('#attachments .picture').length, document.getElementById('sendBtn').disabled]"), [0, 2, false]);
if (shot) { const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".attachments.png", Buffer.from(r.data, "base64")); }
await js("window.pendingImage = addFile(new File(['x'], 'cancel.png', {type: 'image/png'})); true"); await sleep(50);
await js("document.getElementById('newBtn').click(); finishUpload({path: '/state/images/cancel.png'}); pendingImage.then(() => true)");
check("upload from the previous draft never enters a new chat", await js("[segments().length, document.querySelectorAll('#attachments .picture').length]"), [0, 0]);
await js("__replies['/api/upload'] = () => Promise.reject(new Error('Upload failed')); addFile(new File(['x'], 'error.png', {type: 'image/png'})).then(() => true)");
check("failed upload clears progress without adding a segment", await js("[uploads.size, segments().length, document.querySelector('.toast:last-of-type').textContent]"), [0, 0, "Upload failed"]);
await js("__replies['/api/upload'] = {path: '/state/images/a.png'}; addFiles({files: [new File(['a'], 'a.png', {type: 'image/png'}), new File(['b'], 'b.png', {type: 'image/png'})]}); true");
await sleep(150);
check("multiple images attach with distinct numbers", await js("segments().filter(s => s.kind === 'image').map(s => s.label)"), ["Картинка 1", "Картинка 2"]);

// ---- full library: settings entry, all skills, search/groups, details, modes and pinning ----
const ALMANAC = {name: "hallmark-almanac", title: "Almanac", summary: "редакционный, средний тон, сдержанный акцент", group: "style", source: "builtin", origin: "hallmark", category: "themes", thumbnail: "/api/skill-image?name=hallmark-almanac&file=preview.webp", mode: "manual", preview: {colors: ["#C4CBD2", "#BBC2C8", "#060E15", "#970D63", "#76004B"], font: "Hanken Grotesk"}};
const REFS = {images: [{file: "preview.webp", label: "Десктоп", url: "/api/skill-image?name=hallmark-almanac&file=preview.webp"}, {file: "mobile.webp", label: "Телефон", url: "/api/skill-image?name=hallmark-almanac&file=mobile.webp"}], links: [{label: "Открыть пример", url: "https://www.usehallmark.com/themes/almanac/"}, {label: "Исходник темы", url: "https://github.com/nutlope/hallmark"}]};
const OD = {name: "opendesign-creative-studio-portfolio", title: "Creative Studio Portfolio", summary: "Present three projects with an asymmetrical image grid.", group: "task", source: "builtin", origin: "opendesign", category: "websites", style: "Editorial", mode: "auto", thumbnail: "/api/skill-image?name=opendesign-creative-studio-portfolio&file=assets%2Freference.webp"};
const OD_APP = {...OD, name: "opendesign-offline-hiking-journal-app", title: "Offline Hiking Journal", category: "apps", style: "Organic", thumbnail: "/api/skill-image?name=opendesign-offline-hiking-journal-app&file=assets%2Freference.webp"};
const OD_REFS = {images: [{file: "assets/reference.webp", label: "Референс", url: OD.thumbnail}], links: [{label: "Промпт OpenDesign", url: "https://open-design.ai/prompts/creative-studio-portfolio/"}]};
const LIBSK = [...SK.map(s => s.name === "graphite" ? {...s, preview: {colors: ["#1C1D21", "#2A2B31", "#E4E6EE", "#8AA4FF"], font: "Inter"}} : s), {name: "external", title: "External", summary: "From pen.dev", group: "other", source: "pen.dev", mode: "manual"}, ...MANY, ALMANAC, OD, OD_APP];
await js(`document.querySelectorAll(".toast").forEach(t => t.remove()); window.__catalog = ${JSON.stringify(LIBSK)};
  __replies['/api/skill?'] = (u) => ({...__catalog.find(s => s.name === new URL(u, 'http://local').searchParams.get('name')), dir: '/skills/graphite', body: '# Instruction', files: [{name: 'SKILL.md', size: 1200}, {name: 'tokens.md', size: 600}], references: u.includes('hallmark-almanac') ? ${JSON.stringify(REFS)} : u.includes('opendesign-') ? ${JSON.stringify(OD_REFS)} : undefined});
  __replies['/api/skill-mode'] = (u) => { const b = __api.at(-1)[1]; __catalog = __catalog.map(s => s.name === b.name ? {...s, mode: b.mode} : s); return {skills: __catalog}; };
  __replies['/api/skill-import'] = {name: 'graphite', skills: __catalog};
  __emit({type: 'state', state: ${JSON.stringify({...STATE, skills: LIBSK})}}); __t.set({draftSkills: ['paper']}); document.getElementById('pickerBtn').click(); document.getElementById('toSettings').click(); document.getElementById('libraryBtn').click(); true`);
const openSources = async (scope) => {
  if (!await js(`!!document.querySelector('[data-source-options="'+${JSON.stringify(scope)}+'"]')`)) {
    await js(`document.querySelector('[data-source-trigger="'+${JSON.stringify(scope)}+'"]').click();true`);
  }
};
const chooseSources = async (scope, ids) => {
  await openSources(scope);
  await js(`(() => {const root=document.querySelector('[data-source-options="'+${JSON.stringify(scope)}+'"]');root.querySelector('[data-origin=all]').click();for(const button of [...root.querySelectorAll('input[data-origin]')]){if(!${JSON.stringify(ids)}.includes(button.dataset.origin))button.click();}root.querySelector('[data-source-done]').click();return true})()`);
};
const toggleSource = async (scope, id) => {
  await openSources(scope);
  await js(`var rootSource=document.querySelector('[data-source-options="'+${JSON.stringify(scope)}+'"]');[...rootSource.querySelectorAll('input[data-origin]')].find(b=>b.dataset.origin===${JSON.stringify(id)}).click();rootSource.querySelector('[data-source-done]').click();true`);
};
check("settings opens the complete library", await js("[library.screen, document.getElementById('skillLibrary').hidden, document.querySelectorAll('[data-skill]').length, document.getElementById('settings').hidden]"), ["catalog", false, LIBSK.length, true]);
check("pen.dev modes are read only", await js("document.querySelector('[data-mode=external]').disabled"), true);
await chooseSources("library", ["opendesign"]); await sleep(100);
check("OpenDesign source filter shows its skills with provenance badges and local thumbnails", await js("[[...document.querySelectorAll('[data-skill]')].map(b => b.dataset.skill), [...document.querySelectorAll('.origin-tag')].map(e => e.textContent), [...document.querySelectorAll('.skill-thumb')].every(i => i.naturalWidth > 0)]"),
  [[OD.name, OD_APP.name], ["OpenDesign", "OpenDesign"], true]);
await js("document.getElementById('skillCategory').value = 'websites'; document.getElementById('skillCategory').dispatchEvent(new Event('change', {bubbles: true})); true");
check("type filter combines with the selected source", await js("[...document.querySelectorAll('[data-skill]')].map(b => b.dataset.skill)"), [OD.name]);
if (shot) { const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".opendesign-library.png", Buffer.from(r.data, "base64")); }
await js(`document.querySelector('[data-skill=${OD.name}]').click(); true`); await sleep(100);
check("OpenDesign card names the collection, type and style and loads its reference", await js("[document.getElementById('libraryBack').parentElement.textContent.includes('OpenDesign · Сайты · Editorial'), document.querySelector('.reference-shot img').naturalWidth > 0]"), [true, true]);
await key("ArrowRight", "ArrowRight", 39);
check("skill navigation respects both origin and type filters", await js("library.name"), OD.name);
if (shot) { const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".opendesign-card.png", Buffer.from(r.data, "base64")); }
await key("Escape", "Escape", 27);
check("returning to the catalog preserves source and type filters", await js("[library.sources, document.getElementById('skillCategory').value]"), [["opendesign"], "websites"]);
await chooseSources("library", ["hallmark"]);
check("Hallmark filter switches collections and clears the previous type", await js("[[...document.querySelectorAll('[data-skill]')].map(b => b.dataset.skill), document.getElementById('skillCategory').value, document.querySelector('.origin-tag').textContent]"), [[ALMANAC.name], "all", "Hallmark"]);
await openSources("library");await js("document.querySelector('[data-source-options=library] [data-origin=all]').click();document.querySelector('[data-source-done]').click();document.getElementById('skillSearch').focus();true");
await type("Приложения");
check("search includes localized design types", await js("[...document.querySelectorAll('[data-skill]')].map(b => b.dataset.skill)"), [OD_APP.name]);
await js("document.getElementById('skillSearch').value = ''; document.getElementById('skillSearch').dispatchEvent(new Event('input', {bubbles: true})); true");
await js("document.querySelector('[data-mode=graphite]').click(); true");
check("a skill's mode is a small menu", await js("[...document.querySelectorAll('.modemenu [data-set-mode]')].map(b => b.querySelector('.grow').firstChild.textContent)"), ["Вручную", "Сам", "Всегда"]);
await js("document.querySelector('.modemenu [data-set-mode=auto]').click(); true"); await sleep(50);
check("it sets the mode", (await calls('/api/skill-mode')).at(-1), {name: "graphite", mode: "auto"});
await js("document.querySelector('[data-mode=graphite]').click(); document.querySelector('.modemenu [data-set-mode=manual]').click(); true"); await sleep(50);
await js("document.querySelector('[data-group=quality]').click(); true");
check("group filter limits the library", await js("[...document.querySelectorAll('[data-skill]')].map(b => b.dataset.skill)"), ["better-typography"]);
await js("document.querySelector('[data-group=all]').click(); document.getElementById('skillSearch').focus(); true");
await type("SDK");
check("catalog search includes the full description", await js("[...document.querySelectorAll('[data-skill]')].map(b => b.dataset.skill)"), ["s7"]);
await js("document.getElementById('skillSearch').value = ''; document.getElementById('skillSearch').dispatchEvent(new Event('input', {bubbles: true})); true");
if (shot) { const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".library.png", Buffer.from(r.data, "base64")); }
await js("document.querySelector('[data-skill=graphite]').click(); true"); await sleep(50);
check("card shows real files and style preview", await js("[library.screen, document.querySelectorAll('.skill-file span').length > 0, document.querySelectorAll('.skill-palette i').length, document.querySelector('pre').textContent]"), ["card", true, 4, "# Instruction"]);
await js("__t.set({library: {...library, group: 'style'}}); true");
await key("ArrowRight", "ArrowRight", 39); await sleep(50);
check("right arrow opens the next skill card", await js("[library.name, library.detail.name]"), ["paper", "paper"]);
await key("ArrowLeft", "ArrowLeft", 37); await sleep(50);
check("left arrow opens the previous card without changing pinned skills", await js("[library.name, pinned()]"), ["graphite", ["paper"]]);
await key("ArrowLeft", "ArrowLeft", 37);
check("navigation stops at the filtered group's first card", await js("library.name"), "graphite");
await js("__t.set({library: {...library, q: 'sdk'}}); openSkill('s7').then(() => true)");
await key("ArrowRight", "ArrowRight", 39);
check("card navigation respects the search filter", await js("library.name"), "s7");
await js("__t.set({library: {...library, q: ''}}); openSkill('graphite').then(() => true)");
await key("ArrowRight", "ArrowRight", 39, 2);
check("modified arrow shortcuts do not navigate", await js("library.name"), "graphite");
await js("const field = document.createElement('input'); field.id = 'cardField'; document.getElementById('skillLibrary').append(field); field.focus(); true");
await key("ArrowRight", "ArrowRight", 39);
check("arrows in a form field keep their normal behavior", await js("library.name"), "graphite");
await js("document.getElementById('cardField').remove(); true");
await js("document.querySelector('[data-card-mode=auto]').click(); true"); await sleep(50);
check("mode selection reaches the server and updates the card", [(await calls('/api/skill-mode')).at(-1), await js("skillOf('graphite').mode")], [{name: "graphite", mode: "auto"}, "auto"]);
await js("document.querySelector('[data-pin]').click(); true"); await sleep(50);
check("pinning another style keeps the previous style", await js("pinned()"), ["paper", "graphite"]);
await js("document.querySelector('[data-folder]').click(); true"); await sleep(50);
check("folder action names the catalog entry", (await calls('/api/skill-folder')).at(-1), {name: "graphite"});
if (shot) { const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".skill.png", Buffer.from(r.data, "base64")); }
await js("openSkill('hallmark-almanac').then(() => true)"); await sleep(150);
check("a theme card shows its local desktop screenshot and reference links", await js("[document.querySelector('.reference-shot img').naturalWidth, [...document.querySelectorAll('.reference-links a')].map(a => [a.textContent, a.target, a.rel.includes('noopener')]), document.documentElement.scrollWidth <= innerWidth]"),
  [960, [["Открыть пример ↗", "_blank", true], ["Исходник темы ↗", "_blank", true]], true]);
if (shot) {
  const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".references.png", Buffer.from(r.data, "base64"));
  await send("Emulation.setDeviceMetricsOverride", {width: 840, height: 1000, deviceScaleFactor: 1, mobile: false});
  await sleep(100); const wide = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".references-wide.png", Buffer.from(wide.data, "base64"));
  await send("Emulation.setDeviceMetricsOverride", {width: 400, height: 860, deviceScaleFactor: 1, mobile: false});
}
await js("document.querySelector('[data-preview=\"1\"]').click(); true"); await sleep(150);
check("the phone tab shows the mobile reference", await js("[document.querySelector('.reference-shot img').naturalWidth, document.querySelector('[data-preview=\"1\"]').getAttribute('aria-pressed')]"), [360, "true"]);
await js("document.querySelector('[data-reference-image]').click(); true"); await sleep(150);
check("reference previews open in the zoomable gallery with a download", await js("[document.getElementById('viewer').open, document.getElementById('viewerTitle').textContent, document.getElementById('viewerDownload').download, document.querySelector('#viewerImage').naturalWidth]"),
  [true, "Almanac · Телефон", "mobile.webp", 360]);
await key("ArrowLeft", "ArrowLeft", 37); await sleep(100);
check("gallery arrows switch between reference views", await js("document.getElementById('viewerTitle').textContent"), "Almanac · Десктоп");
await key("Escape", "Escape", 27);
check("closing a reference returns to the same skill card", await js("[document.getElementById('viewer').open, library.name, library.screen]"), [false, "hallmark-almanac", "card"]);
await js("document.querySelector('.reference-shot img').dispatchEvent(new Event('error')); true");
check("a preview load failure offers retry", await js("document.querySelector('.reference-error').textContent"), "Не удалось загрузить превьюПовторить");
await js("document.querySelector('.reference-error button').click(); true"); await sleep(150);
check("retry restores the reference image", await js("document.querySelector('.reference-shot img').naturalWidth"), 360);
await js("openSkill('graphite').then(() => true)");
check("switching skills removes the previous references", await js("document.querySelector('.skill-references') === null"), true);
await key("Escape", "Escape", 27);
check("back from card keeps the library", await js("library.screen"), "catalog");
await js("document.querySelector('[data-page=help]').click(); true");
check("library explains levels, sources and skill metadata", await js("document.querySelector('#skillLibrary .body').textContent.includes('Четыре уровня') && document.querySelector('#skillLibrary pre').textContent.includes('metadata:')"), true);
await key("Escape", "Escape", 27);
await js("document.querySelector('[data-page=add]').click(); document.getElementById('skillFolder').value = '/new/graphite'; document.getElementById('skillImport').requestSubmit(); true"); await sleep(50);
check("add imports a folder and opens its card", [(await calls('/api/skill-import')).at(-1), await js("library.screen")], [{folder: "/new/graphite"}, "card"]);
await key("Escape", "Escape", 27); await key("Escape", "Escape", 27);
check("closing library returns to settings", await js("[library, document.getElementById('settings').hidden]"), [null, false]);
await js("document.getElementById('back').click(); document.getElementById('attachBtn').click(); menu.querySelector('[data-a=library]').click(); true");
check("composer also opens the catalog", await js("library.screen"), "catalog");
await key("Escape", "Escape", 27);
await js("ed.innerHTML = ''; ed.focus(); changed(); true"); await type('/');
await js("menu.querySelector('[data-library]').click(); true");
check("slash menu opens catalog without leaving a stray slash", await js("[library.screen, ed.textContent.includes('/') ]"), ["catalog", false]);
await key("Escape", "Escape", 27);

// ---- quick skill filters: Tab types, arrows skills, selection and pinning stay separate ----
await js(`__emit({type: 'state', state: ${JSON.stringify({...STATE, skills: LIBSK})}}); __t.set({view: 'chat', chat: null, draftSkills: [], slashCategory: 'all', skillPrefs: {favorites: [], recent: []}}); clearDraft(); ed.focus(); true`);
await type("/");
check("quick skill menu lists only available design types", await js("[...menu.querySelectorAll('[data-slash-category]')].map(b => b.dataset.slashCategory)"), ["all", "recent", "favorites", "websites", "apps", "themes", "general"]);
const agentBeforeFilters = await js("S.settings.agent");
await key("Tab", "Tab", 9); await key("Tab", "Tab", 9); await key("Tab", "Tab", 9);
check("Tab switches to websites while keeping the caret and agent", await js("[__t.get().slash.category, __t.get().slash.i, document.activeElement === ed, S.settings.agent, pinned()]"), ["websites", 0, true, agentBeforeFilters, []]);
check("website filter shows matching skills with thumbnails", [await menuItems(), await js("!!menu.querySelector('.slash-thumb')")], [[OD.title], true]);
if (shot) { const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".quick-skill-filter.png", Buffer.from(r.data, "base64")); }
await key("Tab", "Tab", 9, 8); await key("Tab", "Tab", 9, 8); await key("Tab", "Tab", 9, 8);
check("Shift+Tab returns to all types", await js("__t.get().slash.category"), "all");
await key("Tab", "Tab", 9, 8);
check("Shift+Tab wraps to general skills", await js("[__t.get().slash.category, !!menu.querySelector('.slash-thumb')]"), ["general", false]);
await js("menu.querySelector('[data-slash-category=apps]').click(); true");
await type("hiking");
check("typing a query keeps the chosen type and filters results", [await js("__t.get().slash.category"), await menuItems()], ["apps", [OD_APP.title]]);
await key("Tab", "Tab", 9, 8);
check("a query with no matches keeps its filter and offers a reset", await js("[__t.get().slash.category, __t.get().slash.items.length, !!menu.querySelector('[data-reset-slash]'), __t.get().slash.q]"), ["websites", 0, true, "hiking"]);
await key("Tab", "Tab", 9);
check("Tab still switches types when the current result is empty", [await js("__t.get().slash.category"), await menuItems()], ["apps", [OD_APP.title]]);
await key("Tab", "Tab", 9, 8);
await js("menu.querySelector('[data-reset-slash]').click(); true");
check("resetting the type keeps the query", [await js("__t.get().slash.category"), await menuItems()], ["all", [OD_APP.title]]);
await key("Tab", "Tab", 9); await key("Tab", "Tab", 9); await key("Tab", "Tab", 9);
await js("menu.querySelector('[data-library]').click(); true");
check("the full library opens with the quick menu's selected type", await js("[library.category, ed.textContent.includes('/') ]"), ["websites", false]);
await key("Escape", "Escape", 27);
await js("ed.focus(); true"); await type("/");
check("reopening the quick menu remembers its type", await js("__t.get().slash.category"), "websites");
await key(" ", "Space", 32); await key("Tab", "Tab", 9); await key(" ", "Space", 32);
check("selected skills survive switching types", await js("segments().filter(s => s.kind === 'skill').map(s => s.name)"), [OD.name, OD_APP.name]);
await key("Enter", "Enter", 13, 2); await sleep(50);
check("Ctrl+Enter pins the current skill without changing the type", await js("[pinned(), __t.get().slash.category, segments().filter(s => s.kind === 'skill').map(s => s.name)]"), [[OD_APP.name], "apps", [OD.name]]);
await js("menu.querySelector('[data-pin-current]').click(); true"); await sleep(50);
check("the visible pin button can unpin it", await js("pinned()"), []);
await key("Enter", "Enter", 13);
await js(`clearDraft(); __t.set({draftSkills: [${JSON.stringify(OD.name)}]}); document.querySelector('#pinnedBtn b').click(); menu.querySelector('[data-a=add]').click(); true`);
check("pin mode opens with the same type", await js("[__t.get().slash.mode, __t.get().slash.category, document.activeElement.id]"), ["pin", "apps", "sq"]);
await key("Tab", "Tab", 9);
check("Tab changes types in pin mode too", await js("[__t.get().slash.category, document.activeElement.id]"), ["themes", "sq"]);
await key("Enter", "Enter", 13); await sleep(50);
check("Enter pins the selected filtered theme", await js("pinned()"), [OD.name, ALMANAC.name]);
await key("Escape", "Escape", 27);
await js("__t.set({slashCategory: 'all'}); clearDraft(); ed.focus(); true"); await type("/");
await js(`menu.querySelector('[data-slash-category=websites]').click(); menu.querySelector('[data-favorite=${OD.name}]').click(); true`);
check("favoriting a skill does not attach it or move the caret", await js("[__t.get().skillPrefs.favorites, segments().filter(s => s.kind === 'skill').length, document.activeElement === ed]"), [[OD.name], 0, true]);
await js("menu.querySelector('[data-slash-category=favorites]').click(); true");
check("Favorites shows only saved skills", await menuItems(), [OD.title]);
await js(`menu.querySelector('[data-favorite=${OD.name}]').click(); true`);
check("unfavoriting removes the row and explains the empty state", await js("[__t.get().slash.items.length, menu.querySelector('.empty-state b').textContent]"), [0, "В избранном пока пусто"]);
await js(`menu.querySelector('[data-slash-category=websites]').click(); menu.querySelector('[data-favorite=${OD.name}]').click(); menu.querySelector('[data-slash-category=recent]').click(); true`);
check("Recent contains used and pinned skills in usage order", await menuItems(), [ALMANAC.title, OD.title, OD_APP.title]);
await js("menu.querySelector('[data-library]').click(); true");
check("the full library keeps the Recent collection and its order", await js("[library.collection, document.querySelector('[data-skill]').dataset.skill]"), ["recent", ALMANAC.name]);
await js("document.querySelector('[data-skill-collection=favorites]').click(); true");
check("Favorites is available in the full library too", await js("[...document.querySelectorAll('[data-skill]')].map(b=>b.dataset.skill)"), [OD.name]);
await key("Escape", "Escape", 27);
await js("__t.set({slashCategory: 'all'}); true");

// ---- larger skill cards and a responsive grid controlled by all four arrows ----
await js("clearDraft(); ed.focus(); true"); await type("/");
check("list thumbnails are larger than the old compact rows", await js("(() => {const i=menu.querySelector('.slash-preview');return i.getBoundingClientRect().width>=96 && i.getBoundingClientRect().height>=64;})()"), true);
await js("menu.querySelector('[data-skill-view=grid]').click(); true");
check("grid mode expands the available skills and keeps the editor focused", await js("[__t.get().slashView, Object.keys(__t.get().slash.items.more || {}).length, document.activeElement===ed, !!menu.querySelector('.skill-grid')]"), ["grid", 0, true, true]);
check("grid cards without an image omit the preview",await js("!menu.querySelector('.no-image') && !!menu.querySelector('.slash-entry:not(:has(.slash-preview))')"),true);
check("grid cards keep their preview height inside the scrolling menu", await js("[...menu.querySelectorAll('.slash-entry:has(.slash-preview)')].every(c => c.getBoundingClientRect().height > 200 && c.querySelector('.slash-preview').getBoundingClientRect().height > 80)"), true);
await key("ArrowRight", "ArrowRight", 39);
check("Right selects the next grid card", await js("__t.get().slash.i"), 1);
await key("ArrowDown", "ArrowDown", 40);
check("Down moves by a visual row in the two-column grid", await js("__t.get().slash.i"), 3);
await key("ArrowLeft", "ArrowLeft", 37);
check("Left selects the previous grid card", await js("__t.get().slash.i"), 2);
await key("ArrowUp", "ArrowUp", 38);
check("Up returns to the same column of the previous row", await js("__t.get().slash.i"), 0);
await key("ArrowLeft", "ArrowLeft", 37);
check("Left at the first card wraps to the last skill", await js("__t.get().slash.i===__t.get().slash.items.length-1"), true);
await key("ArrowRight", "ArrowRight", 39);
await send("Emulation.setDeviceMetricsOverride", {width: 840, height: 1000, deviceScaleFactor: 1, mobile: false}); await sleep(50);
await key("ArrowDown", "ArrowDown", 40);
check("grid navigation follows the resized three-column layout", await js("__t.get().slash.i"), 3);
await key("ArrowUp", "ArrowUp", 38);
if (shot) { const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".grid-wide.png", Buffer.from(r.data, "base64")); }
await send("Emulation.setDeviceMetricsOverride", {width: 400, height: 860, deviceScaleFactor: 1, mobile: false}); await sleep(50);
await key("ArrowDown", "ArrowDown", 40);
check("grid navigation adapts back to two columns", await js("__t.get().slash.i"), 2);
await key("ArrowUp", "ArrowUp", 38);
await key(" ", "Space", 32);
check("Space still checks a grid card without changing the query", await js("[segments().filter(s=>s.kind==='skill').map(s=>s.name), __t.get().slash.q, document.activeElement===ed]"), [["graphite"], "", true]);
await js("menu.querySelector('[data-skill-view=list]').click(); true");
check("switching to the list preserves the selection and active skill", await js("[__t.get().slashView, __t.get().slash.items[__t.get().slash.i].name, segments().filter(s=>s.kind==='skill').map(s=>s.name)]"), ["list", "graphite", ["graphite"]]);
await js("menu.querySelector('[data-skill-view=grid]').click(); true");
await key("Enter", "Enter", 13);
await js(`clearDraft(); __t.set({draftSkills:[${JSON.stringify(OD.name)}]}); document.querySelector('#pinnedBtn b').click(); menu.querySelector('[data-a=add]').click(); true`);
check("the same grid mode is available while pinning skills", await js("[__t.get().slash.mode, !!menu.querySelector('.skill-grid'), document.activeElement.id]"), ["pin", true, "sq"]);
await key("ArrowRight", "ArrowRight", 39);
check("Right also navigates grid cards in pin mode", await js("__t.get().slash.items[__t.get().slash.i].name"), "paper");
await js("menu.querySelector('[data-skill-view=preview]').click(); true");
await key("ArrowDown", "ArrowDown", 40);
check("preview mode follows keyboard browsing in the pinning menu", await js("[document.querySelector('[data-preview-skill]').dataset.previewSkill, __t.get().slash.items[__t.get().slash.i].name, document.activeElement.id]"), ["s0", "s0", "sq"]);
await key("Escape", "Escape", 27);

// ---- the preview browser keeps browsing separate from marking a skill ----
await js("clearDraft(); __t.set({slashCategory:'all'}); ed.focus(); true"); await type("/");
check("preview mode starts with the description when a skill has no image", await js("[__t.get().slashView,document.querySelector('[data-preview-skill]').dataset.previewSkill,!!menu.querySelector('.inspector-media'),menu.querySelector('.slash-inspector').firstElementChild.className]"), ["preview","graphite",false,"inspector-copy"]);
await js(`menu.querySelector('[data-k="'+__t.get().slash.items.findIndex(k=>k.name===${JSON.stringify(ALMANAC.name)})+'"]').click(); true`);
check("clicking a row opens its large preview without selecting it", await js("[document.querySelector('[data-preview-skill]').dataset.previewSkill, menu.querySelector('.inspector-media img').getAttribute('src'), segments().filter(s=>s.kind==='skill').length, document.activeElement===ed]"), [ALMANAC.name, ALMANAC.thumbnail, 0, true]);
await key("ArrowUp", "ArrowUp", 38);
check("Up changes the preview to the previous skill", await js("document.querySelector('[data-preview-skill]').dataset.previewSkill"), "s9");
await key("ArrowDown", "ArrowDown", 40);
await js("menu.querySelector('[data-preview-select]').click(); true");
check("the preview checkbox adds the active skill to the message", await js("[segments().filter(s=>s.kind==='skill').map(s=>s.name), menu.querySelector('[data-preview-select]').getAttribute('aria-pressed')]"), [[ALMANAC.name], "true"]);
await js(`menu.querySelector('[data-k="'+__t.get().slash.i+'"]').previousElementSibling.click();true`);
check("the row checkbox removes the active skill without closing the browser", await js("[segments().filter(s=>s.kind==='skill').length, __t.get().slashView, !!document.querySelector('[data-preview-skill]')]"), [0, "preview", true]);
await send("Emulation.setDeviceMetricsOverride", {width: 840, height: 1000, deviceScaleFactor: 1, mobile: false});
await js("__t.set({draft:__t.get().draft+1});true"); await sleep(100);
check("the preview is beside the list on a wide panel", await js("(() => {const a=menu.querySelector('.slash-list').getBoundingClientRect(),b=menu.querySelector('.slash-inspector').getBoundingClientRect();return b.left>=a.right && b.width>300 && menu.querySelector('.inspector-media').getBoundingClientRect().width>300})()"), true);
if (shot) { const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".preview-wide.png", Buffer.from(r.data, "base64")); }
await send("Emulation.setDeviceMetricsOverride", {width: 400, height: 860, deviceScaleFactor: 1, mobile: false});
await js("__t.set({draft:__t.get().draft+1});true"); await sleep(100);
check("a narrow panel puts the large preview above a scrollable list", await js("(() => {const a=menu.querySelector('.slash-list').getBoundingClientRect(),b=menu.querySelector('.slash-inspector').getBoundingClientRect();return b.bottom<=a.top+1 && a.height>=80 && menu.querySelector('.inspector-media').getBoundingClientRect().width>300 && document.documentElement.scrollWidth<=innerWidth})()"), true);
if (shot) { const r = await send("Page.captureScreenshot", {format: "png"}); fs.writeFileSync(shot + ".preview-narrow.png", Buffer.from(r.data, "base64")); }
await js("menu.querySelector('[data-slash-category=apps]').click();true");
check("category filters update the large preview", await js("document.querySelector('[data-preview-skill]').dataset.previewSkill"), OD_APP.name);
await type("does-not-exist");
check("an empty search clears the previous preview", await js("[!!menu.querySelector('.empty-state'), !!menu.querySelector('[data-preview-skill]')]"), [true, false]);
await key("Escape", "Escape", 27);

// ---- compact source popup preserves independent toggles and the combined filter ----
await js("clearDraft();__t.set({slashCategory:'all',slashSources:null});ed.focus();true");await type('/');
const sources = (ids) => chooseSources('slash', ids);
check("the source filter is compact when closed",await js("[!!document.querySelector('[data-source-trigger=slash]'),!!document.querySelector('[data-source-options]'),!!menu.querySelector('.source-chips')]"),[true,false,false]);
await openSources('slash');
check("source popup lists installed origins as checkboxes",await js("[...document.querySelectorAll('[data-source-options=slash] input[data-origin]')].map(b=>b.dataset.origin)"),['opendesign','hallmark','builtin','project','mine','pen.dev']);
check("opening the source popup leaves the skill menu open",await js("menu?.dataset.kind"),'slash');
const sourceOutside = await js("(()=>{const r=menu.querySelector('[data-skill-view=preview]').getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2}})()");
await send('Input.dispatchMouseEvent',{type:'mousePressed',button:'left',clickCount:1,...sourceOutside});
await send('Input.dispatchMouseEvent',{type:'mouseReleased',button:'left',clickCount:1,...sourceOutside});
check("clicking outside sources closes the popup and keeps the skills open",await js("[!!document.querySelector('[data-source-options]'),menu?.dataset.kind,document.activeElement===ed]"),[false,'slash',true]);
await sources(['opendesign']);
check("source chips filter skills and type counts without moving the caret",await js("[__t.get().slash.sources,__t.get().slash.items.map(k=>k.name),menu.querySelector('[data-slash-category=all] small').textContent,document.activeElement===ed]"),[['opendesign'],[OD.name,OD_APP.name],'2',true]);
await js("menu.querySelector('[data-slash-category=websites]').click();true");await key(' ','Space',32);
await toggleSource("slash","hallmark");
check("enabling Hallmark retains OpenDesign and the selected type",await js("[__t.get().slash.sources,__t.get().slash.category,segments().filter(s=>s.kind==='skill').map(s=>s.name)]"),[['opendesign','hallmark'],'websites',[OD.name]]);
await js("menu.querySelector('[data-slash-category=all]').click();true");
check("multiple sources combine their results",await js("__t.get().slash.items.map(k=>k.name).sort()"),[ALMANAC.name,OD.name,OD_APP.name].sort());
await toggleSource("slash","opendesign");
check("turning one source off keeps the other and existing selected chips",await js("[__t.get().slash.sources,__t.get().slash.items.map(k=>k.name),segments().filter(s=>s.kind==='skill').map(s=>s.name)]"),[['hallmark'],[ALMANAC.name],[OD.name]]);
await js("menu.querySelector('[data-skill-view=grid]').click();true");await sources(['opendesign']);
await key('ArrowRight','ArrowRight',39);await key(' ','Space',32);
check("grid navigation stays within enabled sources",await js("[__t.get().slash.items[__t.get().slash.i].name,segments().filter(s=>s.kind==='skill').map(s=>s.name)]"),[OD_APP.name,[OD.name,OD_APP.name]]);
await sources(['hallmark']);await js("menu.querySelector('[data-skill-view=preview]').click();true");await type('hiking');
check("typing preserves enabled sources and offers a reset for empty results",await js("[__t.get().slash.sources,__t.get().slash.q,__t.get().slash.items.length,!!menu.querySelector('[data-reset-origin]')]"),[['hallmark'],'hiking',0,true]);
await sources([]);
check("all sources can be disabled without silently enabling everything",await js("[__t.get().slash.sources,__t.get().slash.items.length,menu.querySelector('.empty-state b').textContent]"),[[],0,'Источники выключены']);
await js("menu.querySelector('[data-reset-origin]').click();true");
check("All restores sources while keeping the query and skill selections",await js("[__t.get().slash.sources,__t.get().slash.q,__t.get().slash.items.map(k=>k.name),segments().filter(s=>s.kind==='skill').map(s=>s.name)]"),[null,'hiking',[OD_APP.name],[OD.name,OD_APP.name]]);
await key('Enter','Enter',13);await js("clearDraft();ed.focus();true");await type('/');await sources(['hallmark']);
await key('ArrowRight','ArrowRight',39,1);await key(' ','Space',32);
check("Alt opens the source popup and Space toggles a checkbox",await js("[document.activeElement.dataset.origin,__t.get().slash.sources]"),['opendesign',['hallmark','opendesign']]);
await key('Escape','Escape',27);
check("Escape closes only the sources and restores the editor caret",await js("[document.activeElement===ed,!!document.querySelector('[data-source-options]'),menu?.dataset.kind]"),[true,false,'slash']);
await js("menu.querySelector('[data-slash-category=favorites]').click();true");
check("Favorites composes with multiple source chips",await js("__t.get().slash.items.map(k=>k.name)"),[OD.name]);
await js("menu.querySelector('[data-slash-category=recent]').click();menu.querySelector('[data-library]').click();true");
check("the full library inherits every enabled source",await js("[library.sources,library.collection,[...document.querySelectorAll('[data-skill]')].every(b=>b.dataset.skill.startsWith('hallmark-')||b.dataset.skill.startsWith('opendesign-'))]"),[['hallmark','opendesign'],'recent',true]);
await key('Escape','Escape',27);
await js(`clearDraft();__t.set({draftSkills:[${JSON.stringify(ALMANAC.name)}]});document.querySelector('#pinnedBtn b').click();menu.querySelector('[data-a=add]').click();true`);
await sources(['opendesign']);
check("pin mode remembers and applies source chips",await js("[__t.get().slash.sources,document.activeElement.id]"),[['opendesign'],'sq']);
await type('hiking');await key('Enter','Enter',13);await sleep(50);
check("pinning still uses the filtered skill",await js("pinned()"),[ALMANAC.name,OD_APP.name]);
await sources(['opendesign','hallmark']);await key('Escape','Escape',27);

// ---- Design resources: kinds, source filters, metadata and card navigation ----
const DESIGN_DETAILS = JSON.parse(execFileSync("python3", ["-c", `
import sys,json
from pathlib import Path
sys.path.insert(0,'sidecar')
import skills
print(json.dumps([skills.details(skills.read_skill(str(p),'builtin')) for p in sorted(Path('skills/skills').glob('design-*'))]))
`], {cwd:path.join(path.dirname(new URL(import.meta.url).pathname),".."),encoding:"utf8"}));
const RESOURCES = DESIGN_DETAILS.map(({body,files,dir,path,references,truncated,...skill})=>skill);
await js(`clearDraft();__t.set({chat:null,draftSkills:[],slashSources:null,slashCategory:'all'});window.__catalog=${JSON.stringify([...LIBSK,...RESOURCES])};window.__designDetails=${JSON.stringify(DESIGN_DETAILS)};
  const fallback=__replies['/api/skill?'];__replies['/api/skill?']=(u)=>__designDetails.find(k=>k.name===new URL(u,'http://local').searchParams.get('name'))||fallback(u);
  __emit({type:'state',state:${JSON.stringify({...STATE,skills:[...LIBSK,...RESOURCES]})}});ed.focus();true`);
await type('/');
check("collections and design types are separate groups", await js(`[!!menu.querySelector('[aria-label="Подборка навыков"]'),!!menu.querySelector('[aria-label="Тип навыка"] [data-slash-category=design-systems]')]`), [true,true]);
await js("menu.querySelector('[data-slash-category=design-systems]').click();true");
check("design resources have counted subtypes", await js("[...menu.querySelectorAll('[data-resource-kind]')].map(b=>[b.dataset.resourceKind,b.querySelector('small').textContent])"), [['all','7'],['system','4'],['ui-kit','1'],['components','2']]);
await js("menu.querySelector('[data-resource-kind=components]').click();true");
check("component filter keeps the composer caret", await js("[__t.get().slash.items.map(k=>k.name),document.activeElement===ed]"), [['design-material-ui','design-shadcn-ui'],true]);
await type('shadcn');
check("typing preserves the resource subtype", await js("[__t.get().slash.resourceKind,__t.get().slash.items.map(k=>k.name)]"), ['components',['design-shadcn-ui']]);
check("resource badges distinguish community kits and mixed access", await js("menu.querySelector('.resource-tags').textContent.includes('Автор / community')&&menu.querySelector('.resource-tags').textContent.includes('Бесплатно / платно')"), true);
await js("menu.querySelector('[data-library]').click();true");
check("library inherits resource type and subtype", await js("[library.category,library.resourceKind,[...document.querySelectorAll('[data-skill]')].map(b=>b.dataset.skill)]"), ['design-systems','components',['design-material-ui','design-shadcn-ui']]);
await js("document.querySelector('[data-skill=design-shadcn-ui]').click();true");await sleep(60);
check("resource card displays format and access", await js("document.querySelector('.resource-tags').textContent.includes('Figma')&&document.querySelector('.resource-tags').textContent.includes('Код')&&document.querySelector('.resource-tags').textContent.includes('Бесплатно / платно')"), true);
await sleep(100);
check("real design card loads its local light preview",await js("[document.querySelector('.reference-shot img').naturalWidth,document.querySelectorAll('[data-preview]').length]"),[1080,2]);
await js(`document.querySelector('[data-preview="1"]').click();true`);await sleep(100);
check("real design card switches to its local dark preview",await js("[document.querySelector('.reference-shot img').naturalWidth,document.querySelector('.reference-shot img').src.includes('dark.webp')]"),[1080,true]);
if (shot) {const r=await send('Page.captureScreenshot',{format:'png'});fs.writeFileSync(shot+'.design-skill-card.png',Buffer.from(r.data,'base64'));}
await key('Escape','Escape',27);
check("returning from the card preserves subtype", await js("[library.resourceKind,document.querySelector('[data-resource-kind=components]').getAttribute('aria-pressed')]"), ['components','true']);
await js("document.querySelector('[data-resource-kind=ui-kit]').click();true");
check("UI kit filter selects the kit", await js("[...document.querySelectorAll('[data-skill]')].map(b=>b.dataset.skill)"), ['design-figma-simple']);
await js("document.querySelector('[data-group=library]').click();document.getElementById('skillCategory').value='websites';document.getElementById('skillCategory').dispatchEvent(new Event('change',{bubbles:true}));true");
check("changing design type clears incompatible kind and group", await js("[library.resourceKind,library.group,[...document.querySelectorAll('[data-skill]')].map(b=>b.dataset.skill)]"), ['all','all',[OD.name]]);
await key('Escape','Escape',27);
await js("clearDraft();ed.focus();true");await type('/');
await js("menu.querySelector('[data-slash-category=design-systems]').click();true");
await sources(['design-resources']);
check("source selection composes with resource type", await js("[__t.get().slash.category,__t.get().slash.items.length,menu.querySelector('[data-slash-category=all] small').textContent]"), ['design-systems',7,'7']);
await js("menu.querySelector('[data-resource-kind=system]').click();true");
if (shot) { const r=await send('Page.captureScreenshot',{format:'png'});fs.writeFileSync(shot+'.design-systems.png',Buffer.from(r.data,'base64')); }
await sources(['opendesign']);
check("a source without design resources falls back to all", await js("[__t.get().slash.category,__t.get().slash.items.map(k=>k.name),!!menu.querySelector('[data-resource-kind]')]"), ['all',[OD.name,OD_APP.name],false]);
await sources(['opendesign','hallmark']);await key('Escape','Escape',27);

// The real skill cards attach to a message, pin to a draft chat and send both levels.
await js("clearDraft();__t.set({chat:null,draftSkills:['design-carbon'],slashSources:null});ed.focus();true");await type('Build an access screen');
const openDesignCard = async (name) => {
  await js("document.getElementById('attachBtn').click();menu.querySelector('[data-a=library]').click();true");
  await chooseSources('library',['design-resources']);
  await js(`document.querySelector('[data-skill=${name}]').click();true`);await sleep(60);
};
await openDesignCard('design-material-3');
await js("document.querySelector('[data-pin]').click();true");await sleep(30);
check("pinning a real system replaces the draft chat's previous system",await js("pinned()"),['design-material-3']);
await js("document.querySelector('[data-add-message]').click();true");
check("a card adds its skill to the message and preserves draft text",await js("[library,__t.get().settingsOpen,segments().filter(s=>s.kind==='skill').map(s=>s.name),ed.textContent.includes('Build an access screen'),document.activeElement===ed]"),[null,false,['design-material-3'],true,true]);
await openDesignCard('design-carbon');await js("document.querySelector('[data-add-message]').click();true");
check("message system replaces only the previous message system",await js("[segments().filter(s=>s.kind==='skill').map(s=>s.name),pinned()]"),[['design-carbon'],['design-material-3']]);
await openDesignCard('design-carbon');
check("an attached skill cannot be added twice from its card",await js("document.querySelector('[data-add-message]').disabled"),true);
await key('Escape','Escape',27);await key('Escape','Escape',27);
await openDesignCard('design-shadcn-ui');await js("document.querySelector('[data-add-message]').click();true");
check("a component library can accompany a system in the message",await js("segments().filter(s=>s.kind==='skill').map(s=>s.name).sort()"),['design-carbon','design-shadcn-ui']);
await js(`__replies['/api/send']=${JSON.stringify({...CHAT,id:'design-test',skills:['design-material-3']})};true`);
await key('Enter','Enter',13);await sleep(80);
const designSend=(await calls('/api/send')).at(-1);
check("sending includes real message skill names and groups",designSend.segments.filter(s=>s.kind==='skill').map(s=>[s.name,s.group]).sort((a,b)=>a[0].localeCompare(b[0])),[['design-carbon','system'],['design-shadcn-ui','library']]);
check("sending carries the draft chat's pinned system",designSend.skills,['design-material-3']);
await js("__t.set({draftSkills:[]});true");

// ---- Strict: the start card, the one-line input, any file, the queue ----
await js(`__emit({type: "state", state: ${JSON.stringify({...STATE, chats: [{id: "c1", title: "Сделай", agent: "claude", updated: 1}]})}}); newChat(); true`);
check("an empty input is one line, + next to the model", await js("[document.getElementById('box').classList.contains('compact'), getComputedStyle(document.getElementById('attachBtn')).display !== 'none', document.getElementById('sendBtn').disabled]"), [true, true, true]);
check("the empty input sits in the middle of the box, level with send", await js("(() => { const e = document.getElementById('input').getBoundingClientRect(), b = document.getElementById('sendBtn').getBoundingClientRect(); return Math.round(e.top + e.height / 2) === Math.round(b.top + b.height / 2); })()"), true);
await press("3");
check("1–3 pick a way to start", await js("document.querySelector('.choice.on b').textContent"), "Привести к токенам");
await js(`__replies["/api/send"] = ${JSON.stringify({...CHAT, id: "c3", messages: [{role: "user", segments: [{kind: "text", text: "x"}]}]})}; true`);
await key("Enter", "Enter", 13);
await sleep(50);
check("Enter starts it", (await calls("/api/send")).at(-1).segments.map((s) => s.text ?? s.kind), ["Приведи цвета и тексты к переменным и стилям файла "]);
await js(`newChat(); __replies["/api/upload"] = {path: "/state/images/x-tokens.json", size: 4100};
  addFile(new File(["{}"], "tokens.json", {type: "application/json"})).then(() => true)`);
check("any file attaches, as a tile with its type and size", await js("[segments().map(s => s.kind + ':' + s.label), document.querySelector('#attachments .filetile').textContent, document.getElementById('box').classList.contains('compact')]"),
      [["file:tokens.json"], "tokens.jsonJSON · 4 КБ", false]);
check("its upload carries the name", (await calls("/api/upload")).at(-1).name, "tokens.json");
await js(`clearDraft(); __t.set({chat: ${JSON.stringify({...CHAT, id: "c1", messages: [{role: "user", segments: [{kind: "text", text: "x"}]}, {role: "assistant", agent: "claude", running: true, parts: []}]})}});
  __emit({type: "running", running: [{chat: "c1", file: "/d/x.figcraft"}]}); ed.focus(); true`);
await type("и на экране С тоже");
check("while the agent works, Enter queues", await js("document.getElementById('boxHint').textContent"), "↵ в очередь");
const sendsBefore = (await calls("/api/send")).length;
await key("Enter", "Enter", 13);
check("the queued message waits under the answer", [await js("document.querySelector('.umsg.queued .me').textContent"), (await calls("/api/send")).length - sendsBefore, await segs()],
      ["и на экране С тоже", 0, []]);
await js(`__emit({type: "running", running: []}); true`);
await sleep(50);
check("and goes once the agent stops", (({chat, segments}) => ({chat, segments}))((await calls("/api/send")).at(-1)), {chat: "c1", segments: [{kind: "text", text: "и на экране С тоже"}]});

if (shot) {
  await js("__t.set({view: 'remarks'}); true");
  await sleep(300);
  const r = await send("Page.captureScreenshot", {format: "png"});
  fs.writeFileSync(shot, Buffer.from(r.data, "base64"));
}
await send("Page.reload"); await sleep(500);
check("favorites and recent skills survive a page reload", await js(`const p=__t.get().skillPrefs; [p.favorites.includes(${JSON.stringify(OD.name)}), p.recent.includes(${JSON.stringify(ALMANAC.name)})]`), [true, true]);
check("the chosen skill display survives a page reload", await js("__t.get().slashView"), "preview");
check("enabled sources survive a page reload",await js("__t.get().slashSources"),["design-resources"]);
} finally {
ws.close();
const gone = new Promise((r) => chrome.once("exit", r));
chrome.kill();
await gone;  // Chromium writes into its profile until it exits
fs.rmSync(profile, {recursive: true, force: true, maxRetries: 5, retryDelay: 100});
}
console.log(failed ? `${failed} failed` : "all passed");
process.exit(failed ? 1 : 0);
