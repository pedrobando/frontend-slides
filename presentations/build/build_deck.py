"""Build retreat-2027-day-1.html and retreat-2027-day-2.html from build/slides.json.

Run from anywhere:  python3 -I presentations/build/build_deck.py
Look and runtime come from build/shell-phase1.html (never edited here).
Media is optional: drop media/retreat-2027/<id>.jpg (photo) or <id>.mp4 (story clip), then rebuild.
"""
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PRES = os.path.dirname(HERE)
MEDIA = 'media/retreat-2027'
SHELL = open(os.path.join(HERE, 'shell-phase1.html'), encoding='utf-8').read()
SLIDES = json.load(open(os.path.join(HERE, 'slides.json'), encoding='utf-8'))['slides']


# ---------------------------------------------------------------- shell pieces
def between(a, b, s=SHELL, inclusive=True):
    i = s.index(a)
    j = s.index(b, i) + (len(b) if inclusive else 0)
    return s[i:j] if inclusive else s[i + len(a):j]


STYLE = between('<style>', '</style>', inclusive=False)
RCLIPS = between('<!-- @@R-CLIPS@@ -->', '<!-- /@@R-CLIPS@@ -->')
SNOW = between('<!-- @@SNOWFLAKE@@ -->', '<!-- /@@SNOWFLAKE@@ -->')
FONTS_HEAD = re.search(r'<script>\(function\(\)\{var d=document\.documentElement.*?</script>', SHELL).group(0)
rt_start = SHELL.index('/* Deck runtime')
RUNTIME = SHELL[SHELL.rindex('<script>', 0, rt_start):SHELL.index('</script>', rt_start) + 9]
FILM = re.search(r'<section class="slide slide--film dark" data-slide-id="d1-snowflake".*?</section>', SHELL, re.S).group(0)
LEARN = re.search(r'<section class="slide slide--learn" data-slide-id="d1-s3".*?</section>', SHELL, re.S).group(0)
COVER1 = re.search(r'<section class="slide slide--cover dark" data-slide-id="d1-cover".*?</section>', SHELL, re.S).group(0)

# runtime patches: session from meta, C = city, V = visual notes
RUNTIME = RUNTIME.replace(
    "var slides = [].slice.call(document.querySelectorAll('.slide'));",
    "var slides = [].slice.call(document.querySelectorAll('.slide'));\n"
    "  var SESSION = (document.querySelector('meta[name=\"presentation-session\"]') || {}).content || '1';", 1)
assert "session: '1'" in RUNTIME
RUNTIME = RUNTIME.replace("session: '1'", 'session: SESSION')
RUNTIME = RUNTIME.replace(
    "      case 'F5': return true;",
    "      case 'c': case 'C': if (window.cityCycle) window.cityCycle(); return true;\n"
    "      case 'v': case 'V': root.classList.toggle('show-vis'); return true;\n"
    "      case 'F5': return true;", 1)
assert 'cityCycle' in RUNTIME and 'show-vis' in RUNTIME

CITY_HEAD = """<script>(function(){var d=document.documentElement,c='mke';try{c=localStorage.getItem('retreat-city')||c}catch(e){}
var q=location.search.match(/[?&]city=(mke|fl)/);if(q)c=q[1];d.setAttribute('data-city',c);
window.cityCycle=function(){var n=d.getAttribute('data-city')==='fl'?'mke':'fl';d.setAttribute('data-city',n);
try{localStorage.setItem('retreat-city',n)}catch(e){}var t=document.querySelector('.city-toast');
if(t){t.textContent=n==='fl'?'Florida':'Milwaukee';t.classList.add('on');clearTimeout(t._h);t._h=setTimeout(function(){t.classList.remove('on')},1400)}};})();</script>"""

# ---------------------------------------------------------------- text helpers
WORDNUM = {w: i for i, w in enumerate('zero one two three four five six seven eight nine ten eleven twelve'.split())}


def clean(s):
    s = re.sub(r'\s*—\s*', ', ', s or '')
    s = s.replace('–', '-')
    for a, b in (('“', '"'), ('”', '"'), ('‘', "'"), ('’', "'")):
        s = s.replace(a, b)
    return s.strip()


def strip_q(s):
    s = clean(s)
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        s = s[1:-1]
    return s.strip()


def esc(s):
    return html.escape(s, quote=False)


def attr(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')


def rich(s):
    """Escape, then mark [Pedro: x] placeholders and ____ blanks."""
    s = esc(s)
    s = re.sub(r'\[Pedro:\s*([^\]]*)\]', r'<span class="pedro">Pedro: \1</span>', s)
    s = re.sub(r'_{3,}', '<span class="blank-line"></span>', s)
    return s


UL = '<svg class="ul" viewBox="0 0 200 14" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" d="M2 9 C 50 2, 100 14, 198 6"/></svg>'


def hl(inner_html, blue=False):
    return f'<span class="hl{" hl--blue" if blue else ""}">{inner_html}{UL}</span>'


def sentences(s):
    return [p for p in re.split(r'(?<=[.?!])\s+(?=[^a-z])', s.strip()) if p]


def headline(s, mark=True):
    parts = sentences(s)
    if mark and len(parts) >= 2 and len(parts[-1]) <= 28 and '[' not in parts[-1]:
        parts[-1] = hl(rich(parts[-1]))
        return '<br>'.join([rich(p) for p in parts[:-1]] + [parts[-1]])
    return '<br>'.join(rich(p) for p in parts)


def size_cls(s):
    n = len(s)
    return 's1' if n <= 22 else 's2' if n <= 40 else 's3' if n <= 64 else 's4'


def city(mke, fl):
    return f'<span class="city-mke">{mke}</span><span class="city-fl">{fl}</span>'


def media(sid, ext):
    p = f'{MEDIA}/{sid.lower()}.{ext}'
    return p if os.path.exists(os.path.join(PRES, p)) else None


# ---------------------------------------------------------------- content fixes
def sub(s, old, new):
    if old not in s:
        raise SystemExit(f'Monday rewrite missed: {old!r}')
    return s.replace(old, new)


MONDAY = {
    'D1-03': [('notes', 'read their numbers every Friday', 'read their Monday planning report every week')],
    'D1-42': [('notes', "Friday, 30 minutes, 'Score my week.", "Monday, 30 minutes, 'Planning report.")],
    'D1-43': [('onScreen', 'Every Friday.', 'Every Monday.'),
              ('visual', 'single Friday calendar icon', 'single Monday calendar icon'),
              ('notes', 'Right side, Friday, 30 minutes: write the week', 'Right side, Monday, 30 minutes, your planning report: write last week')],
    'D1-44': [('notes', 'Friday blocked?', 'Monday report blocked?')],
    'D1-105': [('notes', 'Mention the Friday self-audit: anyone untouched in five days gets touched before the weekend.',
                'Mention the self-audit in the Monday planning report: anyone untouched in five days gets touched that day.')],
    'D2-29': [('notes', 'Every Friday you write four numbers', 'Every Monday, in your planning report, you write four numbers')],
    'D2-30': [('onScreen', 'Set the Friday reminder.', 'Set the Monday reminder.')],
    'D2-49': [('notes', 'Every Friday', 'Every Monday')],
    'D2-51': [('onScreen', 'Fridays', 'Mondays'), ('notes', 'every Friday', 'every Monday')],
    'D2-67': [('onScreen', 'Text your score Friday.', 'Your total goes in the Monday report.'),
              ('notes', 'text your total on Friday', 'your total goes in your Monday planning report')],
    'D2-120': [('onScreen', 'Friday, Jan 8.', 'Monday, Jan 11.'),
               ('notes', 'Friday, January 8: your first Friday score, texted to your partner',
                'Monday, January 11: your first Monday planning report, shared with your partner'),
               ('workbook', '(Friday score)', '(Monday report)')],
}
KEEP_FRIDAY = {'D2-25', 'D1-39', 'D1-41'}

for s in SLIDES:
    for f in ('onScreen', 'visual', 'notes', 'activity', 'workbook'):
        s[f] = clean(s[f])
    s['onScreen'] = strip_q(s['onScreen'])
    for f, old, new in MONDAY.get(s['id'], []):
        s[f] = sub(s[f], old, new)
    if s['id'] in MONDAY:
        for f in ('onScreen', 'visual', 'notes', 'activity', 'workbook'):
            s[f] = re.sub(r'\bFriday', 'Monday', s[f])
BY = {s['id']: s for s in SLIDES}


# ---------------------------------------------------------------- shared parts
def notes_for(s, extra_cues=()):
    mins = s['minutes']
    m = f"{int(mins) if mins == int(mins) else mins} min"
    win = f" ({s['window']})" if s['window'] else ''
    cues = [f"> {s['id']} · {s['rawType']} · {m}{win}"]
    cues += [f'> {c}' for c in extra_cues]
    if s['activity']:
        cues.append(f"> Activity: {s['activity']}")
    if s['workbook'] and s['workbook'].lower() != 'none':
        cues.append(f"> Workbook: {s['workbook']}")
    if s['visual']:
        cues.append(f"> Visual: {s['visual']}")
    return '\n'.join(cues) + '\n\n' + s['notes']


def foot(s):
    return f'<div class="foot"><span>2027 Agent Retreat · Paso a paso.</span><span>{esc(s["blockTitle"])} · {s["id"]}</span></div>'


def vis(s):
    return f'<div class="vis"><b>Visual</b> {rich(s["visual"])}</div>' if s['visual'] else ''


def eyebrow(s, text=None):
    return f'<p class="eyebrow reveal">{esc(text or s["blockTitle"])}</p>'


def section(s, cls, inner, sid=None, notes=None, extra=''):
    sid = sid or s['id']
    n = notes if notes is not None else notes_for(s)
    return (f'<!-- {sid} -->\n<section class="slide {cls}" data-slide-id="{sid.lower()}"{extra} data-notes="{attr(n)}">\n'
            f'{inner}\n{vis(s)}\n</section>\n')


def timer_sec(s):
    t = s['onScreen']
    m = re.search(r'\b(\d+|' + '|'.join(WORDNUM) + r') minutes?\b', t, re.I)
    if m:
        v = m.group(1).lower()
        return int(WORDNUM.get(v, v) if not v.isdigit() else v) * 60
    for p in sentences(t):
        m = re.fullmatch(r'(?:Live: )?(\d+) seconds\.', p)
        if m:
            return int(m.group(1))
    m = re.search(r'(\d+)\s*min', s['activity'])
    if m:
        return int(m.group(1)) * 60
    return int(s['minutes'] * 60) if s['minutes'] else 0


def timer(sec, lg=False):
    if not sec:
        return ''
    lab = f'{sec // 60} MIN' if sec >= 120 or sec % 60 == 0 and sec >= 60 else f'{sec} SEC'
    return f'<span class="timer{" lg" if lg else ""}" data-sec="{sec}">{lab}</span>'


def variant(s):
    m = re.search(r'\(([^)]*)\)', s['rawType'])
    return m.group(1) if m else ''


def wb_ref(s):
    """('Open the Mind', '9') from the workbook field, or page from on-screen."""
    m = re.search(r'Page (\d+)', s['onScreen'])
    wm = re.search(r'^(.*?)\s*p\.\s?(\d+)', s['workbook'])
    book = wm.group(1).strip() if wm else ''
    page = m.group(1) if m else (wm.group(2) if wm else '')
    return book, page


def strip_meta(t):
    t = re.sub(r'Page \d+\.\s*', '', t)
    t = re.sub(r'\s*\b(\d+|' + '|'.join(WORDNUM) + r') minutes?( each| a round)?\.', '', t, flags=re.I)
    t = re.sub(r'\s*\b\d+ seconds( each)?\.', '', t)
    return t.strip()


# ---------------------------------------------------------------- renderers
def r_image(s):
    t = s['onScreen']
    photo = media(s['id'], 'jpg')
    bg = f'<img class="bgimg" src="{photo}" alt=""><div class="bgshade"></div>' if photo else ''
    wm = '<img class="wm abs" src="media/retreat-2027/logo-wordmark-white.png" alt="reThought Real Estate">' if s['id'] == 'D1-01' else ''
    cues = [] if photo else [f'Photo slot: add {MEDIA}/{s["id"].lower()}.jpg and rebuild.']
    tag = f'<div class="meta"><span class="tag amber">Move</span></div>' if 'movement' in s['rawType'] else ''
    inner = (f'{bg}<div class="frame bottom">{wm}{tag}{eyebrow(s)}'
             f'<h1 class="reveal d1 {size_cls(t)}">{headline(t)}</h1>{foot(s)}</div>')
    return section(s, 'slide--image dark' + (' has-photo' if photo else ''), inner, notes=notes_for(s, cues))


POLLS = {'D1-92': ['5 min', '1 hour', 'Same day', 'Tomorrow'],
         'D2-23': ['Daily panic', 'Once a week', 'When I remember'],
         'D2-77': ['10', '20', '30 or more']}


def r_question(s):
    t = s['onScreen']
    meta = []
    if 'movement' in s['rawType'] or 'whip' in s['rawType']:
        meta.append(f'<span class="tag amber">{esc(variant(s).split(":")[0].title() or "Move")}</span>')
    if s['id'] in POLLS:
        meta.append('<span class="tag">Hands up</span>')
    chips = ''
    if s['id'] in POLLS:
        chips = '<ul class="poll stagger">' + ''.join(f'<li>{esc(o)}</li>' for o in POLLS[s['id']]) + '</ul>'
    m = f'<div class="meta">{"".join(meta)}</div>' if meta else ''
    inner = (f'<div class="frame center">{m}{eyebrow(s)}<h1 class="reveal d1 {size_cls(t)}">{headline(t, mark=False)}</h1>'
             f'{chips}{foot(s)}</div>')
    return section(s, 'slide--question dark', inner)


def fw_items(t):
    for sep in (' → ', ' · ', ' + '):
        if sep in t:
            return [x.strip() for x in t.split(sep)]
    ps = sentences(t)
    if len(ps) >= 2 and all(' = ' in p for p in ps):
        return ps
    if len(ps) >= 3 and all(len(p.split()) <= 3 and '?' not in p for p in ps):
        return [p.rstrip('.') for p in ps]
    return None


def r_framework(s):
    t = s['onScreen']
    if s['id'] == 'D1-11':
        en, es = [x.strip() for x in t.split(' / ')]
        inner = (f'<div class="frame center">{eyebrow(s, "The rule · two days")}'
                 f'<h1 class="reveal d1 s2">{headline(en)}</h1><p class="es-line reveal d2" lang="es">{esc(es)}</p>{foot(s)}</div>')
        return section(s, 'slide--statement dark', inner)
    if s['id'] == 'D1-94':
        return r_r04(s)
    items = fw_items(t)
    if not items:
        inner = f'<div class="frame center">{eyebrow(s)}<h2 class="reveal d1 big2">{headline(t)}</h2>{foot(s)}</div>'
        return section(s, 'slide--fw', inner)
    arrow = ' → ' in t
    boxes = []
    for i, it in enumerate(items, 1):
        if ' = ' in it:
            a, b = it.rstrip('.').split(' = ', 1)
            body = f'<b>{rich(a)}</b><small>{rich(b)}</small>'
        else:
            body = f'<b>{rich(it)}</b>'
        boxes.append(f'<li><span class="n">{i}</span>{body}</li>')
    cls = 'fw arrows' if arrow else 'fw'
    inner = (f'<div class="frame center">{eyebrow(s)}'
             f'<ol class="{cls} n{len(items)} stagger">{"".join(boxes)}</ol>{foot(s)}</div>')
    return section(s, 'slide--fw', inner)


def r_contrast(s):
    t = s['onScreen']
    if ' | ' in t:
        a, b = [x.strip() for x in t.split(' | ')]
        inner = (f'<div class="frame center">{eyebrow(s)}<div class="vs stagger">'
                 f'<div class="vs-a"><p class="k">Not this</p><h2>{rich(a)}</h2></div><span class="vs-x">vs</span>'
                 f'<div class="vs-b"><p class="k">This</p><h2>{rich(b)}</h2></div></div>{foot(s)}</div>')
        return section(s, 'slide--contrast bone', inner)
    inner = f'<div class="frame center">{eyebrow(s)}<h1 class="reveal d1 {size_cls(t)}">{headline(t)}</h1>{foot(s)}</div>'
    return section(s, 'slide--contrast bone', inner)


def r_story(s):
    t = s['onScreen']
    live = 'live demo' in s['rawType']
    clip = media(s['id'], 'mp4')
    meta = '<div class="meta"><span class="tag">Live</span>' + timer(timer_sec(s)) + '</div>' if live else ''
    if clip:
        inner = (f'<div class="vid-wrap" data-src="{clip}"><video playsinline muted preload="none"></video><div class="vid-shade"></div>'
                 f'<div class="frame center vid-card">{eyebrow(s, "Story")}<h2>{rich(t)}</h2>'
                 '<p class="vid-hint"><span class="play"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.5v15l12.5-7.5z" fill="currentColor"/></svg></span>Click to play</p></div>'
                 '<div class="vid-over"><span class="vid-tag">Dramatization · made-up names</span><div class="vid-lines"></div></div></div>')
        return section(s, 'slide--video dark', inner)
    cue = [f'Story slot: tell it live, or drop {MEDIA}/{s["id"].lower()}.mp4 and rebuild.']
    inner = (f'<div class="frame center">{meta}{eyebrow(s, "Live demo" if live else "Story")}'
             f'<h1 class="reveal d1 {size_cls(t)}">{headline(t)}</h1>{foot(s)}</div>')
    return section(s, 'slide--story dark', inner, notes=notes_for(s, cue))


def r_commit(s):
    t = s['onScreen']
    sec = timer_sec(s)
    tag = '<span class="tag amber">Move</span>' if 'movement' in s['rawType'] else '<span class="tag">Commit</span>'
    inner = (f'<div class="frame center"><div class="meta">{tag}{timer(sec)}</div>{eyebrow(s)}'
             f'<h1 class="reveal d1 {size_cls(t)}">{headline(t)}</h1>'
             f'<div class="lines commit reveal d2"><i></i><i></i></div>{foot(s)}</div>')
    return section(s, 'slide--bridge dark', inner)


BIGNUM_CAP = {'D1-24': 'Sample page: sphere dollars back per dollar spent',
              'D1-93': 'Personal touches in four months vs. where most agents stop',
              'D2-54': 'Days from first click to keys',
              'D2-98': 'Six months of waiting, on the sample',
              'D2-107': city('Wisconsin · weekends count', 'Florida · ask me, MLS rules vary')}


def r_bignum(s):
    t = s['onScreen']

    def tok(w):
        if '[' in w:
            return w
        return f'<b>{esc(w)}</b>' if re.search(r'\d', w) else f'<small>{esc(w)}</small>'
    pieces = re.split(r'(\[Pedro:[^\]]*\]|\s+)', t)
    out = []
    for p in pieces:
        if not p:
            continue
        if p.startswith('[Pedro'):
            out.append(rich(p))
        elif p.isspace():
            out.append(' ')
        else:
            out.append(tok(p))
    lines = ''.join(out)
    lines = lines.replace('</small> <b>1</b>', '</small><br><b>1</b>', 1) if s['id'] == 'D1-103' else lines
    cap = BIGNUM_CAP.get(s['id'])
    cap = f'<p class="lead reveal d2">{cap}</p>' if cap else ''
    inner = f'<div class="frame center">{eyebrow(s)}<p class="bignum reveal d1">{lines}</p>{cap}{foot(s)}</div>'
    return section(s, 'slide--bignum dark', inner)


def r_activity(s):
    t = s['onScreen']
    sec = timer_sec(s)
    book, page = wb_ref(s)
    eb = ' · '.join(x for x in ('Workbook', book, f'Page {page}' if page else '') if x) if (book or page) else s['blockTitle']
    rest = strip_meta(t)
    v = variant(s)
    if s['id'] == 'D2-50' or ' · ' in rest and len(sentences(rest)) == 1:
        steps_html = '<ul class="poll left stagger">' + ''.join(f'<li>{rich(x)}</li>' for x in rest.split(' · ')) + '</ul>'
        head = f'<h2 class="reveal d1">{esc(v.split(":")[-1].strip().capitalize() or "Four corners")}</h2>'
    else:
        steps = sentences(rest)
        if len(steps) <= 1:
            head = f'<h2 class="reveal d1 act-h">{headline(rest)}</h2>'
            steps_html = ''
        else:
            head = ''
            steps_html = '<ol class="steps stagger">' + ''.join(
                f'<li><span class="n">{i}</span><span>{rich(p)}</span></li>' for i, p in enumerate(steps, 1)) + '</ol>'
    tagcls = 'tag amber' if 'movement' in v or 'role' in v else 'tag'
    vtag = f'<span class="{tagcls}">{esc(v.split(":")[0])}</span>' if v else '<span class="tag">Do it</span>'
    side = f'<aside class="act-side reveal d2">{timer(sec, lg=True)}{vtag}</aside>' if sec else f'<aside class="act-side">{vtag}</aside>'
    inner = (f'<div class="frame">{eyebrow(s, eb)}<div class="act">'
             f'<div class="act-main">{head}{steps_html}</div>{side}</div>{foot(s)}</div>')
    return section(s, 'slide--act bone', inner)


def r_pointer(s):
    t = s['onScreen']
    book, page = wb_ref(s)
    rest = strip_meta(t)
    sec = timer_sec(s) if 'activity' in s['rawType'] or re.search(r'minutes?\.', t) else 0
    big = f'<p class="wbp-n">p.&#8239;{page}</p>' if page else ''
    inner = (f'<div class="frame center"><div class="meta"><span class="tag">Open the book</span>{timer(sec)}</div>'
             f'{eyebrow(s, book or s["blockTitle"])}<div class="wbp reveal d1">{big}'
             f'<h2>{headline(rest)}</h2></div>{foot(s)}</div>')
    return section(s, 'slide--wbp bone', inner)


def r_break(s):
    t = s['onScreen']
    word = 'Almuerzo' if s['type'] == 'Lunch' else 'Break'
    back = re.search(r'Back at ([\d:]+)', t).group(1)
    extra = '<p class="lead reveal d2">Film your hook.</p>' if 'Film your hook' in t else ''
    inner = (f'<div class="frame center"><div class="meta">{timer(int(s["minutes"] * 60))}</div>'
             f'<p class="brk reveal" lang="{"es" if word == "Almuerzo" else "en"}">{word}</p>'
             f'<h2 class="reveal d1">Back at {hl(back)}</h2>{extra}{foot(s)}</div>')
    return section(s, 'slide--break dark', inner)


# ---------------------------------------------------------------- special slides
def r_film(s):
    shell_notes = re.search(r'data-notes="(.*?)"', FILM, re.S).group(1).split('\n---\n')[0]
    cues = [ln[2:] for ln in html.unescape(shell_notes).split('\n') if ln.startswith('> ')]
    sec = FILM.replace('<h2 data-b="2">Every snowflake is different.</h2>', '<h2 data-b="2">No two alike.</h2>')
    assert 'No two alike.' in sec
    sec = re.sub(r'data-notes=".*?"', lambda m: f'data-notes="{attr(notes_for(s, cues))}"', sec, count=1, flags=re.S)
    return f'<!-- {s["id"]} -->\n' + sec + '\n'


def r_r04(s):
    frame = re.search(r'<div class="frame">.*</div>\s*</section>', LEARN, re.S).group(0)[:-len('</section>')].rstrip()
    frame = re.sub(r'<p class="eyebrow">.*?</p>', f'<p class="eyebrow">{esc(s["blockTitle"])}</p>', frame, count=1)
    frame = re.sub(r'<div class="foot">.*?</div>', foot(s), frame, count=1, flags=re.S)
    cues = ['Let the clip run once. Point to day 3: most agents quit here.']
    return section(s, 'slide--learn', frame, notes=notes_for(s, cues))


def cover2():
    c = COVER1
    c = c.replace('data-slide-id="d1-cover"', 'data-slide-id="d2-cover"')
    c = re.sub(r'data-notes=".*?"', 'data-notes="' + attr(
        '> Walk on with the cover up.\n\nDía 2. Yesterday we opened the mind and set the target. Today we build the machine: '
        'social media, el motor, buyers, listings. Books open.') + '"', c, count=1, flags=re.S)
    c = c.replace('Agent Retreat · 2027 plan · Day 1', 'Agent Retreat · 2027 plan · Day 2')
    c = re.sub(r'<h1 class="reveal d1">.*?</h1>', f'<h1 class="reveal d1">From knowing<br>to {hl("doing.")}</h1>', c, count=1, flags=re.S)
    c = re.sub(r'<p class="lead reveal d2">.*?</p>', '<p class="lead reveal d2">Social media. El motor. Buyers. Listings.</p>', c, count=1)
    return '<!-- D2 cover -->\n' + c + '\n'


def sample_tag():
    return '<span class="tag sample-tag">Sample · made-up</span>'


def worked(s, body, h=None):
    t = h or s['onScreen']
    inner = (f'<div class="frame"><div class="meta">{sample_tag()}</div><div class="head">{eyebrow(s, s["blockTitle"] + " · Worked example")}'
             f'<h2 class="reveal d1">{headline(t)}</h2></div><div class="body">{body}</div>{foot(s)}</div>')
    return section(s, 'slide--worked bone', inner)


def W_D1_25(s):
    body = ('<div class="row-sheet reveal d1"><div><p class="k">Source</p><p class="v">Open houses</p></div>'
            '<div><p class="k">Closings</p><p class="v">3</p></div><div><p class="k">GCI</p><p class="v">$21,000</p></div>'
            '<div><p class="k">Cost</p><p class="v">$450</p></div></div>'
            f'<p class="calc reveal d2">$21,000 ÷ $450 = {hl("about 47 to 1")}</p>')
    return worked(s, body)


def W_D1_32(s):
    body = ('<p class="calc wrong reveal d1"><s>$82,400 ÷ 75 = $1,099</s></p>'
            '<p class="calc reveal d2">$82,400 ÷ <span class="circ">0.75</span> = <b class="g">$109,867</b></p>'
            '<p class="note reveal d3">Keep 75%? Divide by 0.75. That is the GCI you need.</p>')
    return worked(s, body)


def W_D1_48(s):
    body = (f'<div class="card quote reveal d1"><p class="k">I am the agent who…</p>'
            f'<p class="qt">{hl("calls back")} every lead before 7 PM, even on game nights.</p></div>')
    return worked(s, body)


def W_D1_61(s):
    body = ('<div class="g2 cities stagger">'
            '<div class="card c-mke"><p class="k">Milwaukee</p><p class="qt">I help Bay View condo owners move up to a house without moving twice.</p>'
            '<p class="eg">Proved by a written move plan.</p></div>'
            '<div class="card c-fl"><p class="k">Florida</p><p class="qt">I help Poinciana renters turn their rent into a payment they own.</p>'
            '<p class="eg">Proved by a payment worksheet before we tour.</p></div></div>')
    return worked(s, body)


def W_D1_75(s):
    rows = [('The home', '1950s Cape Cod, West Allis', 'Pool home, Kissimmee'),
            ('The problem', 'Old water stains scared buyers off', 'Green pool in the old photos'),
            ('The fix', 'We got the dry-basement report up front', 'Cleaned it, reshot at golden hour'),
            ('The result', 'Three offers the first weekend', 'Under contract in a week')]
    body = '<ol class="steps story4 stagger">' + ''.join(
        f'<li><span class="n">{i}</span><span><b class="k">{a}</b> {city(m, f)}</span></li>' for i, (a, m, f) in enumerate(rows, 1)) + '</ol>'
    return worked(s, body)


def W_D1_107(s):
    rows = [('Leads', 220, ''), ('Conversations', 90, '41%'), ('Set', 36, '40%'), ('Held', 27, '75%'), ('Signed', 14, '52%'), ('Closed', 11, '79%')]
    out = []
    for name, n, pct in rows:
        low = pct == '40%'
        p = f'<span class="pct{" circ" if low else ""}">{pct}</span>' if pct else '<span class="pct"></span>'
        out.append(f'<li{" class=low" if low else ""}><span class="fn">{name}</span><span class="bar" style="--w:{n / 220:.3f}"><b>{n}</b></span>{p}</li>')
    body = '<ul class="funnel stagger">' + ''.join(out) + '</ul><p class="note reveal d3">The leak is the smallest percent: conversations to set.</p>'
    return worked(s, body)


def W_D2_11(s):
    rows = [('HOA fees', "Everyone says run from HOAs. Here's when I tell buyers to pick one."),
            ('Property tax bill', "If you're fighting your assessment without this, stop.")]
    body = '<div class="rebuild stagger">' + ''.join(
        f'<div class="rb"><p class="rb-a"><span class="k">Boring</span>{esc(a)}</p><span class="arr">→</span><p class="rb-b"><span class="k">Rebuilt</span>"{esc(b)}"</p></div>'
        for a, b in rows) + '</div>'
    return worked(s, body)


def W_D2_18(s):
    hooks = [('Hot take', "Unpopular opinion: closing costs aren't the scary part."),
             ('Myth', 'Everyone says the seller pays closing costs. Not always.'),
             ('Story', 'I almost lost a buyer at the closing table over this.')]
    body = ('<p class="k reveal">Topic: closing costs</p><div class="g3 stagger">' + ''.join(
        f'<div class="card"><p class="k">{a}</p><p class="qt sm">"{esc(b)}"</p></div>' for a, b in hooks) + '</div>')
    return worked(s, body)


def W_D2_25(s):
    eps = [('Ep 1', 'What $1,800 a month gets you'), ('Ep 2', 'The down payment, for real'), ('Ep 3', 'Your first year, both ways')]
    body = '<div class="reels stagger">' + ''.join(
        f'<div class="reel"><p class="k">Rent vs. Own Friday · {e}</p><p class="rt">{esc(t)}</p></div>' for e, t in eps) + '</div>'
    return worked(s, body)


def W_D2_39(s):
    def card(cls, name, rows, hook):
        li = ''.join(f'<li><b>{a}</b> {esc(b)}</li>' for a, b in rows)
        return f'<div class="card {cls}"><p class="k">{name}</p><ul class="av">{li}</ul><p class="qt sm">"{esc(hook)}"</p></div>'
    mke = card('c-mke', 'Milwaukee buyer', [('11 PM:', 'looking at duplexes, wondering if upstairs rent covers the mortgage'),
                                             ('Tried:', 'asked a friend who said wait'), ('Afraid:', 'not "investor" material')],
               "Your upstairs tenant could pay half your mortgage. Here's how it works.")
    fl = card('c-fl', 'Florida buyer', [('11 PM:', 'checking their credit score again'),
                                        ('Tried:', 'an online calculator that said no'), ('Afraid:', 'credit will keep them renting forever')],
              "Think your credit's too low to buy in Kissimmee? Let's actually check.")
    return worked(s, f'<div class="g2 cities stagger">{mke}{fl}</div>')


def W_D2_99(s):
    rows = [('Sale price', '$415,000'), ('Payoff', '−$236,000'), ('Fee', 'As agreed in writing'),
            ('Closing costs', '−$5,200'), ('Taxes, prorated', '−$3,100')]
    li = ''.join(f'<li><span>{a}</span><b{" class=blank" if a == "Fee" else ""}>{b}</b></li>' for a, b in rows)
    body = f'<ul class="sheet reveal d1">{li}<li class="tot"><span>What you walk away with</span><b class="blank-line"></b></li></ul>'
    return worked(s, body)


WORKED = {'D1-25': W_D1_25, 'D1-32': W_D1_32, 'D1-48': W_D1_48, 'D1-61': W_D1_61, 'D1-75': W_D1_75,
          'D1-107': W_D1_107, 'D2-11': W_D2_11, 'D2-18': W_D2_18, 'D2-25': W_D2_25, 'D2-39': W_D2_39, 'D2-99': W_D2_99}


# ---------------------------------------------------------------- multiple choice
MC = {
    'D1-25': [dict(q='Marisol has two sources. Portal: $1,200 cost, 1 deal, $6,000 GCI. Sphere: $300 cost, 2 deals, $14,000 GCI. Which pays her back more?',
                   o=['Portal, about 5 to 1', 'Sphere, about 47 to 1', 'Same, both made deals', "Can't tell without more months"], a=1,
                   why='GCI ÷ cost. $14,000 ÷ $300 is about 47. $6,000 ÷ $1,200 is 5.')],
    'D1-94': [dict(q='Which one counts as a touch?',
                   o=['An automatic drip email', 'Your monthly newsletter', 'A 20-second video text that says his name', 'A like on his post'], a=2,
                   why='A touch is you, live or personal. Automatic messages and likes do not count.')],
    'D1-97': [dict(q='Day 5. Ana has not answered. Which text do you send?',
                   o=['"Just checking in!"', '"Hi Ana, any update?"',
                      '"Ana, 2 new 3-bedrooms hit today in ' + city('West Allis', 'Kissimmee') + '. Want the links?"', 'Wait for her to reach out'], a=2,
                   why='Bring something new. Her name, a real reason, one easy yes.', raw=True)],
    'D2-37': [dict(q='Which detail belongs in your buyer avatar?',
                   o=['Their age', 'Their religion', 'What they check on their phone at 11 PM', 'How many kids they have'], a=2,
                   why='The worry, not the demographic. And religion or family status never goes in an ad.')],
    'D2-39': [dict(q='Which is the better hook?',
                   o=['"Call the #1 agent in Central Florida"', '"Tired of rent going up every lease? Let\'s see what a payment looks like."',
                      '"Homes for sale. Contact me today."', '"Great rates on homes this month!"'], a=1,
                   why='It names their problem in their words, then offers one small next step.')],
    'D2-49': [dict(q='Day 7. Same $180 on each ad. Ad A: 20 leads, 1 booked. Ad B: 8 leads, 4 booked. Which ad wins?',
                   o=['Ad A, more leads', 'Ad B, more appointments'], a=1,
                   why='Ad B: $45 per appointment. Ad A: $180. Count chairs, not clicks.')],
    'D2-80': [dict(q='You expect multiple offers. What is your first move?',
                   o=['Write the highest price', 'Call the listing agent first', 'A personal letter with a family photo', 'Waive the inspection'], a=1,
                   why='Ask what the seller cares about before you write a word. Skip the photo letter, it is a Fair Housing risk.'),
              dict(q='The listing agent says the seller needs 30 days after closing. What do you offer?',
                   o=['A rent-back', 'Add $5,000', 'Ask the seller for closing costs', 'A shorter inspection'], a=0,
                   why='Ease. Solve their real problem and you can win without the most money.')],
    'D2-110': [dict(q='Three showings. No feedback after 24 hours. What do you do?',
                    o=['Wait, they are busy', 'Call each showing agent', 'Email the seller the showing count', 'Lower the price'], a=1,
                    why='No news is still a call. Get the feedback, then bring numbers to the seller.')],
}


def r_mc(s, mc, k):
    sid = f'{s["id"]}Q{k}' if k > 1 else f'{s["id"]}Q'
    opts = ''.join(
        f'<li class="opt{" ans" if i == mc["a"] else ""}"><b>{"ABCD"[i]}</b><span>{o if mc.get("raw") else esc(o)}</span></li>'
        for i, o in enumerate(mc['o']))
    notes = (f'> {sid} · Quick check · after {s["id"]}\n> Read it out. Hands up for '
             + ', '.join("ABCD"[:len(mc["o"])]) + '. Count. Click to reveal.\n> Answer: '
             + "ABCD"[mc['a']] + '\n\n' + mc['why'])
    inner = (f'<div class="frame mc"><div class="meta"><span class="tag">Hands up</span></div><div class="head">'
             f'{eyebrow(s, s["blockTitle"] + " · Quick check")}<h2 class="reveal d1 mc-q">{esc(mc["q"])}</h2></div>'
             f'<div class="body"><ol class="opts n{len(mc["o"])} stagger">{opts}</ol>'
             f'<p class="why frag"><b>{"ABCD"[mc["a"]]}.</b> {esc(mc["why"])}</p></div>{foot(s)}</div>')
    return (f'<!-- {sid} -->\n<section class="slide slide--mc bone" data-slide-id="{sid.lower()}" data-notes="{attr(notes)}">\n'
            f'{inner}\n</section>\n')


# ---------------------------------------------------------------- dispatch
def render(s):
    sid, ty = s['id'], s['type']
    if sid == 'D1-07':
        return r_film(s)
    if sid in WORKED:
        return WORKED[sid](s)
    if ty == 'Image + headline':
        return r_image(s)
    if ty == 'Big question':
        return r_question(s)
    if ty == 'Simple framework':
        return r_framework(s)
    if ty == 'Contrast':
        return r_contrast(s)
    if ty == 'Story prompt':
        return r_story(s)
    if ty == 'Commitment':
        return r_commit(s)
    if ty == 'Big number':
        return r_bignum(s)
    if ty == 'Activity':
        return r_activity(s)
    if ty == 'Workbook pointer':
        return r_pointer(s)
    if ty in ('Break', 'Lunch'):
        return r_break(s)
    raise SystemExit(f'no renderer for {sid} {ty}')


EXTRA_CSS = r"""
/* ================= retreat full decks (build_deck.py) ================= */
.frame.bottom{justify-content:flex-end;gap:calc(var(--u)*28);padding-bottom:calc(var(--u)*190)}
h1.s1{font-size:calc(var(--u)*150)} h1.s2{font-size:calc(var(--u)*124)} h1.s3{font-size:calc(var(--u)*100)} h1.s4{font-size:calc(var(--u)*82)}
h1{text-wrap:balance} h2{text-wrap:balance}
.dark .hl{color:var(--sprout)}
.slide.slide--image{background:radial-gradient(ellipse 70% 60% at 80% 0%,rgba(3,76,118,.5),transparent 70%),radial-gradient(ellipse 60% 50% at 0% 100%,rgba(140,201,78,.12),transparent 70%),var(--ink-deep)}
.bgimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.bgshade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(18,26,34,.1) 30%,rgba(18,26,34,.88) 100%)}
.slide.slide--question{background:radial-gradient(ellipse 60% 55% at 50% 110%,rgba(3,76,118,.55),transparent 70%),var(--ink-deep)}
.slide.slide--story{background:radial-gradient(ellipse 50% 60% at 100% 50%,rgba(224,166,58,.14),transparent 70%),var(--ink-deep)}
.slide.slide--bignum{background:radial-gradient(ellipse 60% 60% at 50% 50%,rgba(140,201,78,.10),transparent 70%),var(--ink-deep)}
.slide.slide--break{background:linear-gradient(135deg,#0E2233 0%,var(--ink-deep) 70%)}
.pedro{display:inline-block;font-family:var(--font-display);font-weight:600;font-size:.42em;letter-spacing:0;line-height:1.25;vertical-align:middle;
  background:var(--amber-light);color:#6B4A0E;border:2px dashed var(--amber);border-radius:calc(var(--u)*14);padding:.25em .6em;max-width:calc(var(--u)*1300);white-space:normal;text-align:left}
.blank-line{display:inline-block;width:3.2em;border-bottom:.08em solid currentColor;vertical-align:baseline;margin:0 .12em}
.vis{display:none;position:absolute;z-index:9;left:calc(var(--u)*24);right:calc(var(--u)*24);top:calc(var(--u)*24);padding:calc(var(--u)*16) calc(var(--u)*22);
  background:rgba(255,248,230,.96);color:#4A3608;border:2px solid var(--amber);border-radius:calc(var(--u)*14);font-size:calc(var(--u)*22);line-height:1.4}
.vis b{font-family:var(--font-display);text-transform:uppercase;letter-spacing:.1em;margin-right:.5em}
html.show-vis .vis{display:block}
.es-line{font-family:var(--font-display);font-weight:600;font-size:calc(var(--u)*56);color:var(--muted-2)}
.poll{display:flex;gap:calc(var(--u)*20);flex-wrap:wrap;margin-top:calc(var(--u)*24)}
.poll li{font-family:var(--font-display);font-weight:600;font-size:calc(var(--u)*40);padding:calc(var(--u)*18) calc(var(--u)*36);border-radius:999px;border:2px solid var(--dline);background:rgba(251,251,251,.05)}
.bone .poll li{border-color:var(--line);background:var(--paper)}
.poll.left{margin-top:calc(var(--u)*32)}
.bignum{font-family:var(--font-display);font-weight:700;line-height:1;letter-spacing:-.03em;font-size:calc(var(--u)*260)}
.bignum b{color:var(--sprout);font-weight:700}
.bignum small{font-size:.32em;font-weight:600;letter-spacing:0;color:var(--muted-2)}
.bignum .pedro{font-size:.2em}
/* framework */
.slide--fw .big2{font-size:calc(var(--u)*96)}
.fw{display:flex;gap:calc(var(--u)*24);align-items:stretch;margin-top:calc(var(--u)*24)}
.fw li{flex:1;min-width:0;background:var(--card);border-radius:calc(var(--u)*22);padding:calc(var(--u)*32) calc(var(--u)*24);display:flex;flex-direction:column;gap:calc(var(--u)*18);position:relative}
.fw li b{font-family:var(--font-display);font-weight:700;font-size:calc(var(--u)*48);line-height:1.1}
.fw li small{font-size:calc(var(--u)*30);color:var(--muted);line-height:1.3}
.fw.n5 li b,.fw.n6 li b{font-size:calc(var(--u)*34)}
.fw li:last-child{background:var(--sprout-light)}
.fw li:last-child .n{background:var(--sprout-deep)}
.fw.arrows{gap:calc(var(--u)*44)}
.fw.arrows li:not(:last-child)::after{content:"→";position:absolute;right:calc(var(--u)*-36);top:50%;transform:translateY(-50%);font-family:var(--font-display);font-weight:700;font-size:calc(var(--u)*34);color:var(--muted-2)}
/* contrast */
.vs{display:grid;grid-template-columns:1fr auto 1fr;gap:calc(var(--u)*40);align-items:center;margin-top:calc(var(--u)*24)}
.vs>div{border-radius:calc(var(--u)*24);padding:calc(var(--u)*56);display:flex;flex-direction:column;gap:calc(var(--u)*16)}
.vs h2{font-size:calc(var(--u)*92)}
.vs-a{background:var(--clay-light)} .vs-a h2{color:var(--clay)}
.vs-b{background:var(--sprout-light)} .vs-b h2{color:var(--sprout-deep)}
.vs-x{font-family:var(--font-display);font-weight:700;font-size:calc(var(--u)*40);color:var(--muted)}
/* commitment */
.lines.commit{max-width:calc(var(--u)*1200);margin-top:calc(var(--u)*48)}
.lines.commit i{background:var(--dline);height:3px}
/* activity */
.act{flex:1;display:grid;grid-template-columns:1fr calc(var(--u)*420);gap:calc(var(--u)*64);align-items:center;padding-bottom:calc(var(--u)*80)}
.act-main{display:flex;flex-direction:column;gap:calc(var(--u)*24)}
.act-h{font-size:calc(var(--u)*88)}
.steps{display:flex;flex-direction:column;gap:calc(var(--u)*26)}
.steps li{display:flex;gap:calc(var(--u)*28);align-items:center;font-family:var(--font-display);font-weight:600;font-size:calc(var(--u)*58);line-height:1.12}
.steps .n{width:calc(var(--u)*64);height:calc(var(--u)*64);font-size:calc(var(--u)*30)}
.act-side{display:flex;flex-direction:column;gap:calc(var(--u)*24);align-items:stretch;text-align:center}
.timer.lg{font-size:calc(var(--u)*72);padding:calc(var(--u)*40) calc(var(--u)*24);border-radius:calc(var(--u)*32);letter-spacing:.04em}
.act-side .tag{align-self:center;background:var(--paper)}
.tag.amber{background:var(--amber-light);color:#6B4A0E}
.act-side .tag.amber{background:var(--amber-light)}
/* workbook pointer */
.wbp{display:flex;gap:calc(var(--u)*72);align-items:center}
.wbp-n{flex:none;font-family:var(--font-display);font-weight:700;font-size:calc(var(--u)*220);line-height:1;color:var(--brand);letter-spacing:-.03em}
.wbp h2{font-size:calc(var(--u)*80)}
/* break */
.brk{font-family:var(--font-display);font-weight:700;font-size:calc(var(--u)*240);line-height:1;letter-spacing:-.03em}
/* worked examples */
.sample-tag{background:var(--amber-light);color:#6B4A0E}
.slide--worked .body{gap:calc(var(--u)*36)}
.row-sheet{display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;background:var(--paper);border-radius:calc(var(--u)*22);border:1px solid var(--line);overflow:hidden}
.row-sheet>div{padding:calc(var(--u)*28) calc(var(--u)*32);border-left:1px solid var(--line);display:flex;flex-direction:column;gap:calc(var(--u)*10)}
.row-sheet>div:first-child{border-left:0}
.row-sheet .v{font-family:var(--font-display);font-weight:700;font-size:calc(var(--u)*56)}
.calc{font-family:var(--font-display);font-weight:700;font-size:calc(var(--u)*76);line-height:1.15}
.calc.wrong{color:var(--clay);font-size:calc(var(--u)*56)} .calc.wrong s{text-decoration-thickness:.08em}
.calc .g{color:var(--sprout-deep)}
.circ{display:inline-block;border:.06em solid var(--sprout);border-radius:999px;padding:0 .25em}
.card.quote{background:var(--paper);padding:calc(var(--u)*56)}
.qt{font-family:var(--font-display);font-weight:600;font-size:calc(var(--u)*60);line-height:1.2}
.qt.sm{font-size:calc(var(--u)*40)}
.cities .card{background:var(--paper);padding:calc(var(--u)*44);gap:calc(var(--u)*20)}
.cities .qt{font-size:calc(var(--u)*46)}
.cities .c-mke{order:0} .cities .c-fl{order:1}
html[data-city="fl"] .cities .c-fl{order:-1}
.story4 li{font-size:calc(var(--u)*50)}
.story4 .k{display:inline-block;width:calc(var(--u)*300);font-size:calc(var(--u)*24)}
.funnel{display:flex;flex-direction:column;gap:calc(var(--u)*14)}
.funnel li{display:grid;grid-template-columns:calc(var(--u)*320) 1fr calc(var(--u)*160);gap:calc(var(--u)*24);align-items:center}
.fn{font-family:var(--font-display);font-weight:600;font-size:calc(var(--u)*34)}
.bar{display:block;height:calc(var(--u)*58);width:calc(var(--w) * 100%);min-width:calc(var(--u)*90);background:var(--brand);border-radius:calc(var(--u)*12);color:var(--paper);display:flex;align-items:center;padding-left:calc(var(--u)*20);font-family:var(--font-display);font-size:calc(var(--u)*30)}
.funnel li.low .bar{background:var(--clay)}
.pct{font-family:var(--font-display);font-weight:700;font-size:calc(var(--u)*38);text-align:center}
.pct.circ{border-color:var(--clay);color:var(--clay)}
.rebuild{display:flex;flex-direction:column;gap:calc(var(--u)*28)}
.rb{display:grid;grid-template-columns:calc(var(--u)*440) auto 1fr;gap:calc(var(--u)*32);align-items:center}
.rb p{border-radius:calc(var(--u)*20);padding:calc(var(--u)*32);display:flex;flex-direction:column;gap:calc(var(--u)*10);font-family:var(--font-display);font-weight:600}
.rb-a{background:var(--card);color:var(--muted);font-size:calc(var(--u)*40)}
.rb-b{background:var(--paper);font-size:calc(var(--u)*40);line-height:1.2}
.arr{font-family:var(--font-display);font-size:calc(var(--u)*48);color:var(--sprout-deep)}
.g3 .card{background:var(--paper);padding:calc(var(--u)*40)}
.reels{display:flex;gap:calc(var(--u)*40);justify-content:center}
.reel{width:calc(var(--u)*330);height:calc(var(--u)*560);border-radius:calc(var(--u)*28);padding:calc(var(--u)*32);display:flex;flex-direction:column;justify-content:space-between;
  background:linear-gradient(180deg,rgba(18,26,34,.2),rgba(18,26,34,.9)),linear-gradient(135deg,var(--brand),var(--sprout-deep));color:var(--paper)}
.reel .k{color:var(--sprout)}
.rt{font-family:var(--font-display);font-weight:700;font-size:calc(var(--u)*44);line-height:1.1}
.av{display:flex;flex-direction:column;gap:calc(var(--u)*12);font-size:calc(var(--u)*30);line-height:1.35}
.av b{font-family:var(--font-display)}
.sheet{background:var(--paper);border:1px solid var(--line);border-radius:calc(var(--u)*22);max-width:calc(var(--u)*1100);width:100%}
.sheet li{display:flex;justify-content:space-between;align-items:baseline;padding:calc(var(--u)*22) calc(var(--u)*40);border-top:1px solid var(--line);font-size:calc(var(--u)*38)}
.sheet li:first-child{border-top:0}
.sheet b{font-family:var(--font-display);font-weight:700;font-variant-numeric:tabular-nums}
.sheet b.blank{color:var(--muted);font-weight:600;font-style:italic}
.sheet .tot{background:var(--sprout-light);color:var(--sprout-deep);font-family:var(--font-display);font-weight:700;font-size:calc(var(--u)*44);border-radius:0 0 calc(var(--u)*22) calc(var(--u)*22)}
.sheet .tot .blank-line{width:calc(var(--u)*260)}
/* multiple choice */
.mc-q{font-size:calc(var(--u)*62);max-width:calc(var(--u)*1560)}
.opts{display:grid;grid-template-columns:1fr 1fr;gap:calc(var(--u)*22)}
.opt{display:flex;gap:calc(var(--u)*24);align-items:center;background:var(--paper);border:2px solid var(--line);border-radius:calc(var(--u)*22);padding:calc(var(--u)*26) calc(var(--u)*30);
  font-family:var(--font-display);font-weight:600;font-size:calc(var(--u)*36);line-height:1.2;transition:opacity .4s,background .4s,border-color .4s}
.opt b{flex:none;width:calc(var(--u)*60);height:calc(var(--u)*60);border-radius:50%;background:var(--ink);color:var(--paper);display:grid;place-items:center;font-size:calc(var(--u)*30)}
.opts.n2 .opt{font-size:calc(var(--u)*52);padding:calc(var(--u)*44)}
.why{font-size:calc(var(--u)*34);line-height:1.35;color:var(--sprout-deep);font-weight:700;font-family:var(--font-display)}
.mc:has(.why.on) .opt{opacity:.38}
.mc:has(.why.on) .opt.ans{opacity:1;background:var(--sprout-light);border-color:var(--sprout)}
.mc:has(.why.on) .opt.ans b{background:var(--sprout-deep)}
/* city switch (C key or ?city=fl) */
.city-fl{display:none}
html[data-city="fl"] .city-mke{display:none}
html[data-city="fl"] .city-fl{display:inline}
.city-toast{position:fixed;z-index:99;left:50%;bottom:calc(var(--u)*40);transform:translate(-50%,20px);opacity:0;pointer-events:none;transition:opacity .3s,transform .3s;
  font-family:var(--font-display);font-weight:600;text-transform:uppercase;letter-spacing:.1em;font-size:calc(var(--u)*24);background:var(--paper);color:var(--ink);padding:calc(var(--u)*14) calc(var(--u)*28);border-radius:999px}
.city-toast.on{opacity:1;transform:translate(-50%,0)}
@media print{
  .vis,.city-toast{display:none!important}
  .mc .opt.ans{background:var(--sprout-light)!important;border-color:var(--sprout)!important}
}
"""


# ---------------------------------------------------------------- assemble
DAYS = {
    'D1': dict(file='retreat-2027-day-1.html', title='Day 1 · Open the mind. Set the target.', session='1', date='2026-11-19'),
    'D2': dict(file='retreat-2027-day-2.html', title='Day 2 · Build the machine.', session='2', date='2026-11-20'),
}


def build(day):
    cfg = DAYS[day]
    parts = [COVER1 + '\n' if day == 'D1' else cover2()]
    for s in [x for x in SLIDES if x['day'] == day]:
        parts.append(render(s))
        for k, mc in enumerate(MC.get(s['id'], []), 1):
            parts.append(r_mc(s, mc, k))
    body = '\n'.join(parts)
    count = body.count('<section class="slide')
    head = (f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8" />\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
            f'<title>{cfg["title"]} | 2027 Agent Retreat</title>\n\n<!-- Presentation Hub Metadata -->\n'
            f'<meta name="presentation-title" content="{cfg["title"]}">\n'
            f'<meta name="presentation-series" content="2027 Agent Retreat">\n'
            f'<meta name="presentation-session" content="{cfg["session"]}">\n'
            f'<meta name="presentation-date" content="{cfg["date"]}">\n'
            f'<meta name="presentation-slides" content="{count}">\n\n'
            f'{FONTS_HEAD}\n{CITY_HEAD}\n<style>{STYLE}{EXTRA_CSS}</style>\n</head>\n')
    tail = [RUNTIME, RCLIPS if 'data-clip="R04"' in body else '', SNOW if day == 'D1' else '']
    out = (head + '<body>\n<div id="blank" aria-hidden="true"></div>\n<div class="city-toast" aria-live="polite"></div>\n\n'
           + body + '\n' + '\n'.join(t for t in tail if t) + '\n</body>\n</html>\n')
    open(os.path.join(PRES, cfg['file']), 'w', encoding='utf-8').write(out)
    return cfg['file'], count


if __name__ == '__main__':
    for d in DAYS:
        f, n = build(d)
        print(f'{f}: {n} slides')
