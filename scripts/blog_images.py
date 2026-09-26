"""Generates the blog featured images as SVG (rendered to WebP/PNG by render-images.js)."""
import math, os
W, H = 1600, 900
INK = "#F2F1EE"; MUTE = "#3A3A38"; DIM = "#26262A"

def frame(inner, glow=(800, 470)):
    gx, gy = glow
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice">
<defs>
  <linearGradient id="pg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C9A3FF"/><stop offset=".45" stop-color="#9B5CFF"/><stop offset="1" stop-color="#6A2CF5"/></linearGradient>
  <linearGradient id="pgh" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1600" y2="0"><stop offset="0" stop-color="#C9A3FF"/><stop offset=".5" stop-color="#9B5CFF"/><stop offset="1" stop-color="#6A2CF5"/></linearGradient>
  <radialGradient id="glow" cx="{gx/W}" cy="{gy/H}" r=".55"><stop offset="0" stop-color="#9B5CFF" stop-opacity=".30"/><stop offset=".5" stop-color="#6A2CF5" stop-opacity=".08"/><stop offset="1" stop-color="#0A0A0A" stop-opacity="0"/></radialGradient>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>
  <filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .06 0"/></filter>
  <pattern id="grid" width="80" height="80" patternUnits="userSpaceOnUse"><path d="M80 0H0V80" fill="none" stroke="#FFFFFF" stroke-opacity=".035" stroke-width="1"/></pattern>
</defs>
<rect width="{W}" height="{H}" fill="#0A0A0A"/>
<rect width="{W}" height="{H}" fill="url(#grid)"/>
<rect width="{W}" height="{H}" fill="url(#glow)"/>
{inner}
<rect width="{W}" height="{H}" filter="url(#n)"/>
</svg>'''

def seo():
    # rising monthly line with a loop arrow
    x0, x1, yb = 300, 1300, 700
    pts = []
    vals = [0.06,0.10,0.09,0.17,0.22,0.21,0.31,0.38,0.36,0.49,0.58,0.72]
    for i, v in enumerate(vals):
        x = x0 + i*(x1-x0)/(len(vals)-1); y = yb - v*460; pts.append((x, y))
    d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
    area = d + f" L{x1} {yb} L{x0} {yb} Z"
    dots = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="#0A0A0A" stroke="url(#pg)" stroke-width="3"/>' for x, y in pts)
    ticks = "".join(f'<line x1="{x:.0f}" y1="{yb}" x2="{x:.0f}" y2="{yb+14}" stroke="{MUTE}" stroke-width="2"/>' for x, _ in pts)
    gl = "".join(f'<line x1="{x0}" y1="{yb-k*115}" x2="{x1}" y2="{yb-k*115}" stroke="{DIM}" stroke-width="1.5" stroke-dasharray="4 10"/>' for k in range(1,5))
    lx, ly = pts[-1]
    once = [0.06,0.14,0.22,0.25,0.24,0.22,0.20,0.19,0.17,0.16,0.15,0.14]
    op = [(x0 + i*(x1-x0)/(len(once)-1), yb - v*460) for i, v in enumerate(once)]
    od = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in op)
    loop = f'<path d="{od}" fill="none" stroke="#6E6E6A" stroke-width="3" stroke-dasharray="10 10" stroke-linecap="round"/><circle cx="{op[-1][0]:.0f}" cy="{op[-1][1]:.0f}" r="6" fill="#6E6E6A"/>'
    return frame(f'''
<g><path d="{area}" fill="url(#pg)" opacity=".10"/>{gl}
<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{MUTE}" stroke-width="2"/>{ticks}{loop}
<path d="{d}" fill="none" stroke="url(#pg)" stroke-width="14" opacity=".45" filter="url(#soft)"/>
<path d="{d}" fill="none" stroke="url(#pg)" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>{dots}
<circle cx="{lx:.0f}" cy="{ly:.0f}" r="16" fill="url(#pg)"/></g>''', glow=(1100, 380))

def call():
    cx, cy = 800, 450
    phone = f'''<g><rect x="{cx-170}" y="{cy-330}" width="340" height="660" rx="52" fill="#101012" stroke="{MUTE}" stroke-width="3"/>
    <rect x="{cx-40}" y="{cy-308}" width="80" height="10" rx="5" fill="{MUTE}"/>
    <rect x="{cx-130}" y="{cy-250}" width="200" height="16" rx="8" fill="{DIM}"/><rect x="{cx-130}" y="{cy-220}" width="140" height="16" rx="8" fill="{DIM}"/>
    <rect x="{cx-130}" y="{cy-160}" width="260" height="120" rx="14" fill="#16161A"/>
    <rect x="{cx-130}" y="{cy-20}" width="260" height="14" rx="7" fill="{DIM}"/><rect x="{cx-130}" y="{cy+8}" width="210" height="14" rx="7" fill="{DIM}"/>
    <rect x="{cx-130}" y="{cy+170}" width="260" height="84" rx="42" fill="url(#pg)"/>
    <g transform="translate({cx-78} {cy+212}) scale(1.35)" fill="#FFFFFF"><path d="M-9 -13c-2 0-4 2-4 4 0 12 10 22 22 22 2 0 4-2 4-4v-4c0-1-1-2-2-2l-5-1c-1 0-2 0-2 1l-2 2c-4-2-7-5-9-9l2-2c1-1 1-2 1-2l-1-5c0-1-1-2-2-2z"/></g>
    <rect x="{cx-40}" y="{cy+200}" width="130" height="14" rx="7" fill="#FFFFFF" opacity=".95"/><rect x="{cx-40}" y="{cy+224}" width="90" height="10" rx="5" fill="#FFFFFF" opacity=".6"/></g>'''
    tx, ty = cx+60, cy+212
    rip = "".join(f'<circle cx="{tx}" cy="{ty}" r="{r}" fill="none" stroke="url(#pg)" stroke-width="{w}" opacity="{o}"/>' for r, w, o in [(90,3,.8),(150,2.5,.5),(215,2,.3),(285,1.5,.16)])
    return frame(f'''<ellipse cx="{tx}" cy="{ty}" rx="160" ry="120" fill="#9B5CFF" opacity=".25" filter="url(#soft)"/>{phone}{rip}
''', glow=(tx, ty))

def speed():
    cx, cy, r = 800, 600, 380
    def pt(a, rr): return cx + rr*math.cos(math.radians(a)), cy - rr*math.sin(math.radians(a))
    ticks = ""
    for k in range(0, 41):
        a = 180 - k*4.5; big = k % 5 == 0
        x1, y1 = pt(a, r-10); x2, y2 = pt(a, r-(52 if big else 30))
        col = "url(#pg)" if k >= 30 else MUTE
        ticks += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{4 if big else 2}" stroke-linecap="round"/>'
    sx, sy = pt(180, r+30); ex, ey = pt(0, r+30)
    arc_bg = f'<path d="M{sx:.0f} {sy:.0f} A{r+30} {r+30} 0 0 1 {ex:.0f} {ey:.0f}" fill="none" stroke="{DIM}" stroke-width="10" stroke-linecap="round"/>'
    fx, fy = pt(45, r+30)
    arc_fg = f'<path d="M{fx:.0f} {fy:.0f} A{r+30} {r+30} 0 0 1 {ex:.0f} {ey:.0f}" fill="none" stroke="url(#pg)" stroke-width="10" stroke-linecap="round"/>'
    nx, ny = pt(28, r-80)
    needle = f'<line x1="{cx}" y1="{cy}" x2="{nx:.0f}" y2="{ny:.0f}" stroke="{INK}" stroke-width="8" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="26" fill="#0A0A0A" stroke="{INK}" stroke-width="6"/>'
    streaks = "".join(f'<line x1="{120+i*30}" y1="{250+i*70}" x2="{380+i*10}" y2="{250+i*70}" stroke="url(#pgh)" stroke-width="{3-i*0.4:.1f}" stroke-linecap="round" opacity="{.55-i*.1:.2f}"/>' for i in range(4))
    return frame(f'''{streaks}{arc_bg}<path d="M{fx:.0f} {fy:.0f} A{r+30} {r+30} 0 0 1 {ex:.0f} {ey:.0f}" fill="none" stroke="url(#pg)" stroke-width="30" opacity=".35" filter="url(#soft)"/>{arc_fg}{ticks}
    <line x1="{cx}" y1="{cy}" x2="{nx:.0f}" y2="{ny:.0f}" stroke="url(#pg)" stroke-width="22" opacity=".5" filter="url(#soft)"/>{needle}''', glow=(1050, 380))

def plan():
    # sitemap tree of wireframe cards
    def card(x, y, w, h, hl=False):
        s = "url(#pg)" if hl else MUTE
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#111114" stroke="{s}" stroke-width="{3 if hl else 2}"/>'
                f'<rect x="{x+18}" y="{y+18}" width="{w*0.5:.0f}" height="12" rx="6" fill="{"#C9A3FF" if hl else DIM}" opacity="{.9 if hl else 1}"/>'
                f'<rect x="{x+18}" y="{y+42}" width="{w-36}" height="{h*0.32:.0f}" rx="6" fill="{DIM}" opacity=".7"/>'
                f'<rect x="{x+18}" y="{y+h-34}" width="{w*0.38:.0f}" height="16" rx="8" fill="{"url(#pg)" if hl else DIM}"/>')
    top = (690, 110, 220, 150)
    mids = [(250, 390), (590, 390), (930, 390), (1270, 390)]
    lows = [(160, 650), (360, 650), (840, 650), (1040, 650)]
    lines = ""
    tx, ty = top[0]+top[2]/2, top[1]+top[3]
    for mx, my in mids:
        lines += f'<path d="M{tx} {ty} V {ty+55} H {mx+90} V {my}" fill="none" stroke="{MUTE}" stroke-width="2"/>'
    for (lx, ly), (mx, my) in zip(lows, [mids[0], mids[0], mids[2], mids[2]]):
        lines += f'<path d="M{mx+90} {my+130} V {my+175} H {lx+80} V {ly}" fill="none" stroke="{MUTE}" stroke-width="2" stroke-dasharray="6 8"/>'
    cards = card(*top, hl=True) + "".join(card(x, y, 180, 130, hl=(i == 2)) for i, (x, y) in enumerate(mids)) + "".join(card(x, y, 160, 110) for x, y in lows)
    pencil = '<g transform="translate(1280 700) rotate(-40)"><rect x="0" y="0" width="230" height="30" rx="4" fill="#1A1A1E" stroke="#C9A3FF" stroke-width="2.5"/><path d="M230 0 L270 15 L230 30 Z" fill="#C9A3FF"/><rect x="-26" y="0" width="26" height="30" rx="4" fill="#6A2CF5"/></g>'
    return frame(lines + cards + pencil, glow=(800, 300))

def rank():
    rows = ""
    y = 150
    for i in range(5):
        hl = i == 0
        h = 118
        rows += (f'<g opacity="{1 if hl else .9 - i*.14:.2f}"><rect x="360" y="{y}" width="880" height="{h}" rx="16" fill="{"#15121C" if hl else "#111113"}" stroke="{"url(#pg)" if hl else "#222226"}" stroke-width="{3 if hl else 1.5}"/>'
                 f'<text x="420" y="{y+72}" font-family="Georgia, serif" font-style="italic" font-size="46" fill="{"url(#pg)" if hl else "#4A4A48"}">{i+1}</text>'
                 f'<rect x="500" y="{y+30}" width="{380 if hl else 330 - i*20}" height="18" rx="9" fill="{"#C9A3FF" if hl else "#2E2E32"}"/>'
                 f'<rect x="500" y="{y+62}" width="{620 if hl else 560 - i*30}" height="12" rx="6" fill="#2A2A2E"/>'
                 f'<rect x="500" y="{y+84}" width="{480 if hl else 400 - i*30}" height="12" rx="6" fill="#222226"/></g>')
        if hl:
            rows += f'<rect x="360" y="{y}" width="880" height="{h}" rx="16" fill="none" stroke="url(#pg)" stroke-width="16" opacity=".35" filter="url(#soft)"/>'
            stars = "".join(f'<path transform="translate({1100+k*26} {y+44}) scale(.9)" d="M0 -12 L3.5 -4 L12 -3.5 L5.5 2 L7.5 10.5 L0 6 L-7.5 10.5 L-5.5 2 L-12 -3.5 L-3.5 -4 Z" fill="#C9A3FF"/>' for k in range(5))
            rows += stars
        y += h + 28
    search = f'<rect x="360" y="60" width="880" height="0" />'
    return frame(rows, glow=(800, 200))

def fold():
    bx, by, bw, bh = 330, 90, 940, 760
    fy = 470
    browser = (f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="22" fill="#0F0F11" stroke="{MUTE}" stroke-width="2.5"/>'
               f'<line x1="{bx}" y1="{by+56}" x2="{bx+bw}" y2="{by+56}" stroke="{MUTE}" stroke-width="2"/>'
               + "".join(f'<circle cx="{bx+34+i*26}" cy="{by+28}" r="7" fill="{c}"/>' for i, c in enumerate(["#3A3A38", "#3A3A38", "#3A3A38"]))
               + f'<rect x="{bx+130}" y="{by+16}" width="420" height="24" rx="12" fill="#18181B"/>')
    above = (f'<rect x="{bx+60}" y="{by+110}" width="120" height="14" rx="7" fill="#C9A3FF" opacity=".9"/>'
             f'<rect x="{bx+60}" y="{by+146}" width="560" height="40" rx="10" fill="{INK}"/>'
             f'<rect x="{bx+60}" y="{by+200}" width="420" height="40" rx="10" fill="{INK}" opacity=".85"/>'
             f'<rect x="{bx+60}" y="{by+262}" width="360" height="12" rx="6" fill="#4A4A48"/>'
             f'<rect x="{bx+60}" y="{by+306}" width="190" height="52" rx="26" fill="url(#pg)"/>'
             + "".join(f'<path transform="translate({bx+300+k*24} {by+332}) scale(.8)" d="M0 -12 L3.5 -4 L12 -3.5 L5.5 2 L7.5 10.5 L0 6 L-7.5 10.5 L-5.5 2 L-12 -3.5 L-3.5 -4 Z" fill="#C9A3FF"/>' for k in range(5))
             + f'<rect x="{bx+660}" y="{by+106}" width="220" height="254" rx="16" fill="#1A1622" stroke="#2E2640"/>'
             f'<circle cx="{bx+770}" cy="{by+200}" r="46" fill="url(#pg)" opacity=".7"/><path d="M{bx+690} {by+340} Q {bx+770} {by+250} {bx+850} {by+340}" fill="url(#pg)" opacity=".5"/>')
    below = "".join(f'<rect x="{bx+60+c*290}" y="{fy+50}" width="250" height="150" rx="14" fill="#141416" stroke="#1F1F22"/>' for c in range(3)) + \
            f'<rect x="{bx+60}" y="{fy+230}" width="820" height="14" rx="7" fill="#1C1C1F"/>'
    fl = (f'<line x1="{bx-80}" y1="{fy}" x2="{bx+bw+80}" y2="{fy}" stroke="url(#pgh)" stroke-width="3" stroke-dasharray="14 12"/>'
          f'<text x="{bx+bw+90}" y="{fy+8}" font-family="Helvetica, Arial, sans-serif" font-size="20" letter-spacing="5" fill="#9B5CFF">FOLD</text>')
    fade = f'<defs><linearGradient id="fd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0A0A0A" stop-opacity=".2"/><stop offset="1" stop-color="#0A0A0A" stop-opacity=".95"/></linearGradient></defs><rect x="{bx+2}" y="{fy+2}" width="{bw-4}" height="{by+bh-fy-4}" rx="0" fill="url(#fd)"/>'
    return frame(browser + above + below + fade + fl, glow=(700, 280))

def schema():
    nodes = [(1140, 250, "#C9A3FF"), (1330, 420, INK), (1160, 620, INK), (960, 450, "#9B5CFF"), (1380, 680, "#6E6E6A"), (980, 730, "#6E6E6A")]
    edges = [(3, 0), (3, 1), (3, 2), (1, 4), (2, 5), (0, 1)]
    e = "".join(f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="{MUTE}" stroke-width="2.5"/>' for a, b in edges)
    n = ""
    for i, (x, y, c) in enumerate(nodes):
        big = i == 3
        n += f'<circle cx="{x}" cy="{y}" r="{46 if big else 30}" fill="#111114" stroke="{"url(#pg)" if big else c}" stroke-width="{4 if big else 2.5}"/>'
        n += f'<rect x="{x-(22 if big else 14)}" y="{y-5}" width="{44 if big else 28}" height="10" rx="5" fill="{c}" opacity=".9"/>'
    code = ""
    lines = [(0, 170), (1, 300), (1, 240), (2, 220), (2, 260), (1, 280), (0, 150)]
    y = 310
    for ind, w in lines:
        if w:
            code += f'<rect x="{330+ind*40}" y="{y}" width="{int(w*0.45)}" height="14" rx="7" fill="#C9A3FF" opacity=".75"/><rect x="{330+ind*40+int(w*0.45)+12}" y="{y}" width="{int(w*0.5)}" height="14" rx="7" fill="#3A3A40"/>'
        y += 46
    braces = (f'<text x="150" y="620" font-family="Georgia, serif" font-size="420" fill="url(#pg)" opacity=".95">{{</text>'
              f'<text x="690" y="620" font-family="Georgia, serif" font-size="420" fill="url(#pg)" opacity=".95">}}</text>')
    glowb = f'<text x="150" y="620" font-family="Georgia, serif" font-size="420" fill="#9B5CFF" opacity=".35" filter="url(#soft)">{{</text>'
    return frame(glowb + braces + code + e + n + f'<circle cx="960" cy="450" r="70" fill="#9B5CFF" opacity=".25" filter="url(#soft)"/>', glow=(900, 450))

IMAGES = {
    "is-seo-a-one-time-thing": seo,
    "click-to-call": call,
    "speed-is-a-design-decision": speed,
    "how-i-plan-a-website-before-opening-figma": plan,
    "what-makes-a-service-page-rank": rank,
    "five-things-every-homepage-needs-above-the-fold": fold,
    "schema-markup-explained-without-the-jargon": schema,
}

if __name__ == "__main__":
    import sys
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for slug, fn in IMAGES.items():
        open(os.path.join(out, slug + ".svg"), "w").write(fn())
    print("wrote", len(IMAGES))
