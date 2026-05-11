#!/usr/bin/env python3
"""One-shot fix: colors, nav dropdowns, footer programs, images, quick-tour hero."""
import os, re

DIR = os.path.dirname(os.path.abspath(__file__))

def read(f):
    with open(os.path.join(DIR, f)) as fh:
        return fh.read()

def write(f, s):
    with open(os.path.join(DIR, f), 'w') as fh:
        fh.write(s)

# ── 4-program nav dropdown block (used in replacements below)
NAV_2 = '<a href="program-1.html">[PROGRAM 1 NAME]</a>\n            <a href="program-2.html">[PROGRAM 2 NAME]</a>'
NAV_4 = '<a href="program-1.html">[PROGRAM 1 NAME]</a>\n            <a href="program-2.html">[PROGRAM 2 NAME]</a>\n            <a href="program-3.html">Dragons</a>\n            <a href="program-4.html">Little Dragons</a>'

# ── 4-program footer list (for files that have only 2)
FOOTER_2 = '        <li><a href="program-1.html">[PROGRAM 1 NAME]</a></li>\n        <li><a href="program-2.html">[PROGRAM 2 NAME]</a></li>'
FOOTER_4 = '        <li><a href="program-1.html">[PROGRAM 1 NAME]</a></li>\n        <li><a href="program-2.html">[PROGRAM 2 NAME]</a></li>\n        <li><a href="program-3.html">Dragons</a></li>\n        <li><a href="program-4.html">Little Dragons</a></li>'

def fix_colors_index(s):
    s = s.replace('--red:         #cc0000;', '--red:         #c2261f;')
    s = s.replace('--red-dark:    #a80000;', '--red-dark:    #9e1f18;')
    s = s.replace('--blue:        #0066cc;', '--blue:        #ffc700;')
    s = s.replace('--blue-dark:   #0052a3;', '--blue-dark:   #cc9f00;')
    s = s.replace('--blue-light:  #e8f0fb;', '--blue-light:  #fff8e1;')
    s = s.replace('--gold:        #d4a017;', '--gold:        #ffc700;')
    return s

def fix_colors_program(s):
    # Update :root CSS vars
    s = s.replace('--blue:#2563eb;--blue-dark:#1d4ed8;--blue-light:#eff6ff;',
                  '--red:#c2261f;--red-dark:#9e1f18;--blue:#ffc700;--blue-dark:#cc9f00;--blue-light:#fff8e1;')
    s = s.replace('--gold:#d4a017;', '--gold:#ffc700;')
    # Make btn-primary use --red instead of --blue
    s = s.replace('background:var(--blue);color:var(--white);border:2px solid var(--blue)}',
                  'background:var(--red);color:var(--white);border:2px solid var(--red)}')
    s = s.replace('background:var(--blue-dark);border-color:var(--blue-dark);transform:translateY(-2px)',
                  'background:var(--red-dark);border-color:var(--red-dark);transform:translateY(-2px)')
    return s

# ── index.html ────────────────────────────────────────────────────────────────
s = read('index.html')
s = fix_colors_index(s)
# Nav dropdown: add Dragons + Little Dragons
s = s.replace(
    '            <a href="program-1.html">[PROGRAM 1 NAME]</a>\n'
    '            <a href="program-2.html">[PROGRAM 2 NAME]</a>\n'
    '          </div>\n'
    '        </div>\n'
    '\n'
    '        <a href="quick-tour.html">',
    '            <a href="program-1.html">[PROGRAM 1 NAME]</a>\n'
    '            <a href="program-2.html">[PROGRAM 2 NAME]</a>\n'
    '            <a href="program-3.html">Dragons</a>\n'
    '            <a href="program-4.html">Little Dragons</a>\n'
    '          </div>\n'
    '        </div>\n'
    '\n'
    '        <a href="quick-tour.html">'
)
# Footer: add Dragons + Little Dragons
s = s.replace(
    '        <li><a href="program-1.html">[PROGRAM 1 NAME]</a></li>\n'
    '        <li><a href="program-2.html">[PROGRAM 2 NAME]</a></li>\n'
    '      </ul>\n'
    '    </div>\n'
    '\n'
    '    <!-- Useful Resources',
    '        <li><a href="program-1.html">[PROGRAM 1 NAME]</a></li>\n'
    '        <li><a href="program-2.html">[PROGRAM 2 NAME]</a></li>\n'
    '        <li><a href="program-3.html">Dragons</a></li>\n'
    '        <li><a href="program-4.html">Little Dragons</a></li>\n'
    '      </ul>\n'
    '    </div>\n'
    '\n'
    '    <!-- Useful Resources'
)
# Program images
s = s.replace('src="images/instructor-action.png" alt="Dragons program at',
              'src="images/karate.png" alt="Dragons program at')
s = s.replace('src="images/class-group.png" alt="Little Dragons program at',
              'src="images/hero-image.png" alt="Little Dragons program at')
write('index.html', s)
print('index.html done')

# ── program-1.html ────────────────────────────────────────────────────────────
s = read('program-1.html')
s = fix_colors_program(s)
s = s.replace(
    '            <a href="program-1.html">[PROGRAM 1 NAME]</a>\n'
    '            <a href="program-2.html">[PROGRAM 2 NAME]</a>\n'
    '          </div>',
    '            <a href="program-1.html">[PROGRAM 1 NAME]</a>\n'
    '            <a href="program-2.html">[PROGRAM 2 NAME]</a>\n'
    '            <a href="program-3.html">Dragons</a>\n'
    '            <a href="program-4.html">Little Dragons</a>\n'
    '          </div>'
)
s = s.replace(
    '        <li><a href="program-1.html">[PROGRAM 1 NAME]</a></li>\n'
    '        <li><a href="program-2.html">[PROGRAM 2 NAME]</a></li>\n'
    '      </ul>',
    '        <li><a href="program-1.html">[PROGRAM 1 NAME]</a></li>\n'
    '        <li><a href="program-2.html">[PROGRAM 2 NAME]</a></li>\n'
    '        <li><a href="program-3.html">Dragons</a></li>\n'
    '        <li><a href="program-4.html">Little Dragons</a></li>\n'
    '      </ul>'
)
write('program-1.html', s)
print('program-1.html done')

# ── program-2.html ────────────────────────────────────────────────────────────
s = read('program-2.html')
s = fix_colors_program(s)
s = s.replace(
    '            <a href="program-1.html">[PROGRAM 1 NAME]</a>\n'
    '            <a href="program-2.html">[PROGRAM 2 NAME]</a>\n'
    '          </div>',
    '            <a href="program-1.html">[PROGRAM 1 NAME]</a>\n'
    '            <a href="program-2.html">[PROGRAM 2 NAME]</a>\n'
    '            <a href="program-3.html">Dragons</a>\n'
    '            <a href="program-4.html">Little Dragons</a>\n'
    '          </div>'
)
s = s.replace(
    '        <li><a href="program-1.html">[PROGRAM 1 NAME]</a></li>\n'
    '        <li><a href="program-2.html">[PROGRAM 2 NAME]</a></li>',
    '        <li><a href="program-1.html">[PROGRAM 1 NAME]</a></li>\n'
    '        <li><a href="program-2.html">[PROGRAM 2 NAME]</a></li>\n'
    '        <li><a href="program-3.html">Dragons</a></li>\n'
    '        <li><a href="program-4.html">Little Dragons</a></li>'
)
write('program-2.html', s)
print('program-2.html done')

# ── program-template.html ─────────────────────────────────────────────────────
s = read('program-template.html')
s = fix_colors_program(s)
write('program-template.html', s)
print('program-template.html done')

# ── programs.html ─────────────────────────────────────────────────────────────
s = read('programs.html')
s = fix_colors_program(s)
# Fix empty footer program-3/4 links
s = s.replace('<li><a href="programs.html#program-3"></a></li>',
              '<li><a href="program-3.html">Dragons</a></li>')
s = s.replace('<li><a href="programs.html#program-4"></a></li>',
              '<li><a href="program-4.html">Little Dragons</a></li>')
write('programs.html', s)
print('programs.html done')

# ── quick-tour.html ───────────────────────────────────────────────────────────
s = read('quick-tour.html')
s = fix_colors_program(s)
# Hero image
s = s.replace('src="images/facility-exterior.webp"', 'src="images/all-ages-class.jpg"')
# Footer empty program links
s = s.replace('<li><a href="program-3.html"></a></li>',
              '<li><a href="program-3.html">Dragons</a></li>')
s = s.replace('<li><a href="program-4.html"></a></li>',
              '<li><a href="program-4.html">Little Dragons</a></li>')
write('quick-tour.html', s)
print('quick-tour.html done')

# ── reviews.html ──────────────────────────────────────────────────────────────
s = read('reviews.html')
s = fix_colors_program(s)
s = s.replace('<li><a href="program-3.html"></a></li>',
              '<li><a href="program-3.html">Dragons</a></li>')
s = s.replace('<li><a href="program-4.html"></a></li>',
              '<li><a href="program-4.html">Little Dragons</a></li>')
write('reviews.html', s)
print('reviews.html done')

# ── schedules.html ────────────────────────────────────────────────────────────
s = read('schedules.html')
s = fix_colors_program(s)
s = s.replace('<li><a href="program-3.html"></a></li>',
              '<li><a href="program-3.html">Dragons</a></li>')
s = s.replace('<li><a href="program-4.html"></a></li>',
              '<li><a href="program-4.html">Little Dragons</a></li>')
write('schedules.html', s)
print('schedules.html done')

# ── news.html ─────────────────────────────────────────────────────────────────
s = read('news.html')
s = fix_colors_program(s)
s = s.replace('<li><a href="program-3.html"></a></li>',
              '<li><a href="program-3.html">Dragons</a></li>')
s = s.replace('<li><a href="program-4.html"></a></li>',
              '<li><a href="program-4.html">Little Dragons</a></li>')
write('news.html', s)
print('news.html done')

print('\nAll done!')
