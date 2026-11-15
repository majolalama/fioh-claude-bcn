"""Fioh logo generator. Usage: python3 generate.py <output-folder>
Edit the palette or the pixel grids below and re-run to regenerate every file."""
import os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.makedirs(OUT, exist_ok=True)

# Fio-fio (white-crested elaenia) palette, taken from the reference photo
PAL = {
    'K': '#0b0f0d',  # outline
    'O': '#8f8f52',  # olive-green head/back
    'D': '#6f7040',  # olive shade
    'B': '#55523c',  # dark wing / tail
    'W': '#ece8b4',  # pale wing bars
    'G': '#d2d2bc',  # pale grey throat
    'Y': '#d6cf7c',  # yellowish belly
    'R': '#efecd2',  # eye ring
    'E': '#14181a',  # eye
    'e': '#ffffff',  # eye glint
    'C': '#e9a27c',  # cheek blush
    'P': '#f08a3c',  # beak / feet (ties to slogan orange)
}
ORANGE = '#f08a3c'
ORANGE_DARK = '#c96a1e'
DARK = '#1e2a26'
CREAM = '#f4ecc0'
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, 'DejaVu Sans Mono', monospace"
SLOGAN = 'from Zero to AI-FSD in a single command'

BIRD = """
..................KK
.................KOOKKK
................KOOOOOOK
...............KOOOOOOOOK
...............KOOOORRRROK
...............KOOOOReEROKKK
...............KOOOOREEROPPPK
..............KDOOOORRRRGKKK
.............KDDOOOOCCGGGK
...........KKBBBDOOOGGGGGK
.........KKBBWWBBDOOGGGGYK
.......KKBBBBBBWWBBOGGYYYK
.....KKBBBWWBBBBBWBBYYYYYK
...KKBBBBBBBWWBBBBBYYYYYYK
.KKBBBBBBBBBBBBBBBYYYYYYK
KBBBBBBKKKKKBBBBYYYYYYYK
KBBBKKK.....KKKYYYYYYKK
.KKK...........KKPKPKK
................KPKPK
...............KPPKPPK
...............KKKKKKK
""".strip('\n').split('\n')

LETTERS = {
    'F': ["XXXXX", "X....", "X....", "XXXX.", "X....", "X....", "X...."],
    'I': ["XXXXX", "..X..", "..X..", "..X..", "..X..", "..X..", "XXXXX"],
    'O': [".XXX.", "X...X", "X...X", "X...X", "X...X", "X...X", ".XXX."],
    'H': ["X...X", "X...X", "X...X", "XXXXX", "X...X", "X...X", "X...X"],
}


def grid(rows, x, y, px, pal=None, fill=None, skip=''):
    """Pixel grid -> merged horizontal run rects."""
    out = []
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            ch = row[c]
            if ch == '.' or ch in skip:
                c += 1
                continue
            n = 1
            while c + n < len(row) and row[c + n] == ch:
                n += 1
            col = fill or pal[ch]
            out.append(f'<rect x="{x + c * px}" y="{y + r * px}" width="{n * px}" height="{px}" fill="{col}"/>')
            c += n
    return '\n'.join(out)


def word(x, y, px, fill, shadow=None, gap=1):
    out = []
    for i, ch in enumerate('FIOH'):
        lx = x + i * (5 + gap) * px
        if shadow:
            out.append(grid(LETTERS[ch], lx + px * 0.5, y + px * 0.5, px, fill=shadow))
        out.append(grid(LETTERS[ch], lx, y, px, fill=fill))
    return '\n'.join(out)


def svg(name, w, h, body):
    with open(os.path.join(OUT, name), 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
                f'shape-rendering="crispEdges" role="img" aria-label="Fioh">\n{body}\n</svg>\n')


def text(x, y, size, fill, anchor='start'):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{MONO}" font-size="{size}" '
            f'font-weight="600" fill="{fill}" shape-rendering="geometricPrecision">{SLOGAN} &#9608;</text>')


bw = max(len(r) for r in BIRD)

# ---------- Badge 1: dark circle ----------
px = 11
dots = ''.join(
    f'<rect x="{x}" y="{y}" width="14" height="14" fill="#ffffff" opacity="{o}"/>'
    for x, y, o in [(120, 250, .05), (134, 264, .08), (106, 292, .05), (548, 236, .06), (562, 250, .04),
                    (534, 278, .07), (566, 330, .05), (136, 428, .07), (540, 420, .06),
                    (554, 448, .04), (500, 190, .05)])
svg('fioh-badge.svg', 700, 700, f'''<circle cx="350" cy="350" r="338" fill="#ffffff"/>
<circle cx="350" cy="350" r="316" fill="{DARK}"/>
<circle cx="350" cy="350" r="316" fill="none" stroke="{PAL['O']}" stroke-width="6" shape-rendering="geometricPrecision"/>
{dots}
{word(350 - (23 * 15) / 2, 108, 15, CREAM, shadow=PAL['D'])}
{grid(BIRD, 350 - bw * px / 2, 270, px, PAL)}
<path id="arc" d="M 78,350 A 272,272 0 0 0 622,350" fill="none"/>
<text font-family="{MONO}" font-size="25" font-weight="600" fill="{ORANGE}" letter-spacing="1" shape-rendering="geometricPrecision">
<textPath href="#arc" startOffset="50%" text-anchor="middle">{SLOGAN} &#9608;</textPath></text>''')

# ---------- Badge 2: no circle, bird perched on the wordmark ----------
px = 13
wp = 22
wx = 350 - 23 * wp / 2          # wordmark left edge
wy = 372
ox = wx + 12 * wp               # left edge of the letter O
bx = ox + wp * 2.5 - 18 * px    # centre the feet (grid col ~18) on the O
svg('fioh-badge-perch.svg', 700, 700, f'''<rect x="8" y="8" width="684" height="684" rx="96" fill="{CREAM}" stroke="{PAL['O']}" stroke-width="8" shape-rendering="geometricPrecision"/>
{word(wx, wy, wp, DARK, shadow=PAL['O'])}
{grid(BIRD, bx, wy - len(BIRD) * px + px, px, PAL)}
{text(350, 608, 23, ORANGE_DARK, 'middle')}''')


# ---------- Simple lockup ----------
def lockup(fg, sub, bg=None):
    b = f'<rect width="790" height="220" fill="{bg}"/>' if bg else ''
    return f'''{b}
{grid(BIRD, 16, 26, 8, PAL)}
{word(270, 36, 14, fg)}
{text(270, 182, 19, sub)}'''


svg('fioh-simple-light.svg', 790, 220, lockup(DARK, ORANGE_DARK))
svg('fioh-simple-dark.svg', 790, 220, lockup(CREAM, ORANGE, bg=DARK))
svg('fioh-simple-white.svg', 790, 220, lockup('#ffffff', ORANGE))

# icon only (app icon / favicon / avatar)
svg('fioh-icon.svg', 240, 240,
    f'<rect width="240" height="240" rx="48" fill="{DARK}" shape-rendering="geometricPrecision"/>\n'
    + grid(BIRD, (240 - bw * 7) / 2, 46, 7, PAL))

# one-colour version; eye + wing bars are cut-outs
mono_rows = BIRD
svg('fioh-mono.svg', 790, 220,
    f'<g fill="currentColor" color="{DARK}">\n{grid(mono_rows, 16, 26, 8, fill="currentColor", skip="WRe")}\n'
    f'{word(270, 36, 14, "currentColor")}\n{text(270, 182, 19, "currentColor")}</g>')
