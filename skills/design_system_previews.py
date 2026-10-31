#!/usr/bin/env python3
"""Build offline component specimens and foundation tables from each skill's local token snapshot.

python3 skills/design_system_previews.py --manifest /tmp/design-systems-render.json
node skills/render_collection_previews.mjs /tmp/design-systems-render.json

No upstream scripts or network resources are executed. Native token values remain in references/tokens.json;
layout dimensions are FigCraft specimen recipes, not a claim that every upstream component has that geometry.
"""
import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent / 'skills'
LABELS = {'background': 'Canvas', 'surface': 'Surface', 'muted': 'Subtle', 'text': 'Text', 'secondaryText': 'Secondary text',
          'primary': 'Primary action', 'onPrimary': 'On primary', 'selected': 'Selection', 'onSelected': 'On selection',
          'border': 'Border', 'focus': 'Focus', 'error': 'Error'}
FONT_SLUG = {'Roboto': 'roboto', 'Segoe UI': 'roboto', 'IBM Plex Sans': 'ibm-plex-sans', 'Inter': 'inter', 'Geist': 'geist'}


def esc(value):
    return html.escape(str(value), quote=True)


def css(value):
    value = str(value).strip()
    if re.search(r'[;{}<>]|url\s*\(|expression\s*\(', value, re.I):
        raise ValueError('Unexpected CSS token: ' + value)
    return value


def specimen(data, mode, slug):
    t = data['themes'][mode]
    d = data['dimensions']
    variables = ';'.join('--' + role + ':' + css(t[key]) for role, key in data['roles'].items())
    variables += ';' + ';'.join('--' + k + ':' + str(v) + 'px' for k, v in d.items())
    font_slug = FONT_SLUG[data['font']]
    fonts = ''.join(f"@font-face{{font-family:Specimen;src:url('fonts/{font_slug}-latin-{w}-normal.woff2') format('woff2');font-weight:{w};font-display:block}}" for w in (400, 500, 600, 700))
    version = data['snapshot'].get('version') or data['snapshot'].get('sha', '')[:10]
    role_tiles = ''.join(f'<div class="color"><span class="paint" style="background:var(--{role})"></span><b>{esc(LABELS[role])}</b><code>{esc(t[data["roles"][role]])}</code></div>' for role in ('surface', 'text', 'primary', 'onPrimary', 'selected', 'error'))
    brand = data['system']
    # These metrics describe the local specimen, while exact component source remains available in upstream/.
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=1080"><title>{esc(brand)} · {mode}</title>
<style>{fonts}
*{{box-sizing:border-box}}html,body{{width:1080px;height:720px;margin:0}}body{{{variables};font:var(--bodySize)/1.45 Specimen,Arial,sans-serif;background:var(--background);color:var(--text)}}
header{{height:104px;padding:24px 40px 20px;display:flex;align-items:center;gap:20px;border-bottom:1px solid var(--border)}}
.wordmark{{display:flex;align-items:center;gap:14px;flex:1}}.symbol{{width:40px;height:40px;background:var(--primary);color:var(--onPrimary);border-radius:var(--buttonRadius);display:grid;place-items:center;font-size:24px;font-weight:600}}
h1{{font-size:28px;line-height:36px;margin:0;font-weight:600;letter-spacing:-.02em}}header p{{margin:0;font-size:12px;color:var(--secondaryText)}}.version{{text-align:right;font-size:12px;color:var(--secondaryText)}}.version b{{display:block;color:var(--text);font-weight:500;margin-bottom:4px}}
main{{padding:24px 40px;display:grid;grid-template-columns:632px 344px;gap:24px;height:552px}}.column{{display:flex;flex-direction:column;gap:20px;min-width:0}}.panel{{border:1px solid var(--border);border-radius:var(--panelRadius);background:var(--surface);overflow:hidden}}.workspace{{height:286px}}.panel-title{{display:flex;gap:12px;align-items:center;padding:18px 20px 12px}}h2{{font-size:18px;font-weight:600;line-height:24px;margin:0;flex:1}}.status{{background:var(--selected);color:var(--onSelected);padding:3px 8px;font-size:11px;border-radius:var(--buttonRadius)}}
.tabs{{display:flex;gap:22px;padding:0 20px;border-bottom:1px solid var(--border);height:38px;align-items:flex-start;font-size:12px;color:var(--secondaryText)}}.tabs b{{color:var(--text);padding-bottom:12px;border-bottom:2px solid var(--primary);font-weight:600}}.content{{padding:18px 20px}}.form{{display:grid;grid-template-columns:1fr 150px;align-items:end;gap:12px}}label{{display:block;font-size:12px;font-weight:500;margin-bottom:7px}}input{{background:var(--surface);color:var(--text);border:1px solid var(--border);border-radius:var(--inputRadius);height:var(--inputHeight);width:100%;padding:0 12px;font:inherit;outline:none}}button{{font:500 14px/20px Specimen,Arial,sans-serif;height:var(--buttonHeight);border:1px solid var(--border);border-radius:var(--buttonRadius);padding:0 18px;background:var(--surface);color:var(--text);white-space:nowrap}}button.primary{{background:var(--primary);color:var(--onPrimary);border-color:var(--primary)}}.member{{display:flex;align-items:center;gap:10px;margin-top:18px;padding-top:14px;border-top:1px solid var(--border);font-size:12px}}.avatar{{width:28px;height:28px;border-radius:50%;background:var(--selected);color:var(--onSelected);display:grid;place-items:center;font-size:10px;font-weight:600}}.member span:nth-child(2){{flex:1}}.member small{{display:block;color:var(--secondaryText);font-size:11px}}.member em{{font-style:normal;color:var(--secondaryText)}}
.controls{{height:218px;padding:18px 20px}}.eyebrow{{font-size:11px;letter-spacing:.07em;text-transform:uppercase;color:var(--secondaryText);margin:0 0 14px;font-weight:600}}.buttons{{display:flex;gap:10px;align-items:center;margin-bottom:17px}}.focused{{outline:2px solid var(--focus);outline-offset:3px}}button:disabled{{opacity:.38}}.choices{{display:flex;gap:22px;align-items:center;margin:12px 0 14px;font-size:12px}}.choice{{display:flex;align-items:center;gap:7px}}.checkbox{{width:18px;height:18px;border:1px solid var(--primary);border-radius:2px;background:var(--primary);color:var(--onPrimary);font:600 12px/16px Specimen;text-align:center}}.radio{{width:18px;height:18px;border:5px solid var(--primary);border-radius:50%;background:var(--surface)}}.switch{{width:36px;height:20px;border-radius:20px;background:var(--primary);padding:3px;display:flex;justify-content:flex-end}}.switch i{{display:block;background:var(--onPrimary);width:14px;height:14px;border-radius:50%}}.error{{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--error)}}.error i{{font-style:normal;font-weight:700;border:1px solid currentColor;border-radius:50%;width:16px;height:16px;line-height:14px;text-align:center}}
.type{{height:224px;padding:18px 20px}}.type .sample{{font-size:42px;line-height:48px;letter-spacing:-.035em;margin:0 0 6px;font-weight:600}}.type .headline{{font-size:20px;line-height:28px;font-weight:600;margin:0 0 4px}}.type p{{font-size:12px;line-height:18px;color:var(--secondaryText);margin:0 0 14px}}.type code{{font-size:10px;color:var(--secondaryText);display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}.palette{{height:280px;padding:18px 20px}}.colors{{display:grid;grid-template-columns:1fr 1fr;gap:14px 12px}}.color{{min-width:0;display:grid;grid-template-columns:32px 1fr;column-gap:8px;align-items:center}}.paint{{grid-row:span 2;display:block;width:32px;height:34px;border:1px solid var(--border);border-radius:var(--inputRadius)}}.color b{{font-size:11px;line-height:15px;font-weight:500}}.color code{{font-size:8px;line-height:13px;color:var(--secondaryText);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}.token-note{{font-size:10px;color:var(--secondaryText);line-height:15px;margin:18px 0 0;padding-top:12px;border-top:1px solid var(--border)}}footer{{margin:8px 40px 0;display:flex;align-items:center;justify-content:space-between;height:40px;border-top:1px solid var(--border);font-size:10px;color:var(--secondaryText)}}
body[data-system="carbon"] header{{background:#161616;color:#fff}}body[data-system="carbon"] header p,body[data-system="carbon"] header .version,body[data-system="carbon"] header .version b{{color:#c6c6c6}}body[data-system="carbon"] .status{{border-radius:0}}body[data-system="carbon"] .content input{{border:0;border-bottom:1px solid var(--border);background:var(--muted)}}body[data-system="carbon"] .tabs{{gap:0}}body[data-system="carbon"] .tabs>*{{padding:0 16px 12px}}
body[data-system="material-3"] .tabs b{{color:var(--primary)}}body[data-system="material-3"] .workspace{{border:0;background:var(--muted)}}body[data-system="material-3"] .switch{{width:52px;height:32px;padding:4px}}body[data-system="material-3"] .switch i{{height:24px;width:24px}}body[data-system="material-3"] .choices{{margin-top:6px;margin-bottom:8px}}
body[data-system="material-ui"] .symbol{{border-radius:4px}}body[data-system="material-ui"] button{{text-transform:uppercase;letter-spacing:.02857em}}body[data-system="material-ui"] .tabs b{{text-transform:uppercase;color:var(--primary)}}
body[data-system="gravity-ui"] .status{{border-radius:4px}}body[data-system="gravity-ui"] .buttons button{{font-size:13px}}body[data-system="gravity-ui"] .tabs b{{border-bottom-width:3px}}
body[data-system="shadcn-ui"] .panel{{box-shadow:0 1px 2px #00000008}}body[data-system="shadcn-ui"] .tabs{{gap:4px;padding:0 16px;align-items:center;background:var(--muted)}}body[data-system="shadcn-ui"] .tabs>*{{padding:4px 10px;border:0;border-radius:6px}}body[data-system="shadcn-ui"] .tabs b{{background:var(--surface)}}
</style><body data-system="{esc(slug)}"><header><div class="wordmark"><span class="symbol">{esc(brand[0])}</span><div><h1>{esc(brand)}</h1><p>Tokens, typography & component states</p></div></div><div class="version"><b>{mode.capitalize()} theme</b>{esc(version)}</div></header>
<main><div class="column"><section class="panel workspace" data-component="workspace"><div class="panel-title"><h2>Project access</h2><span class="status">Active project</span></div><div class="tabs"><b>Members</b><span>Settings</span><span>Activity</span></div><div class="content"><div class="form"><div><label for="email">Invite by email</label><input id="email" value="alex@example.com" readonly data-component="input"></div><button class="primary" data-component="primary">Send invite</button></div><div class="member"><span class="avatar">AL</span><span>Alex Lee<small>alex@example.com</small></span><em>Editor</em><span>⌄</span></div></div></section>
<section class="panel controls" data-component="states"><p class="eyebrow">Interaction states</p><div class="buttons"><button class="primary">Default</button><button class="focused">Focused</button><button disabled>Disabled</button></div><div class="choices"><span class="choice"><i class="checkbox">✓</i>Selected</span><span class="choice"><i class="radio"></i>Option</span><span class="choice"><i class="switch"><i></i></i>Enabled</span></div><div class="error"><i>!</i>Please enter a valid email address.</div></section></div>
<div class="column"><section class="panel type" data-component="typography"><p class="eyebrow">Typography</p><div class="sample">Aa 123</div><div class="headline">Built to work together</div><p>Clear roles. Consistent components.<br>One system across every screen.</p><code>{esc(data['previewFont'])} · body {d['bodySize']}/{d['bodyLineHeight']} · label / heading</code></section><section class="panel palette" data-component="palette"><p class="eyebrow">Semantic color roles</p><div class="colors">{role_tiles}</div><p class="token-note">Theme values come from the local upstream snapshot.<br>Use the native token names in references/tokens.json.</p></section></div></main><footer><span>FigCraft component specimen · local editable-layout reference</span><span>{esc(data['previewFont'])} · {mode} specimen</span></footer></body></html>'''


def foundations(data):
    lines = [f"# {data['system']} · local foundations", '', 'Read this table before drawing. Exact native tokens, both theme maps and the pinned source are in [tokens.json](tokens.json).', '',
             'These are a pinned usable baseline, not a claim about the newest release. Keep a matching project theme or component version when one exists.', '',
             f"Font: **{data['font']}**. Local preview: {data['previewFont']}. Check installed fonts before creating text styles; report a substitution once and keep the text editable.", '',
             '| Semantic purpose | Native token | Light | Dark |', '|---|---|---|---|']
    for role, key in data['roles'].items():
        lines.append(f"| {LABELS[role]} | `{key}` | `{data['themes']['light'][key]}` | `{data['themes']['dark'][key]}` |")
    lines += ['', '## Component specimen recipe', '', 'The following px metrics define the local FigCraft specimen; use the retained component source for exact responsive, density and API variants. They are not new global design-system tokens.', '',
              '| Property | Value (px) |', '|---|---|']
    lines += [f'| {key} | {value} |' for key, value in data['dimensions'].items()]
    lines += ['', 'Keep native names when creating file variables. For dimensional values, resolve rem against the project root (the specimen uses 16px); retain unitless typography line-height as a multiplier. Preserve alias relationships where available in the upstream snapshots. Alpha colours need their alpha channel, not a darker opaque substitute.', '',
              'Bind background and on-background roles as pairs. Dark mode uses the dark role map, never automatic colour inversion. Specimen layout and content are examples; build the user’s requested screen with the selected system.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--manifest', type=Path, default=Path('/tmp/figcraft-design-systems-render.json'))
    args = parser.parse_args()
    jobs = []
    for folder in sorted(args.root.glob('design-*')):
        data = json.loads((folder / 'references/tokens.json').read_text())
        (folder / 'references/foundations.md').write_text(foundations(data))
        manifest = json.loads((folder / 'references.json').read_text())
        manifest['images'] = []
        for mode, label in [('light', 'Светлая'), ('dark', 'Тёмная')]:
            page = folder / f'assets/preview-{mode}.html'
            page.write_text(specimen(data, mode, folder.name.removeprefix('design-')))
            target = page.with_suffix('.webp')
            jobs.append({'html': str(page.resolve()), 'image': str(target.resolve()), 'kind': 'design-system'})
            manifest['images'].append({'file': str(target.relative_to(folder)), 'label': label})
        (folder / 'references.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    args.manifest.write_text(json.dumps({'previews': jobs}, indent=2) + '\n')
    print(f'{len(jobs)} local specimens prepared; render {args.manifest}')


if __name__ == '__main__':
    main()
