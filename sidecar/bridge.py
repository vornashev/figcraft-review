#!/usr/bin/env python3
"""MCP server an agent runs in place of FigCraft's: it hands each request to the chat server, which runs it
in that file's own headless FigCraft (a guest in the app's live session), so agents in different files work
at once and whatever tab or workspace is in front.

  bridge.py --doc KEY --port 7980 --token TOKEN [--slot N] [--turn ID]      (server.py writes this into the MCP config)

Besides FigCraft's tools the agent gets build (a tree in one undo step), styles (the style library) and, outside a
variants lane (slot 0), variants (side-by-side variants by other agents); the server answers the last two itself.
"""
import json
import re
import sys
import urllib.error
import urllib.request


TREES = {"get_node", "inspect_document", "inspect_ui"}  # layer trees: what they leave out is the default
GRID = {"columnTracks", "rowTracks", "gridColumns", "gridRows"}


BUILD = {
    "name": "build",
    "description": (
        "Build layers from a nested tree in ONE undo step: the short way to make screens and blocks (it becomes a batch "
        "of node.create, variable.bind, style.apply, instance.create). A node: {type? (frame by default; text, "
        "rectangle, ellipse, line, vector, component, section…), name?, text? (for text), x?, y?, width?, height?, "
        "children? [nodes], textStyle? / fillStyle? / strokeStyle? / effectStyle? (a style's name or id), component? "
        "(name or id: an instance of it instead of a new layer), properties? (an instance's {name: value}), and any "
        "set_properties key (layout, gap, padding, sizingH, cornerRadius, fill, stroke, strokeWeight, …)}. A value "
        "\"$name\" binds that variable: \"fill\": \"$color/bg\", \"gap\": \"$space/md\". Prefer the file's variables and "
        "text styles to raw colours and font fields. A frame without a fill is transparent (not FigCraft's white), and "
        "a layout frame without a width/height or sizingH/sizingV hugs its content. Returns the new layers as {id, name} in tree order."),
    "inputSchema": {"type": "object", "required": ["tree"], "properties": {
        "tree": {"description": "A node or a list of nodes", "anyOf": [{"type": "object"}, {"type": "array", "items": {"type": "object"}}]},
        "parent": {"description": "Where the top nodes go (a frame id; default the page)", "anyOf": [{"type": "integer"}, {"type": "string"}]},
        "label": {"type": "string", "description": "Undo history label (default \"Build\")"}}},
}
STYLES = {
    "name": "styles",
    "description": (
        "The style library: design systems, component libraries and visual styles from every source the designer has "
        "(themes, the project's design systems, kits of ready components). Without name: a list, filtered by the words "
        "of query (mood, platform, source, e.g. \"editorial serif\", \"dashboard dark\", \"mobile\") and group "
        "(system|library|style). With name: that style in full — follow it; a library's screens are built from its "
        "components. Use it when the file has no design system of its own and no style was chosen, and to give each "
        "variant a different direction."),
    "inputSchema": {"type": "object", "properties": {
        "query": {"type": "string"}, "group": {"type": "string", "enum": ["system", "library", "style"]},
        "name": {"type": "string", "description": "A name from the list: load that style"}}},
}
SIZE = {"type": "object", "required": ["width", "height"],
        "properties": {"width": {"type": "number"}, "height": {"type": "number"}}}
VARIANTS = {
    "name": "variants",
    "description": (
        "Start side-by-side variants of the task: the chat puts one frame per direction in a row on the page and runs "
        "a lane for each — another agent, with its own cursor and undo — that designs a full independent take inside "
        "its frame. Call it once per turn, when the designer asks for several variants or options (or the message says "
        "×N), after choosing the directions with styles; then end your turn with a short plan and don't draw in the "
        "frames. When all lanes are done the chat asks you to compare them. axis: style (different styles, none "
        "repeated), structure (one system, different layouts) or adaptive (one design, a frame per device width). "
        "base: a top-level frame to redo — lanes get copies of it instead of empty frames. To mix variants («header "
        "from 1, cards from 3»): one direction whose brief names what to take from which frame (#id)."),
    "inputSchema": {"type": "object", "required": ["directions"], "properties": {
        "axis": {"type": "string", "enum": ["style", "structure", "adaptive"]},
        "base": {"type": "string", "description": "Id of the frame the variants redo; its size is the default"},
        "frame": {**SIZE, "description": "The anchor screen's size (not needed with base)"},
        "directions": {"type": "array", "minItems": 1, "maxItems": 6, "description": "One per variant, each really different",
                       "items": {"type": "object", "required": ["title", "idea"], "properties": {
                           "title": {"type": "string", "description": "2–3 words, names the frame"},
                           "idea": {"type": "string", "description": "The inspiration and what it gives this product"},
                           "style": {"type": "string", "description": "A name from styles"},
                           "frame": {**SIZE, "description": "This direction's own size (adaptive)"},
                           "brief": {"type": "string", "description": "What this variant does beyond the common task"}}}}}},
}
LANE = {
    "name": "lane",
    "description": (
        "Send work into an existing variant: the lane that drew variant n (its agent, session, frame and cursor) does "
        "brief — when the designer asks to refine one variant («second one: denser header»). Don't draw in its frame "
        "yourself."),
    "inputSchema": {"type": "object", "required": ["n", "brief"], "properties": {
        "n": {"type": "integer", "description": "The variant's number, as its frame is named"},
        "brief": {"type": "string", "description": "What to change, in the designer's words and yours"}}},
}
NODE_KEYS = {"type", "name", "text", "x", "y", "width", "height", "index", "path"}
STYLE_KEYS = {"textStyle": None, "fillStyle": "fill", "strokeStyle": "stroke", "effectStyle": None}
FIELDS = {"fills": "fill", "strokes": "stroke"}  # binding fields named after the property


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def expand(args, components=None):
    """build's tree as batch steps, and for each node made the index of its step and its name."""
    steps, made = [], []

    def add(node, parent):
        if not isinstance(node, dict):
            raise ValueError(f"a node must be an object, not {json.dumps(node)[:60]}")
        props, binds, styles = {}, [], []
        for k, v in node.items():
            if k in NODE_KEYS or k in ("children", "component", "properties"):
                continue
            if k in STYLE_KEYS:
                styles.append((v, STYLE_KEYS[k]))
            elif isinstance(v, str) and v.startswith("$") and len(v) > 1:
                binds.append((FIELDS.get(k, k), v[1:]))
            else:
                props[k] = v
        me = len(steps)
        if node.get("component") is not None:
            comp = node["component"]
            if not isinstance(comp, int):
                comp = (components() if components else {}).get(str(comp), comp)
            steps.append({"command": "instance.create", "params": {
                "component": comp, **{k: node[k] for k in ("x", "y") if k in node}, **({"parent": parent} if parent is not None else {})}})
            ref = {"$step": me}
            if node.get("name"):
                props["name"] = node["name"]
            props.update({k: node[k] for k in ("width", "height") if k in node})
            if props:
                steps.append({"command": "node.set", "params": {"ids": [ref], **props}})
            if node.get("properties"):
                steps.append({"command": "instance.setProperties", "params": {"ids": [ref], "properties": node["properties"]}})
        else:
            kind = node.get("type") or "frame"
            if kind == "frame":  # a container: see-through and, with a layout, the size of its content unless told
                if not {"fill", "fills", "fillStyle"} & node.keys():
                    props["fill"] = "none"
                if props.get("layout"):
                    for axis, size in (("sizingH", "width"), ("sizingV", "height")):
                        if axis not in node and size not in node:
                            props[axis] = "hug"
            params = {"type": kind, **{k: node[k] for k in NODE_KEYS - {"type"} if k in node}}
            if parent is not None:
                params["parent"] = parent
            if props:
                params["props"] = props
            params["select"] = False
            steps.append({"command": "node.create", "params": params})
            ref = {"$step": me}
        made.append((me, node.get("name") or node.get("text") or node.get("type") or "frame"))
        for style, target in styles:
            steps.append({"command": "style.apply", "params": {"ids": [ref], "style": style, **({"target": target} if target else {})}})
        for field, var in binds:
            steps.append({"command": "variable.bind", "params": {"ids": [ref], "field": field, "variable": var}})
        for child in node.get("children") or []:
            add(child, ref)

    tree = args.get("tree")
    for node in tree if isinstance(tree, list) else [tree]:
        add(node, args.get("parent"))
    return steps, made


def build(msg, send):
    """Runs a build call as one batch through the server; the answer lists the layers it made."""
    args = (msg.get("params") or {}).get("arguments") or {}
    cache = {}

    def components():  # instance.create takes an id: names are looked up once, only when used
        if "map" not in cache:
            out = send({"jsonrpc": "2.0", "id": msg["id"], "method": "tools/call",
                        "params": {"name": "run_command", "arguments": {"command": "component.list", "params": {}}}})
            try:
                items = json.loads(out["result"]["content"][0]["text"])
            except (KeyError, IndexError, ValueError, TypeError):
                items = []
            cache["map"] = {k: c["id"] for c in items if isinstance(c, dict) for k in (c.get("name"), c.get("label")) if k}
        return cache["map"]

    def answer(text, error=False):
        return {"jsonrpc": "2.0", "id": msg["id"], "result": {"content": [{"type": "text", "text": text}], "isError": error}}

    try:
        steps, made = expand(args, components)
    except ValueError as e:
        return answer(f"build: {e}", True)
    if not steps:
        return answer("build: an empty tree", True)
    out = send({"jsonrpc": "2.0", "id": msg["id"], "method": "tools/call", "params": {
        "name": "batch", "arguments": {"commands": steps, "label": args.get("label") or "Build"}}})
    res = out.get("result") or {}
    if "error" in out or res.get("isError"):
        return out
    try:
        results = json.loads(res["content"][0]["text"])
        ids = [{"id": results[i].get("id"), "name": name} for i, name in made]  # ids: the chat's «Показать» finds them
    except (KeyError, IndexError, ValueError, TypeError, AttributeError):
        return out
    return answer(json.dumps(ids, ensure_ascii=False, separators=(",", ":")))


def prune(o):
    """A layer tree without nulls, empty lists and objects, grid settings of non-grid layouts, and .0 on whole numbers."""
    if isinstance(o, dict):
        grid = o.get("mode") in (None, "grid")
        out = {}
        for k, v in o.items():
            if k in GRID and not grid:
                continue
            v = prune(v)
            if v is not None and v != [] and v != {}:
                out[k] = v
        return out
    if isinstance(o, list):
        return [prune(x) for x in o]
    if isinstance(o, float) and o.is_integer():
        return int(o)
    return o


COMMANDS_FULL = 6  # list_commands: how many commands keep their parameters when a filter finds more


def commands_brief(text, flt):
    """list_commands answers a filter with every command whose parameters mention it ("svg" brings node.create's
    whole docs): the commands named by the filter keep their parameters, the rest only their id and label, and a
    long list keeps parameters for the first few. A filter that is one command's exact id always gets it in full."""
    lines = text.splitlines()
    if len(lines) < 2 or not flt:
        return text
    q = str(flt).lower()
    full, kept = 0, [lines[0]]
    for line in lines[1:]:
        cid, _, rest = line.partition(" — ")
        label = re.split(r" [\[({]", rest, maxsplit=1)[0]
        named = q in cid.lower() or q in label.lower()
        if named and full < COMMANDS_FULL or cid.rstrip("*") == flt:
            full += 1
            kept.append(line)
        elif line.strip():
            kept.append(f"{cid} — {label}")
    if len(kept) - 1 > full:
        kept.append("(без параметров — те, где фильтр только в описании, или их много: list_commands с filter = id команды)")
    return "\n".join(kept)


def compact(msg, out):
    """FigCraft answers in indented JSON; the agent rereads every answer on each later step, so it gets them on one
    line (layer trees pruned too): half the characters, the same data."""
    tool = (msg.get("params") or {}).get("name") if msg.get("method") == "tools/call" else None
    for c in ((out.get("result") or {}).get("content") or []) if tool else []:
        if c.get("type") != "text":
            continue
        if tool == "list_commands":
            c["text"] = commands_brief(c.get("text") or "", ((msg["params"].get("arguments") or {}).get("filter")))
            continue
        try:
            data = json.loads(c["text"])
        except (ValueError, TypeError):
            continue
        c["text"] = json.dumps(prune(data) if tool in TREES else data, ensure_ascii=False, separators=(",", ":"))
    return out


def tools_for(slot):
    """The tools the bridge adds to FigCraft's: a variants lane (slot ≠ 0) can't start or steer variants."""
    return [BUILD, STYLES] + ([VARIANTS, LANE] if str(slot) == "0" else [])


def main():
    # MCP speaks UTF-8; Windows would otherwise use its code page and fail on the first «→» in a tool's description
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    slot = arg("--slot", "0")
    url = f"http://127.0.0.1:{arg('--port')}/api/mcp?doc={arg('--doc')}&slot={slot}&turn={arg('--turn', '')}"
    extra = tools_for(slot)
    token = arg("--token")

    def send(msg):
        req = urllib.request.Request(url, json.dumps(msg).encode(), {"Content-Type": "application/json", "X-Agent-Token": token})
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                return json.load(r)
        except (urllib.error.URLError, OSError, ValueError) as e:
            body = getattr(e, "read", lambda: b"")()
            try:
                text = json.loads(body).get("error") or str(e)
            except ValueError:
                text = str(e)
            return {"jsonrpc": "2.0", "id": msg["id"], "error": {"code": -32000, "message": f"FigCraft Agent: {text}"}}

    for line in sys.stdin:
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        if "id" not in msg:  # notifications: the guest was initialised by the server already
            continue
        if msg.get("method") == "tools/call" and (msg.get("params") or {}).get("name") == "build":
            out = build(msg, send)
        else:
            out = compact(msg, send(msg))
            if msg.get("method") == "tools/list" and isinstance((out.get("result") or {}).get("tools"), list):
                out["result"]["tools"].extend(extra)
        sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
