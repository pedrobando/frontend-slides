#!/usr/bin/env python3
"""Parse retreat-slide-outline.md into slide data (JSON).

Usage: python3 -I parse_outline.py <outline.md> <out.json>
"""
import json, re, sys

SLIDE_RE = re.compile(r'^#### (D[12])-(\d+) · (.+?) · ([\d.]+) min(?: \((.+?)\))?\s*$')
BLOCK_RE = re.compile(r'^## (Block \d+|Day \d close)\s*·?\s*(.*)$')
BLOCK_META_RE = re.compile(r'^\*\*(.+?)\*\*\s*$')
FIELD_RE = re.compile(r'^- \*\*(On screen|Visual|Speaker notes|Activity|Workbook):\*\*\s*(.*)$')
GAP_RE = re.compile(r'Gap:\s*([a-z ,/]+)', re.I)


def parse(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    blocks, slides = [], []
    block = None
    cur = None
    field = None
    for ln in lines:
        m = BLOCK_RE.match(ln)
        if m:
            name, title = m.group(1), m.group(2).strip()
            num = int(name.split()[1]) if name.startswith('Block') else (12.5 if '1' in name else 99)
            block = {'key': name, 'num': num, 'title': title or name, 'meta': '', 'gap': '', 'day': None}
            blocks.append(block)
            cur = None
            continue
        if block is not None and cur is None and not block['meta']:
            mm = BLOCK_META_RE.match(ln)
            if mm:
                block['meta'] = mm.group(1)
                g = GAP_RE.search(mm.group(1))
                block['gap'] = g.group(1).strip() if g else ''
                continue
        m = SLIDE_RE.match(ln)
        if m:
            day, n, typ, mins, window = m.groups()
            if block is not None and block['day'] is None:
                block['day'] = day
            cur = {
                'id': f'{day}-{n}', 'day': day, 'n': int(n), 'rawType': typ,
                'minutes': float(mins), 'window': window or '', 'block': block['key'] if block else '',
                'blockTitle': block['title'] if block else '',
                'gap': block['gap'] if block else '',
                'onScreen': '', 'visual': '', 'notes': '', 'activity': '', 'workbook': '',
            }
            slides.append(cur)
            field = None
            continue
        if cur is None:
            continue
        if ln.startswith('## ') or ln.startswith('### ') or ln.strip() == '---':
            cur = None
            field = None
            continue
        m = FIELD_RE.match(ln)
        if m:
            key = {'On screen': 'onScreen', 'Visual': 'visual', 'Speaker notes': 'notes',
                   'Activity': 'activity', 'Workbook': 'workbook'}[m.group(1)]
            cur[key] = m.group(2).strip()
            field = key
            continue
        if field and ln.strip() and not ln.startswith('#### '):
            cur[field] += ' ' + ln.strip()
    return blocks, slides


def base_type(raw):
    t = raw.split('(')[0].strip()
    if t.startswith('Workbook pointer'):
        return 'Workbook pointer'
    if t.startswith('Activity'):
        return 'Activity'
    return t


if __name__ == '__main__':
    blocks, slides = parse(sys.argv[1])
    for s in slides:
        s['type'] = base_type(s['rawType'])
    json.dump({'blocks': blocks, 'slides': slides}, open(sys.argv[2], 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(len(blocks), 'blocks', len(slides), 'slides',
          sum(1 for s in slides if s['day'] == 'D1'), 'D1',
          sum(1 for s in slides if s['day'] == 'D2'), 'D2')
    empty = [s['id'] for s in slides if not s['onScreen']]
    print('empty onScreen:', empty)
