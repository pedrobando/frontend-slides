/* Slide player: each clip plays when its slide is on screen, holds its last frame, then replays.
   Only the clip loops; the slide's headline and text stay put. Headless export and reduced motion get the last frame. */
(function () {
    var ENGINE = window.__CLIP_ENGINE, CLIPS = window.__CLIPS;
    if (!ENGINE || !CLIPS) return;
    var STILL = navigator.webdriver === true || matchMedia('(prefers-reduced-motion: reduce)').matches;
    var LEAD = 0.6, HOLD = 5, FADE = 0.45;
    var players = [], running = false;
    document.documentElement.classList.add('clips');
    document.querySelectorAll('.clip-slot[data-clip]').forEach(function (slot) {
        var html = CLIPS[slot.dataset.clip];
        if (!html) return;
        var f = document.createElement('iframe');
        f.className = 'clip-frame';
        f.setAttribute('aria-hidden', 'true');
        f.tabIndex = -1;
        var p = { f: f, slide: slot.closest('.slide'), win: null, T: 0, t0: null, on: false };
        f.addEventListener('load', function () {
            p.win = f.contentWindow;
            p.T = p.win.DURATION || 0;
            p.win.seek(STILL ? p.T : 0);
            if (STILL) hideCursor(p);
            if (p.on) { p.t0 = performance.now() + LEAD * 1000; kick(); }
        });
        f.srcdoc = html.split('%%ENGINE%%').join(ENGINE);
        slot.appendChild(f);
        players.push(p);
    });
    // a still frame (PDF export, print, reduced motion) shows the end state without the cursor
    function hideCursor(p, on) { var c = p.win.document.getElementById('cursor'); if (c) c.style.visibility = on ? '' : 'hidden'; }
    window.addEventListener('beforeprint', function () {
        players.forEach(function (p) { if (p.win) { p.win.seek(p.T); hideCursor(p); p.f.style.opacity = ''; } });
    });
    window.addEventListener('afterprint', function () {
        players.forEach(function (p) { if (p.win && !STILL) hideCursor(p, true); });
    });
    if (STILL || !players.length) return;

    function kick() { if (!running) { running = true; requestAnimationFrame(tick); } }
    function tick(now) {
        var any = false;
        players.forEach(function (p) {
            if (!p.on || !p.win || p.t0 === null) return;
            any = true;
            var e = (now - p.t0) / 1000;
            if (e < 0) { p.win.seek(0); return; }
            var cyc = p.T + HOLD, c = e % cyc;
            p.win.seek(Math.min(c, p.T));
            var o = Math.min(1, (cyc - c) / FADE);
            p.f.style.opacity = o < 1 ? o.toFixed(3) : '';
        });
        if (any) requestAnimationFrame(tick); else running = false;
    }
    var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
            players.forEach(function (p) {
                if (p.slide !== e.target || p.on === e.isIntersecting) return;
                p.on = e.isIntersecting;
                p.f.style.opacity = '';
                if (p.on) { p.t0 = performance.now() + LEAD * 1000; }
                else { p.t0 = null; if (p.win) p.win.seek(0); }
            });
        });
        kick();
    }, { threshold: 0.6 });
    players.forEach(function (p) { io.observe(p.slide); });
})();
