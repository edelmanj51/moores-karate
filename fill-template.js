#!/usr/bin/env node
/**
 * fill-template.js
 * Reads client-data.json, auto-populates image slots from folder structure,
 * replaces all [TOKEN] placeholders in every .html file, writes to ./dist/.
 *
 * Image slot folders (drop any image file in — filename doesn't matter):
 *   images/hero/                    → HERO_IMAGE
 *   images/programs/kids-karate/    → PROGRAM 1 PHOTO
 *   images/programs/teens-adults/   → PROGRAM 2 PHOTO
 *   images/programs/dragons/        → PROGRAM 3 PHOTO
 *   images/programs/little-dragons/ → PROGRAM 4 PHOTO
 *   images/instructor/              → INSTRUCTOR 1 PHOTO
 *   images/quick-tour/              → QUICK_TOUR_GALLERY (all files → gallery cards)
 *
 * Usage:
 *   node fill-template.js
 *   node fill-template.js --check   (only report unfilled tokens, no output)
 */

const fs   = require('fs');
const path = require('path');

const CHECK_ONLY = process.argv.includes('--check');
const TOKEN_RE   = /\[([A-Z][A-Z 0-9_]*)\]/g;
const IMG_EXT    = /\.(png|jpg|jpeg|webp|gif|svg)$/i;

// ── Load client data ──────────────────────────────────────────────────────
if (!fs.existsSync('client-data.json')) {
  console.error('ERROR: client-data.json not found. Create it before running.');
  process.exit(1);
}
const data = JSON.parse(fs.readFileSync('client-data.json', 'utf8'));

// ── Auto-populate single-image slots ─────────────────────────────────────
const IMAGE_SLOTS = {
  'images/hero':                    'HERO_IMAGE',
  'images/programs/kids-karate':    'PROGRAM 1 PHOTO',
  'images/programs/teens-adults':   'PROGRAM 2 PHOTO',
  'images/programs/dragons':        'PROGRAM 3 PHOTO',
  'images/programs/little-dragons': 'PROGRAM 4 PHOTO',
  'images/instructor':              'INSTRUCTOR 1 PHOTO',
};

for (const [folder, token] of Object.entries(IMAGE_SLOTS)) {
  if (fs.existsSync(folder)) {
    const files = fs.readdirSync(folder).filter(f => IMG_EXT.test(f));
    if (files.length > 0) {
      data[token] = `${folder}/${files[0]}`;
    }
  }
}

// ── Auto-generate quick-tour gallery ─────────────────────────────────────
const QT_FOLDER = 'images/quick-tour';
if (fs.existsSync(QT_FOLDER)) {
  const files = fs.readdirSync(QT_FOLDER).filter(f => IMG_EXT.test(f)).sort();
  data['QUICK_TOUR_GALLERY'] = files.map(f => {
    const label = f.replace(IMG_EXT, '').replace(/-/g, ' ');
    return (
      `    <div class="gallery-item reveal">\n` +
      `      <div class="gallery-photo"><img src="${QT_FOLDER}/${f}" alt="${label}" style="width:100%;height:100%;object-fit:cover"></div>\n` +
      `    </div>`
    );
  }).join('\n');
}

// ── Collect HTML files ────────────────────────────────────────────────────
const htmlFiles = fs.readdirSync('.').filter(f => f.endsWith('.html')).sort();

// ── Copy images tree to dist (skip review/ staging folder) ────────────────
function copyDirSync(src, dst) {
  if (!fs.existsSync(dst)) fs.mkdirSync(dst, { recursive: true });
  for (const entry of fs.readdirSync(src)) {
    if (entry === 'review') continue;
    const s = path.join(src, entry);
    const d = path.join(dst, entry);
    if (fs.statSync(s).isDirectory()) copyDirSync(s, d);
    else fs.copyFileSync(s, d);
  }
}

if (!CHECK_ONLY) {
  if (!fs.existsSync('dist')) fs.mkdirSync('dist');
  if (fs.existsSync('images')) copyDirSync('images', path.join('dist', 'images'));
}

// ── Process each file ─────────────────────────────────────────────────────
const unfilled = new Set();

for (const file of htmlFiles) {
  let content = fs.readFileSync(file, 'utf8');

  for (const [key, value] of Object.entries(data)) {
    if (value === '' || value == null) continue;
    content = content.split(`[${key}]`).join(value);
  }

  TOKEN_RE.lastIndex = 0;
  let m;
  while ((m = TOKEN_RE.exec(content)) !== null) {
    unfilled.add(m[1]);
  }

  if (!CHECK_ONLY) {
    fs.writeFileSync(path.join('dist', file), content, 'utf8');
    console.log(`  ✓  ${file}`);
  }
}

// ── Report ────────────────────────────────────────────────────────────────
if (unfilled.size > 0) {
  console.log('\n⚠️  Unfilled tokens (' + unfilled.size + '):');
  for (const t of [...unfilled].sort()) {
    console.log(`     [${t}]`);
  }
  if (CHECK_ONLY) process.exit(1);
} else {
  console.log('\n✅  All tokens filled. Output in ./dist/');
}
