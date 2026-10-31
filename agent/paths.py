"""Where a layer is: its path from the page, as one line an agent can act on.

`figcraft #ID TYPE «name» W×H — Page / Top › ◇Instance › … › name  (main: …)`; ◇ marks an
instance, so a change below it belongs in a main component listed after `main:` (outermost first).
"""

CONTAINERS = ("FRAME", "GROUP", "SECTION", "COMPONENT", "COMPONENT_SET", "INSTANCE", "BOOLEAN_OPERATION")


def _box(n):
    b = n.get("absoluteBounds")
    return (b["x"], b["y"], b["width"], b["height"]) if b else (n.get("x", 0), n.get("y", 0), n.get("width", 0), n.get("height", 0))


def _inside(inner, outer, eps=0.5):
    x, y, w, h = inner
    X, Y, W, H = outer
    return x >= X - eps and y >= Y - eps and x + w <= X + W + eps and y + h <= Y + H + eps


def _find(fc, nid, target, box, chain):
    """Depth-first, only into layers whose bounds contain the target's (cheap get_node calls)."""
    for c in fc.node(nid, 1).get("children") or []:
        if c["id"] == target:
            return chain + [c]
        if c.get("type") in CONTAINERS and c.get("childCount", 1) and _inside(box, _box(c)):
            r = _find(fc, c["id"], target, box, chain + [c])
            if r:
                return r


def _deep(n, target, chain):
    for c in n.get("children") or []:
        if c["id"] == target:
            return chain + [c]
        r = _deep(c, target, chain + [c])
        if r:
            return r


def path_of(fc, target, tops):
    """[top, …, layer] for a layer among `tops` (a page's top-level layers), or None."""
    node = fc.node(target, 0)
    box = _box(node)
    if any(t["id"] == target for t in tops):
        return [node]
    hits = [t for t in tops if _inside(box, _box(t))]
    for t in hits:
        r = _find(fc, t["id"], target, box, [t])
        if r:
            r[-1] = node
            return r
    for t in hits or tops:  # a layer may stick out of an unclipped parent: search the whole subtree
        r = _deep(fc.node(t["id"], 60), target, [t])
        if r:
            r[-1] = node
            return r


def facts(fc, target, tops):
    """The layer as the export names it: type, name, size, path, main components, text."""
    chain = path_of(fc, target, tops) or [fc.node(target, 0)]
    n = chain[-1]
    mains = [fc.node(c["id"], 0).get("mainComponentName") for c in chain if c.get("type") == "INSTANCE"]
    return {"id": target, "type": n.get("type"), "name": n.get("name"),
            "size": f"{n.get('width', 0):.0f}×{n.get('height', 0):.0f}",
            "path": " › ".join(("◇" if c.get("type") == "INSTANCE" else "") + str(c.get("name")) for c in chain),
            "mains": [m for m in mains if m], "text": n.get("characters"), "chain": chain}


def describe(fc, target, tops, page=None):
    f = facts(fc, target, tops)
    s = f"figcraft #{target} {f['type']} «{f['name']}» {f['size']} — {page + ' / ' if page else ''}{f['path']}"
    if f["mains"]:
        s += f"  (main: {' › '.join(f['mains'])})"
    if f["text"] is not None:
        s += f"  {f['text'][:60]!r}"
    return s
