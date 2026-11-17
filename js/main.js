(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Mobile menu
  var btn = $('.menu-btn'), nav = $('#nav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // Videos: no autoplay for reduced motion
  if (calm) $$('video').forEach(function (v) { v.removeAttribute('autoplay'); v.pause(); v.setAttribute('controls', ''); });

  // Tabs (audience switch, services journey)
  $$('[role=tablist]').forEach(function (list) {
    var tabs = $$('[role=tab]', list);
    function pick(t, focus) {
      tabs.forEach(function (x) {
        var on = x === t;
        x.setAttribute('aria-selected', on ? 'true' : 'false'); x.tabIndex = on ? 0 : -1;
        var p = document.getElementById(x.getAttribute('aria-controls')); if (p) p.hidden = !on;
      });
      if (focus) t.focus();
    }
    tabs.forEach(function (t, i) {
      t.tabIndex = t.getAttribute('aria-selected') === 'true' ? 0 : -1;
      t.addEventListener('click', function () { pick(t); });
      t.addEventListener('keydown', function (ev) {
        if (ev.key === 'ArrowRight') pick(tabs[(i + 1) % tabs.length], true);
        if (ev.key === 'ArrowLeft') pick(tabs[(i - 1 + tabs.length) % tabs.length], true);
      });
    });
  });

  // Hero brand showcase
  var show = $('.showcase');
  if (show) {
    var slides = $$('.slide', show), dots = $$('.dot', show), cur = 0, timer = null;
    var go = function (n) {
      cur = (n + slides.length) % slides.length;
      slides.forEach(function (s, i) { s.classList.toggle('on', i === cur); s.tabIndex = i === cur ? 0 : -1; });
      dots.forEach(function (d, i) { d.classList.toggle('on', i === cur); });
    };
    var play = function () { if (!calm && !timer) timer = setInterval(function () { go(cur + 1); }, 4000); };
    var stop = function () { clearInterval(timer); timer = null; };
    dots.forEach(function (d, i) { d.addEventListener('click', function () { go(i); }); });
    $$('.arrow', show).forEach(function (a) { a.addEventListener('click', function () { go(cur + Number(a.dataset.dir)); }); });
    show.addEventListener('mouseenter', stop); show.addEventListener('mouseleave', play);
    show.addEventListener('focusin', stop); show.addEventListener('focusout', play);
    go(0); play();
  }

  // Count-up numbers
  var nums = $$('[data-count]');
  if (nums.length && !calm && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, end = Number(el.dataset.count), suf = el.dataset.suffix || '', t0 = null;
        io.unobserve(el);
        var tick = function (t) {
          if (!t0) t0 = t;
          var p = Math.min((t - t0) / 900, 1), v = Math.round(end * (1 - Math.pow(1 - p, 3)));
          el.textContent = v.toLocaleString('en-NZ') + suf;
          if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      });
    }, { threshold: 0.6 });
    nums.forEach(function (n) { io.observe(n); });
  }

  // Brand catalogue: search, filter, detail dialog
  var grid = $('#brand-grid');
  if (grid) {
    var data = JSON.parse($('#brand-data').textContent), cards = $$('.brand', grid), pills = $$('.pill'), q = $('#q');
    var count = $('#count'), empty = $('#empty'), dlg = $('#brand-dialog'), cat = 'all', openSlug = null;
    var apply = function () {
      var term = q.value.trim().toLowerCase(), n = 0;
      cards.forEach(function (c) {
        var ok = (cat === 'all' || c.dataset.cat === cat) && (!term || c.dataset.q.indexOf(term) > -1);
        c.hidden = !ok; if (ok) n++;
      });
      pills.forEach(function (p) { p.setAttribute('aria-pressed', p.dataset.cat === cat ? 'true' : 'false'); });
      count.textContent = n + (n === 1 ? ' brand' : ' brands');
      empty.hidden = n > 0;
    };
    var openBrand = function (slug) {
      var b = data[slug]; if (!b) return;
      openSlug = slug;
      dlg.className = 'c-' + b.cat;
      $('#bd-hero').src = b.hero; $('#bd-hero').alt = b.name + ' products';
      $('#bd-logo').src = b.logo; $('#bd-logo').alt = b.name + ' logo';
      $('#bd-name').textContent = b.name; $('#bd-type').textContent = b.type; $('#bd-fact').textContent = b.fact;
      $('#bd-about').textContent = b.about;
      var g = $('#bd-gallery'); g.textContent = '';
      b.gallery.forEach(function (src, i) { var im = new Image(); im.src = src; im.alt = b.name + ' product image ' + (i + 1); im.loading = 'lazy'; g.appendChild(im); });
      $('#bd-enquire').href = 'partner.html?brand=' + encodeURIComponent(b.name);
      if (!dlg.open) dlg.showModal();
      dlg.scrollTop = 0;
      history.replaceState(null, '', '#' + slug);
    };
    pills.forEach(function (p) { p.addEventListener('click', function () { cat = p.dataset.cat; apply(); }); });
    q.addEventListener('input', apply);
    $('#reset').addEventListener('click', function () { cat = 'all'; q.value = ''; apply(); q.focus(); });
    cards.forEach(function (c) { c.addEventListener('click', function () { openBrand(c.dataset.slug); }); });
    $('.bd-close').addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('click', function (ev) { if (ev.target === dlg) dlg.close(); });
    dlg.addEventListener('close', function () { history.replaceState(null, '', location.pathname + location.search); });
    $('#bd-next').addEventListener('click', function () {
      var vis = cards.filter(function (c) { return !c.hidden; }).map(function (c) { return c.dataset.slug; });
      if (!vis.length) vis = Object.keys(data);
      openBrand(vis[(vis.indexOf(openSlug) + 1) % vis.length]);
    });
    var route = function () {
      var h = location.hash.slice(1);
      if (data[h]) openBrand(h); else if (pills.some(function (p) { return p.dataset.cat === h; })) { cat = h; apply(); }
    };
    window.addEventListener('hashchange', route);
    route();
  }

  // Partner form
  var form = $('#partner-form');
  if (form) {
    var qs = new URLSearchParams(location.search), msg = $('#form-msg'), chips = $$('.chip', form);
    if (qs.get('interest') === 'sell') $$('[name=interest]', form)[1].checked = true;
    chips.forEach(function (c) {
      if (qs.get('brand') === c.dataset.brand) c.setAttribute('aria-pressed', 'true');
      c.addEventListener('click', function () { c.setAttribute('aria-pressed', c.getAttribute('aria-pressed') === 'true' ? 'false' : 'true'); });
    });
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var bad = null;
      $$('[required]', form).forEach(function (f) {
        var ok = f.value.trim() !== '' && (f.type !== 'email' || /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value.trim()));
        f.classList.toggle('bad', !ok); f.setAttribute('aria-invalid', ok ? 'false' : 'true');
        if (!ok && !bad) bad = f;
      });
      if (bad) { msg.className = 'form-msg err'; msg.textContent = 'Please complete the highlighted fields.'; bad.focus(); return; }
      var v = function (n) { return form[n].value.trim(); };
      var picked = chips.filter(function (c) { return c.getAttribute('aria-pressed') === 'true'; }).map(function (c) { return c.dataset.brand; });
      var body = ['Interested in: ' + form.interest.value, 'Name: ' + v('first') + ' ' + v('last'), 'Company: ' + v('company'), 'Email: ' + v('email'),
        'Address: ' + v('address'), 'Business type: ' + v('btype'), 'Interested brands: ' + (picked.join(', ') || '-'), 'Notes: ' + (v('brands') || '-')].join('\n');
      // No server yet: hand the enquiry to the visitor's email app. Replace with a form endpoint before launch.
      location.href = 'mailto:sales@anzpharma.co.nz?subject=' + encodeURIComponent('Partnership enquiry: ' + v('company')) + '&body=' + encodeURIComponent(body);
      msg.className = 'form-msg ok'; msg.textContent = 'Your email app should now open with your enquiry ready to send.';
    });
  }
})();
