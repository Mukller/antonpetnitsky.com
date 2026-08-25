/* shared UI: language + theme toggles (subpages) */
function toggleLang() {
  var l = document.documentElement.lang === 'ru' ? 'en' : 'ru';
  document.querySelectorAll('[data-' + l + ']').forEach(function (el) {
    var val = el.getAttribute('data-' + l);
    if (val) el.innerHTML = val;
  });
  document.documentElement.lang = l;
  var b = document.getElementById('langBtn');
  if (b) b.textContent = l === 'ru' ? 'EN' : 'RU';
  localStorage.setItem('ap_lang', l);
}

function applyTheme(t) {
  document.documentElement.setAttribute('data-theme', t);
  localStorage.setItem('ap_theme', t);
  var m = document.querySelector('meta[name="theme-color"]');
  if (m) m.setAttribute('content', t === 'light' ? '#edf0f3' : '#0d1117');
}

function toggleTheme() {
  applyTheme(document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light');
}

(function () {
  var b = document.getElementById('langBtn');
  if (b && document.documentElement.lang === 'ru') b.textContent = 'EN';
})();
