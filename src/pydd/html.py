"""HTML formatter — interactive dumps from pydump.DumpNode."""

from __future__ import annotations

import html
from pathlib import Path
from typing import Any

from pydump.core import DumpNode, caller_frame, inspect_value
from pydump.core import caller_arg_names, format_dump_tip

_PACKAGE = Path(__file__).resolve().parent

_CSS = (
    'html,body{margin:0;padding:6px;background:#fff}'
    'pre.sf-dump{display:block;background:#18171B;color:#FF8400;'
    'font:12px Menlo,Monaco,Consolas,monospace;padding:5px;margin:0 0 1em;'
    'white-space:pre-wrap;word-break:break-all}'
    '.sf-dump-num{font-weight:bold;color:#1299DA}.sf-dump-const{font-weight:bold;color:#FF8400}'
    '.sf-dump-str{font-weight:bold;color:#56DB3A}.sf-dump-note{color:#1299DA}'
    '.sf-dump-ref{color:#A0A0A0}.sf-dump-key{color:#56DB3A}.sf-dump-index{color:#1299DA}'
    '.sf-dump-public{color:#FFF}.sf-dump-cls{color:#1299DA}.sf-dump-quote{color:#FF8400}'
    '.sf-dump-label{color:#B729D9;font:12px Menlo,Monaco,Consolas,monospace;padding:4px 5px 0}'
    '.sf-dump-compact{display:none}'
    'a.sf-dump-toggle{color:#FF8400;text-decoration:none;cursor:pointer}'
    'a.sf-dump-toggle .sf-dump-arrow{color:#A0A0A0}'
    # Expanded: tip after ▼ inside toggle. Collapsed: tip after ] (sf-dump-tip-out).
    '.sf-dump-tip-out{display:none}'
    'a.sf-dump-toggle:has(+samp.sf-dump-compact) .sf-dump-tip-in{display:none}'
    'a.sf-dump-toggle:has(+samp.sf-dump-compact)+samp+.sf-dump-tip-out{display:inline}'
)

_JS = (
    '<script>document.addEventListener("click",function(e){var a=e.target.closest'
    '&&e.target.closest("a.sf-dump-toggle");if(!a)return;e.preventDefault();'
    'var s=a.nextElementSibling;if(!s||s.tagName!=="SAMP")return;'
    'var c=s.classList.contains("sf-dump-compact");'
    's.className=c?"sf-dump-expanded":"sf-dump-compact";'
    'var ar=a.querySelector(".sf-dump-arrow");if(ar)ar.textContent=c?"▼":"▶";});</script>'
)


def _esc(v: Any) -> str:
    return html.escape(str(v), quote=True)


def _span(kind: str, text: str) -> str:
    return f'<span class=sf-dump-{kind}>{text}</span>'


def _tip(source: str | None) -> str:
    return f' {_span("ref", f"// {_esc(source)}")}' if source else ''


def _tip_in(tip: str) -> str:
    return f'<span class=sf-dump-tip-in>{tip}</span>' if tip else ''


def _tip_out(tip: str) -> str:
    return f'<span class=sf-dump-tip-out>{tip}</span>' if tip else ''


def _quoted(text: str) -> str:
    q = _span('quote', '"')
    return f'{q}{_span("str", _esc(text))}{q}'


def _key(raw: str) -> str:
    if raw.startswith('str:'):
        return _quoted(raw[4:])
    if raw.startswith('idx:'):
        return _span('index', _esc(raw[4:]))
    if raw.startswith('attr:'):
        return '+' + _span('public', _esc(raw[5:]))
    return _esc(raw)


def _scalar(node: DumpNode) -> str:
    sk = node.scalar_kind
    if sk in {'None', 'bool'}:
        return _span('const', _esc(node.text))
    if sk in {'int', 'float'}:
        return _span('num', _esc(node.text))
    if sk == 'str':
        return _quoted(node.text)
    return _span('str', _esc(node.text))


def format_node(
    node: DumpNode,
    *,
    depth: int = 0,
    max_depth: int = 1,
    tip: str = '',
) -> str:
    if node.kind in {'recursion', 'truncated'}:
        return _span('ref', _esc(node.text)) + tip
    if node.kind == 'scalar':
        return _scalar(node) + tip

    label = _span('note' if node.kind == 'container' else 'cls', _esc(node.label))
    if not node.children:
        return f'{label} []{tip}'

    expanded = depth < max_depth
    css = 'sf-dump-expanded' if expanded else 'sf-dump-compact'
    arrow = '▼' if expanded else '▶'
    pad, child = '  ' * depth, '  ' * (depth + 1)
    rows = ''.join(
        f'<br>{child}{_key(k)} => {format_node(c, depth=depth + 1, max_depth=max_depth)}'
        for k, c in node.children
    )
    # Expanded: tip after ▼. Collapsed: tip after ] (see CSS tip-in / tip-out).
    return (
        f'<a class="sf-dump-toggle">{label} '
        f'[<span class=sf-dump-arrow>{arrow}</span>{_tip_in(tip)}</a>'
        f'<samp class="{css}">{rows}<br>{pad}</samp>]{_tip_out(tip)}'
    )


def build_html(*args: Any, **kwargs: Any) -> str:
    skip = (str(_PACKAGE),)
    source = caller_frame(skip_packages=skip)
    values = list(args) + list(kwargs.values())
    labels = [None] * len(args) + [str(k) for k in kwargs]
    arg_names = caller_arg_names(skip_packages=skip)
    blocks: list[str] = []
    if not values:
        tip = _tip(source)
        body = _span('const', '🐛') + tip
        blocks.append(f'<pre class=sf-dump>{body}</pre>')
    else:
        for index, (label, value) in enumerate(zip(labels, values)):
            if label is None and index < len(arg_names):
                label = arg_names[index]
            tip = _tip(format_dump_tip(value, source=source, name=label, skip_packages=skip))
            head = f'<div class=sf-dump-label>{_esc(label)}</div>' if label else ''
            body = format_node(inspect_value(value), tip=tip)
            blocks.append(f'{head}<pre class=sf-dump>{body}</pre>')
    return (
        '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>dd()</title>'
        f'<style>{_CSS}</style>{_JS}</head><body>{"".join(blocks)}</body></html>'
    )
