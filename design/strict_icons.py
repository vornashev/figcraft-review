#!/usr/bin/env python3
"""The panel's icons as components: «Strict · Иконки», right of «Strict · Компоненты».

Material Design Icons, the same SVG paths the sidecar draws (sidecar/web/src/lib/icons.ts), one 16×16 component each,
its vector bound to color/text-faint; an instance's colour is an override on its «Vector». They replace the Nerd Font
glyphs the screens were drawn with: `glyph()` in strict.py places these instances, and

    strict_icons.py           adds the components that are missing and writes icons.json (name → component id)
    strict_icons.py replace   swaps the glyph text layers left in the Strict frames for instances
"""
import base64
import json
import os
import re
import sys

from lib import FC  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
IDS = os.path.join(HERE, "icons.json")
MDI = os.path.join(HERE, "../sidecar/web/node_modules/@mdi/js/mdi.js")
NAME = "Strict · Иконки"
X, Y, SIZE, FAINT_VAR = 2780, 4960, 16, "VariableID:8"

# name: (MDI export, the Nerd Font glyph it replaces; nf-md-* share MDI's code points)
ICONS = {
    "plus": ("mdiPlus", "\U000f0415"), "chevron": ("mdiChevronDown", "\U000f0140"), "gear": ("mdiCogOutline", ""),
    "claude": ("mdiAsterisk", ""), "back": ("mdiArrowLeft", "\U000f004d"), "list": ("mdiFormatListBulleted", "\U000f0279"),
    "puzzle": ("mdiPuzzleOutline", "\U000f0a66"), "unfold": ("mdiUnfoldMoreHorizontal", "\U000f054f"),
    "search": ("mdiMagnify", "\U000f0349"), "alert": ("mdiAlert", "\U000f0026"), "attach": ("mdiFileOutline", "\U000f0224"),
    "book": ("mdiBookOutline", "\U000f0b64"), "pin": ("mdiPin", "\U000f0403"), "branch": ("mdiSourceBranch", "\U000f0568"),
    "doc": ("mdiFileDocument", "\U000f0219"), "image": ("mdiImage", "\U000f02e9"), "download": ("mdiDownload", "\U000f01da"),
    "close": ("mdiClose", "\U000f0156"), "lock": ("mdiLock", "\U000f033e"), "folder": ("mdiFolder", "\U000f024b"),
    "check": ("mdiCheck", "\U000f012c"), "done": ("mdiCheckCircle", "\U000f05e0"), "fix": ("mdiAutoFix", "\U000f0068"),
    "phone": ("mdiCellphone", "\U000f011c"), "palette": ("mdiPalette", "\U000f03d8"), "shape": ("mdiShapeOutline", "\U000f0832"),
    "file": ("mdiFile", "\U000f0214"),
}
GLYPHS = {g: n for n, (_, g) in ICONS.items()}


def ids():
    return json.load(open(IDS)) if os.path.exists(IDS) else {}


def components(fc):
    src = open(MDI).read()
    have = ids()
    known = {c["id"] for c in fc.cmd("component.list")}
    have = {n: i for n, i in have.items() if i in known}
    sec = next((t["id"] for t in fc.tops() if t["name"] == NAME), None)
    if sec is None:
        sec = fc.cmd("node.create", type="section", name=NAME, x=X, y=Y, width=40 + 9 * 56, height=40 + 3 * 56 + 40,
                     select=False)["id"]
    for k, (name, (export, _)) in enumerate(ICONS.items()):
        if name in have:
            continue
        d = re.search(rf'{export} = "([^"]+)"', src).group(1)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" viewBox="0 0 24 24">'
               f'<path fill="#878B94" d="{d}"/></svg>')
        f = fc.cmd("file.import", data=base64.b64encode(svg.encode()).decode(), name=name + ".svg")["id"]
        vec = fc.node(str(f), 1)["children"][0]["id"]
        fc.batch([
            {"command": "node.set", "params": {"ids": [vec], "props": {"name": "Vector", "constraints": {"horizontal": "scale", "vertical": "scale"}}}},
            {"command": "variable.bind", "params": {"ids": [vec], "field": "fill", "variable": FAINT_VAR}},
            {"command": "node.set", "params": {"ids": [f], "props": {"name": "Icon/" + name, "fills": []}}},
            {"command": "component.create", "params": {"ids": [f]}},
            {"command": "node.reparent", "params": {"ids": [f], "parent": sec}},
            {"command": "node.set", "params": {"ids": [f], "props": {"x": 40 + k % 9 * 56, "y": 60 + k // 9 * 56}}},
        ], "Icon/" + name)
        have[name] = f
    json.dump(have, open(IDS, "w"), indent=1)
    return have


def size_for(name, font):
    """The icon's box for a glyph drawn at `font` px: buttons and the header's chevron 16, menu leads 14, the agent's mark 12."""
    return 16 if name in ("Icon", "Chevron") and font >= 14 else 14 if font >= 13 else 12


def glyph_layers(fc):
    """Glyph text layers in the Strict frames: (parent, index, layer, index path from the page, inside an instance)."""
    out = []

    def walk(n, path, inst):
        for i, c in enumerate(n.get("children") or []):
            if c.get("type") == "TEXT" and c.get("characters") in GLYPHS:
                out.append((n, i, c, path + (i,), inst))
            walk(c, path + (i,), inst or c.get("type") == "INSTANCE")
    for t in fc.tops():
        if t["name"].startswith("Strict"):
            walk(fc.node(str(t["id"]), 40), (t["id"],), False)
    return out


def at(fc, trees, path):
    if path[0] not in trees:
        trees[path[0]] = fc.node(str(path[0]), 40)
    n = trees[path[0]]
    for i in path[1:]:
        n = (n.get("children") or [])[i]
    return n


def colour(vec, var, color):
    if var == FAINT_VAR:
        return []
    return [{"command": "variable.bind", "params": {"ids": [vec], "field": "fill", "variable": var}} if var else
            {"command": "node.set", "params": {"ids": [vec], "props": {"fills": [color]}}}]


def replace(fc, have):
    layers = glyph_layers(fc)
    own = [x for x in layers if not x[4]]
    print(len(own), "glyph layers;", len(layers) - len(own), "inside instances")
    cmds, made = [], []
    for parent, i, t, path, _ in own:
        s = size_for(t["name"], t.get("fontSize") or 14)
        r = {"$step": len(cmds)}
        cmds.append({"command": "instance.create", "params": {"component": have[GLYPHS[t["characters"]]], "parent": parent["id"]}})
        cmds.append({"command": "node.reparent", "params": {"ids": [r], "parent": parent["id"], "index": i}})
        props = {"name": t["name"], "width": s, "height": s}
        if (parent.get("layout") or {}).get("mode") in (None, "none"):
            props.update(x=t["x"] + (t["width"] - s) / 2, y=t["y"] + (t["height"] - s) / 2)
        cmds.append({"command": "node.set", "params": {"ids": [r], "props": props}})
        cmds.append({"command": "edit.delete", "params": {"ids": [t["id"]]}})
        made.append((r["$step"], t))
    res = fc.batch(cmds, "Icons for glyphs") if cmds else []
    sets = []
    for step, t in made:
        vec = fc.node(str(res[step]["id"]), 1)["children"][0]["id"]
        sets += colour(vec, (t.get("boundVariables") or {}).get("fill"), (t.get("fills") or [{}])[0].get("color"))
    if sets:
        fc.batch(sets, "Icon colours")
    # Instances whose glyph differed from their main's: the same place now holds an icon instance, swap it to theirs.
    trees, swaps, sets = {}, [], []
    for _, _, t, path, inst in layers:
        if not inst:
            continue
        n = at(fc, trees, path)
        if n.get("type") != "INSTANCE":
            print("not replaced:", path, t["name"])
            continue
        swaps.append({"command": "instance.swap", "params": {"ids": [n["id"]], "component": have[GLYPHS[t["characters"]]]}})
        sets.append((n["id"], t))
    if swaps:
        fc.batch(swaps, "Icons in instances")
        out = []
        for i, t in sets:
            vec = fc.node(str(i), 1)["children"][0]["id"]
            out += colour(vec, (t.get("boundVariables") or {}).get("fill"), (t.get("fills") or [{}])[0].get("color"))
        if out:
            fc.batch(out, "Icon colours in instances")


if __name__ == "__main__":
    fc = FC()
    have = components(fc)
    print(len(have), "icon components")
    if sys.argv[1:] == ["replace"]:
        replace(fc, have)
    fc.tool("save_file", {})
