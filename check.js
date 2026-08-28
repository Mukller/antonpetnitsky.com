const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
const checks = {
  bytes: html.length,
  opens: (html.match(/<script/g) || []).length,
  closes: (html.match(/<\/script>/g) || []).length,
  title: /<\/title>/.test(html),
  hasHero: html.includes('class="hero"'),
  hasProjects: html.includes('class="projects"'),
  hasContact: html.includes('class="contacts"'),
  hasRobotics: html.includes('class="robotics"'),
  hasFooter: html.includes('<footer'),
  hasSkipLink: html.includes('skip-link'),
};
const failed = Object.entries(checks).filter(([k, v]) => !v).map(([k]) => k);
if (failed.length) {
  console.log('FAIL:', failed.join(', '));
  process.exit(1);
} else {
  console.log('OK:', JSON.stringify(checks));
}
