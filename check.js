const fs = require('fs');
const path = require('path');

const checks = [
  { file: 'index.html',  must: ['class="hero"', 'class="now-strip"', 'class="about"', 'class="skills"', 'class="projects"', 'class="contacts"', 'skip-link', '<footer', '</title>'] },
  { file: 'projects/index.html', must: ['class="sub-hero"', 'breadcrumb', '<ol', 'fira-autonomous-rc-car'] },
  { file: 'robotics/index.html', must: ['class="sub-hero"', 'Balance_robot', 'fira-autonomous-rc-car'] },
  { file: 'now/index.html',       must: ['class="sub-hero"', 'This week', 'This month'] },
  { file: 'about/index.html',     must: ['class="sub-hero"', 'Timeline', 'Education', 'How I work'] },
  { file: 'homelab/index.html',   must: ['class="sub-hero"', 'Hardware', 'Watchdog'] },
  { file: 'print3d/index.html',   must: ['class="sub-hero"', 'Klipper', 'Ender 5 S1'] },
  { file: 'minecraft/index.html', must: ['class="sub-hero"', 'Velocity', 'Survival'] },
  { file: 'uses/index.html',      must: ['class="sub-hero"', 'Hardware', 'Software'] },
  { file: 'safalife/index.html',  must: ['class="sub-hero"', 'OSRM', 'Flutter'] },
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
