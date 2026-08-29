/* v3 shared UI: theme + nav injection + page marker
   Subpages include <script src="/assets/site.js" defer></script> and
   leave <header class="top"></header> empty for auto-injection. */
(function () {
  function toggleTheme() {
    var cur = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', cur);
    localStorage.setItem('ap_theme', cur);
    var m = document.querySelector('meta[name="theme-color"]');
    if (m) m.setAttribute('content', cur === 'light' ? '#F4F0E8' : '#0C0C0D');
  }

  function getPage() {
    var p = location.pathname;
    if (p === '/' || p === '/index.html' || /\/$/.test(p) && p.split('/').length === 2) return '/';
    var seg = p.split('/').filter(Boolean)[0];
    return '/' + seg + '/';
  }

  function injectNav() {
    var head = document.querySelector('header.top');
    if (!head || head.dataset.injected) return;
    head.dataset.injected = '1';
    var current = head.getAttribute('data-page') || getPage();
    var items = [
      { href: '/',           label: 'Index' },
      { href: '/projects/',  label: 'Projects' },
      { href: '/robotics/',  label: 'Robotics' },
      { href: '/now/',       label: 'Now' },
      { href: '/homelab/',   label: 'Homelab' },
      { href: '/about/',     label: 'About' }
    ];
    var nav = document.createElement('nav');
    items.forEach(function (it) {
      var a = document.createElement('a');
      a.href = it.href;
      a.textContent = it.label;
      if (it.href === current) a.setAttribute('aria-current', 'page');
      nav.appendChild(a);
    });
    var logo = document.createElement('a');
    logo.className = 'logo';
    logo.href = '/';
    logo.textContent = 'Anton Petnitsky';
    head.appendChild(logo);
    head.appendChild(nav);
    var btn = document.createElement('button');
    btn.className = 'theme-toggle';
    btn.setAttribute('aria-label', 'Toggle theme');
    btn.onclick = toggleTheme;
    head.appendChild(btn);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectNav);
  } else {
    injectNav();
  }

  window.toggleTheme = toggleTheme;
})();
