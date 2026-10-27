"""Build reThought deck clips.
usage: python3 clipbuild.py <frontend-slides root> <out js path>
Reads motion/clips/*.html fragments. Writes:
  motion/dist/<name>.html  standalone preview (loops; ?render for stills)
  <out js path>            <script> block for the deck: engine once + every clip + the slide player
"""
import json, re, sys, pathlib
ROOT = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2])
E = ROOT/'.claude/skills/motion-broll/engine'
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Instrument+Sans:wght@400;500;600;700&family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">'
BRAND = (open(pathlib.Path(__file__).parent/'brand.css').read())
CURSOR = '<svg id="cursor" viewBox="0 0 40 56"><path d="M3 3 L3 41 L12.5 32 L19 47 L25.5 44.2 L19.2 29.8 L32 29.8 Z" fill="#0B0B0B" stroke="#fff" stroke-width="2.6" stroke-linejoin="round"/></svg>'
base = ''.join(l for l in open(E/'base.css').read().splitlines(True) if '@font-face' not in l)
engine = open(E/'motion.js').read()
assert "const RENDER=location.search.includes('render');" in engine
engine = engine.replace("const RENDER=location.search.includes('render');", "const RENDER=location.search.includes('render')||window.EMBED===true;")
# icons the deck clips add to the engine set (Lucide, ISC licence)
engine += """
M.IC.lock=['M5 11h14a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2Z','M7 11V7a5 5 0 0 1 10 0v4'];
M.IC.alert=['m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3','M12 9v4','M12 17h.01'];
"""
# embed mode: no preview loop; fit the stage to the iframe instead
FIT = ("(function(){if(!window.EMBED)return;var st=document.getElementById('stage'),wr=document.getElementById('wrap');"
       "var W=parseFloat(st.style.width),H=parseFloat(st.style.height);document.body.classList.add('embed');"
       "var fit=function(){var k=Math.min(innerWidth/W,innerHeight/H);wr.style.transform='translate(-50%,-50%) scale('+k+')';};"
       "fit();addEventListener('resize',fit);"
       # the cursor arrives with the shape, so a slide never shows a lone cursor before the clip starts
       "var cu=document.getElementById('cursor'),s0=window.seek;window.seek=function(t){s0(t);cu.style.opacity=Math.min(1,Math.max(0,(t-0.15)/0.25));};})();")
EMBED_CSS = 'body.embed #wrap{position:absolute;left:50%;top:50%}'
def parts(src):
    frag = open(src, encoding='utf-8').read()
    m = re.search(r'<title>(.*?)</title>', frag)
    slot = lambda n: (re.search(rf'<div data-slot="{n}">(.*?)</div><!--/{n}-->', frag, re.S) or [None, ''])[1]
    return dict(title=m.group(1) if m else src.stem, css=''.join(re.findall(r'<style>(.*?)</style>', frag, re.S)),
                world=slot('world'), shape=slot('shape'), over=slot('over'), js=''.join(re.findall(r'<script>(.*?)</script>', frag, re.S)))
def page(p, embed):
    return ('<!doctype html><html><head><meta charset="utf-8"><title>' + p['title'] + '</title>' + FONTS +
            '<style>' + base + BRAND + EMBED_CSS + p['css'] + '</style>' + ('<script>window.EMBED=true</script>' if embed else '') + '</head><body>'
            '<div id="wrap"><div id="stage"><div id="world">' + p['world'] + '<div id="shape">' + p['shape'] + '</div>' + p['over'] + '</div>' + CURSOR + '</div></div>'
            '<script>' + ENGINE_TOKEN + '</script><script>' + p['js'] + '</script><script>' + FIT + '</script></body></html>')
ENGINE_TOKEN = '%%ENGINE%%'
dist = ROOT/'motion/dist'; dist.mkdir(parents=True, exist_ok=True)
clips = {}
for src in sorted((ROOT/'motion/clips').glob('*.html')):
    p = parts(src)
    (dist/src.name).write_text(page(p, False).replace(ENGINE_TOKEN, engine), encoding='utf-8')
    clips[src.stem.split('-')[0]] = page(p, True)
    print('built', dist/src.name)
player = open(pathlib.Path(__file__).parent/'player.js').read()
js = 'window.__CLIP_ENGINE=' + json.dumps(engine) + ';\nwindow.__CLIPS=' + json.dumps(clips) + ';\n' + player
js = js.replace('</', '<\\/')
OUT.write_text('<script>\n/* Motion clips (motion-broll engine). Sources: motion/clips/*.html, built by clipbuild.py */\n' + js + '\n</script>\n', encoding='utf-8')
print('wrote', OUT, len(js), 'bytes')
