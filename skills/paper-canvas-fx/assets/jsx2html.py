#!/usr/bin/env python3
"""Minimal converter: Paper get_jsx (inline-styles format) -> plain HTML.
Not a general JSX transpiler; handles exactly what Paper emits."""
import re, sys

def split_top(s, sep):
    out, depth, q, cur = [], 0, None, ''
    for c in s:
        if q:
            cur += c
            if c == q: q = None
            continue
        if c in '"\'': q = c; cur += c; continue
        if c in '([{': depth += 1
        elif c in ')]}': depth -= 1
        if c == sep and depth == 0:
            out.append(cur); cur = ''
        else:
            cur += c
    if cur.strip(): out.append(cur)
    return out

def kebab(k):
    out = re.sub(r'([A-Z])', lambda m: '-' + m.group(1).lower(), k)
    for v in ('webkit', 'moz', 'ms', 'o'):
        if out.startswith(v + '-'): return '-' + out
    return out

def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] in '"\'' and v[-1] == v[0]:
        return v[1:-1]
    return v

def conv_style(m):
    body = m.group(1)
    parts = split_top(body, ',')
    decls = []
    for p in parts:
        if ':' not in p: continue
        i = p.index(':')
        k = p[:i].strip()
        val = unquote(p[i+1:])
        decls.append(f"{kebab(k)}: {val}")
    return "style='" + '; '.join(decls) + "'"

def convert(jsx):
    s = jsx.strip()
    s = re.sub(r'^\(\s*', '', s)
    s = re.sub(r'\s*\)\s*$', '', s)
    # style={{ ... }} -> style='...'
    s = re.sub(r"style=\{\{(.*?)\}\}", conv_style, s, flags=re.S)
    # SVG / presentation camelCase attributes -> kebab
    for a in ('strokeWidth','strokeLinecap','strokeLinejoin','fillRule','fontSize','clipRule'):
        s = s.replace(a + '=', kebab(a) + '=')
    # expand self-closing div/span (HTML has no self-closing non-void tags)
    s = re.sub(r'<(div|span)\b([^>]*?)\s*/>', r'<\1\2></\1>', s, flags=re.S)
    return s

if __name__ == '__main__':
    print(convert(open(sys.argv[1]).read()))
