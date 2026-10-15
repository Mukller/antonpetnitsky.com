const fs = require('fs');
const path = require('path');

const checks = [
  // Sections are addressed by id, not by class, and the /now/ strip was removed
  // on purpose (see AGENTS.md), so only ids that really exist are asserted here.
  { file: 'index.html',  must: ['class="hero"', '<section id="about">', '<section id="skills"', '<section id="projects">', '<section id="reviews">', '<section id="contact">', 'skip-link', '<footer', '</title>'] },
  { file: 'projects/index.html', must: ['class="sub-hero"', 'breadcrumb', '<ol', 'fira-autonomous-rc-car'] },
  { file: 'robotics/index.html', must: ['class="sub-hero"', 'Balance_robot', 'fira-autonomous-rc-car'] },
  { file: 'about/index.html',     must: ['class="sub-hero"', 'Timeline', 'Education', 'How I work'] },
  { file: 'homelab/index.html',   must: ['class="sub-hero"', 'Hardware', 'Watchdog'] },
  { file: 'print3d/index.html',   must: ['class="sub-hero"', 'Klipper', 'Ender 5 S1'] },
  { file: 'assets/css/style.css', must: ['--bg: #0C0C0D', '--accent: #B8924A', 'v3'] },
  { file: 'assets/site.js',       must: ['toggleTheme', 'injectNav', 'aria-current'] },
];

let failed = 0;
for (const c of checks) {
  const p = path.join(__dirname, c.file);
  if (!fs.existsSync(p)) { console.log('FAIL missing:', c.file); failed++; continue; }
  const html = fs.readFileSync(p, 'utf8');
  const missing = c.must.filter(s => !html.includes(s));
  if (missing.length) {
    console.log('FAIL', c.file + ':', missing.join(', '));
    failed++;
  } else {
    console.log('OK  ', c.file);
  }
}
if (failed) { console.log(failed, 'failures'); process.exit(1); }
console.log('all checks passed');
