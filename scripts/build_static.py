"""Build the hand-made, never-changing SVGs in assets/.

Run locally after tweaking text or colours:  python scripts/build_static.py
"""

import random
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent / "assets"
MONO = "font-family=\"'Cascadia Code','Consolas','Courier New',monospace\""
SANS = "font-family=\"'Segoe UI',Helvetica,Arial,sans-serif\""

PURPLE, VIOLET, ORANGE = "#7b2fff", "#a66bff", "#ff6a00"


def write(name, content):
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / name).write_text(content, encoding="utf-8", newline="\n")


# --------------------------------------------------------------------- hero
def hero():
    rnd = random.Random(42)
    glyphs = "01ABCDEF<>/{}$#*=+"
    cols = []
    for i in range(46):
        x = 8 + i * 17.5
        n = rnd.randint(10, 22)
        chars = "".join(
            f'<tspan x="{x:.1f}" dy="17" fill-opacity="{0.15 + 0.85 * (k + 1) / n:.2f}">{escape(rnd.choice(glyphs))}</tspan>'
            for k in range(n)
        )
        head = f'<tspan x="{x:.1f}" dy="17" fill="#e9d5ff">{escape(rnd.choice(glyphs))}</tspan>'
        dur = rnd.uniform(4, 9)
        cols.append(
            f'<text class="col" y="-{n*17}" style="animation-duration:{dur:.1f}s;animation-delay:-{rnd.uniform(0, dur):.1f}s">{chars}{head}</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="190" viewBox="0 0 800 190">
  <!-- flag 3/3: flag{{1m4g3s_h4v3_s0urc3_t00}} -->
  <defs>
    <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#07050d" stop-opacity="0.2"/><stop offset="0.6" stop-color="#07050d" stop-opacity="0.75"/><stop offset="1" stop-color="#07050d"/></linearGradient>
    <linearGradient id="title" x1="0" x2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e9d5ff"/></linearGradient>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#ffffff" fill-opacity="0.04"/></pattern>
    <clipPath id="frame"><rect width="800" height="190" rx="16"/></clipPath>
    <style>
      .col {{ font: 14px 'Cascadia Code', Consolas, monospace; fill: {PURPLE}; animation: fall linear infinite; }}
      @keyframes fall {{ from {{ transform: translateY(0); }} to {{ transform: translateY(520px); }} }}
      .t {{ font: 900 96px 'Segoe UI', 'Arial Black', Arial, sans-serif; letter-spacing: 5px; }}
      .g1 {{ fill: #22d3ee; animation: g1 3.2s steps(1) infinite; }}
      .g2 {{ fill: {ORANGE}; animation: g2 3.2s steps(1) infinite; }}
      .g0 {{ animation: g0 3.2s steps(1) infinite; }}
      @keyframes g1 {{ 0%,86%,100% {{ transform: translate(-3px,0); }} 88% {{ transform: translate(-14px,3px); }} 90% {{ transform: translate(9px,-2px); }} 92% {{ transform: translate(-6px,0); }} 95% {{ transform: translate(12px,2px); }} }}
      @keyframes g2 {{ 0%,86%,100% {{ transform: translate(3px,0); }} 88% {{ transform: translate(12px,-3px); }} 90% {{ transform: translate(-10px,2px); }} 92% {{ transform: translate(7px,0); }} 95% {{ transform: translate(-12px,-2px); }} }}
      @keyframes g0 {{ 0%,86%,100% {{ transform: none; opacity: 1; }} 89% {{ transform: skewX(-12deg); opacity: 0.85; }} 93% {{ transform: translate(4px,0); }} }}
      .slice {{ animation: slice 3.2s steps(1) infinite; }}
      @keyframes slice {{ 0%,87%,97%,100% {{ opacity: 0; }} 88% {{ opacity: 1; transform: translate(0, 0); }} 91% {{ opacity: 1; transform: translate(0, 24px); }} 94% {{ opacity: 1; transform: translate(0, -16px); }} }}
      .bar {{ animation: sweep 6s linear infinite; }}
      @keyframes sweep {{ from {{ transform: translateY(-30px); }} to {{ transform: translateY(220px); }} }}
      .sub {{ font: 600 15px 'Cascadia Code', Consolas, monospace; letter-spacing: 6px; fill: #c4b5fd; }}
      .hud {{ font: 11px 'Cascadia Code', Consolas, monospace; fill: #8b7fb3; letter-spacing: 1px; }}
      .caret {{ animation: blink 1s steps(1) infinite; }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
    </style>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="800" height="190" fill="#07050d"/>
    <g>{''.join(cols)}</g>
    <rect width="800" height="190" fill="url(#fade)"/>
    <g text-anchor="middle">
      <text class="t g1" x="400" y="112" fill-opacity="0.8">MAKU</text>
      <text class="t g2" x="400" y="112" fill-opacity="0.8">MAKU</text>
      <text class="t g0" x="400" y="112" fill="url(#title)">MAKU</text>
      <g class="slice"><rect x="240" y="66" width="320" height="12" fill="#07050d"/><rect x="270" y="88" width="260" height="4" fill="{ORANGE}"/></g>
    </g>
    <text class="sub" x="400" y="148" text-anchor="middle">PLATFORM ENGINEER<tspan class="caret" fill="{ORANGE}">_</tspan></text>
    <rect class="bar" x="0" y="0" width="800" height="30" fill="{VIOLET}" fill-opacity="0.06"/>
    <rect width="800" height="190" fill="url(#scan)"/>
    <g fill="none" stroke="{VIOLET}" stroke-width="2" stroke-opacity="0.7">
      <path d="M16 38 V16 H38"/><path d="M762 16 H784 V38"/><path d="M16 152 V174 H38"/><path d="M762 174 H784 V152"/>
    </g>
    <text class="hud" x="48" y="30">SYS://MAKU-HUB · v2.0</text>
    <text class="hud" x="752" y="30" text-anchor="end">SEC LEVEL ▮▮▮▮▮▮▮▯ 92%</text>
    <text class="hud" x="48" y="168">UPTIME 99.9%</text>
    <text class="hud" x="752" y="168" text-anchor="end">STATUS: <tspan fill="#4ade80">ONLINE</tspan></text>
  </g>
</svg>
"""


# ----------------------------------------------------------------- terminal
def terminal():
    script = [
        ("cmd", "cat /etc/motd"),
        ("out", "Welcome to Maku's corner of GitHub.", "#d2a8ff"),
        ("out", "Connecting people, systems, and ideas into working solutions.", "#d2a8ff"),
        ("cmd", "cat role.txt"),
        ("out", "Platform Engineer — reliable systems, secure by default.", "#c9d1d9"),
        ("cmd", "ls ~/toolbox | more"),
        ("out", "linux/  docker/  kubernetes/  helm/  terraform/  ansible/  nginx/", "#79c0ff"),
        ("out", "github-actions/  gitlab-ci/  prometheus/  grafana/  loki/  vault/", "#79c0ff"),
        ("out", "trivy/  cyclonedx/  semgrep/  sonarqube/  burp-suite/  nmap/  wireshark/", "#79c0ff"),
        ("more", "--More--(32%)"),
        ("cmd", "./scan --interests"),
        ("out", "[+] system-design         [+] embedded   [+] smarthome", "#ffa657"),
        ("out", "[+] cybersecurity         [+] gambling   [+] scuba diving", "#ffa657"),
        ("cmd", "sudo rm -rf /bugs"),
        ("out", "[sudo] password for maku: ********  — nice try.", "#f85149"),
    ]
    prompt = "maku@hub:~$ "
    cw = 7.2
    y0, dy = 36, 22
    t = 0.6
    defs, body = [], []
    for i, line in enumerate(script):
        y = y0 + i * dy
        if line[0] == "cmd":
            p_w = len(prompt) * cw
            full = len(prompt + line[1]) * cw + 40
            dur = max(0.4, len(line[1]) * 0.05)
            defs.append(
                f'<clipPath id="c{i}"><rect x="20" y="{y-18}" height="24" width="0">'
                f'<set attributeName="width" to="{p_w:.0f}" begin="{t:.2f}s" fill="freeze"/>'
                f'<animate attributeName="width" from="{p_w:.0f}" to="{full:.0f}" begin="{t+0.25:.2f}s" dur="{dur:.2f}s" fill="freeze"/>'
                f"</rect></clipPath>"
            )
            body.append(
                f'<text x="24" y="{y}" clip-path="url(#c{i})">'
                f'<tspan fill="#7ee787">maku@hub</tspan><tspan fill="#8b949e">:</tspan>'
                f'<tspan fill="{VIOLET}">~</tspan><tspan fill="#8b949e">$ </tspan>'
                f'<tspan fill="#f0f6fc">{escape(line[1])}</tspan></text>'
            )
            t += 0.25 + dur + 0.35
        elif line[0] == "more":
            # reverse-video pager prompt, like `more` waiting for a keypress
            body.append(
                f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
                f'<rect x="22" y="{y-13}" width="{len(line[1]) * cw + 4:.0f}" height="17" fill="#c9d1d9"/>'
                f'<text x="24" y="{y}" fill="#0d1117">{escape(line[1])}</text></g>'
            )
            t += 0.6
        else:
            body.append(
                f'<text x="24" y="{y}" fill="{line[2]}" opacity="0">{escape(line[1]).replace(" ", chr(160))}'
                f'<set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/></text>'
            )
            t += 0.18
    y = y0 + len(script) * dy
    body.append(
        f'<text x="24" y="{y}" opacity="0"><tspan fill="#7ee787">maku@hub</tspan>'
        f'<tspan fill="#8b949e">:</tspan><tspan fill="{VIOLET}">~</tspan><tspan fill="#8b949e">$ </tspan>'
        f'<set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/></text>'
    )
    cx = 24 + len(prompt) * cw
    body.append(
        f'<rect x="{cx:.0f}" y="{y-12}" width="8" height="15" fill="{VIOLET}" opacity="0">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" begin="{t:.2f}s" repeatCount="indefinite"/></rect>'
    )
    h = y + 24
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{h}" viewBox="0 0 800 {h}" {MONO} font-size="12" xml:space="preserve" style="white-space:pre">
  <defs>{''.join(defs)}</defs>
  <rect width="800" height="{h}" rx="12" fill="#0d1117" stroke="#30363d"/>
  {''.join(body)}
</svg>
"""


# ------------------------------------------------------------ DevSecOps loop
def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return tuple(u**3 * a + 3 * u * u * t * b + 3 * u * t * t * c + t**3 * d for a, b, c, d in zip(p0, p1, p2, p3))


def loop():
    period = 8.0
    segs = [
        ((400, 150), (470, 50), (660, 50), (660, 150)),
        ((660, 150), (660, 250), (470, 250), (400, 150)),
        ((400, 150), (330, 50), (140, 50), (140, 150)),
        ((140, 150), (140, 250), (330, 250), (400, 150)),
    ]
    d = "M400 150 " + " ".join(f"C{s[1][0]} {s[1][1]} {s[2][0]} {s[2][1]} {s[3][0]} {s[3][1]}" for s in segs) + " Z"
    stages = [
        ("PLAN", 2, 0.5, 0, -18, "middle"), ("CODE", 2, 0.95, -16, 5, "end"),
        ("BUILD", 3, 0.3, -10, 26, "end"), ("TEST", 3, 0.75, -6, 30, "middle"),
        ("RELEASE", 0, 0.5, 0, -18, "middle"), ("DEPLOY", 0, 0.95, 16, 5, "start"),
        ("OPERATE", 1, 0.3, 10, 26, "start"), ("MONITOR", 1, 0.75, 6, 30, "middle"),
    ]
    labels = []
    for name, seg, t, dx, dy, anchor in stages:
        x, y = cubic(*segs[seg], t)
        frac = (seg + t) / 4
        labels.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#30363d">'
            f'<animate attributeName="fill" values="#ffffff;{ORANGE};#30363d;#30363d" keyTimes="0;0.06;0.3;1" dur="{period}s" begin="{frac*period:.2f}s" repeatCount="indefinite"/></circle>'
            f'<text x="{x+dx:.0f}" y="{y+dy:.0f}" text-anchor="{anchor}" fill="#6e7681" font-size="13" font-weight="700" letter-spacing="2">{name}'
            f'<animate attributeName="fill" values="#ffffff;#ffffff;#6e7681;#6e7681" keyTimes="0;0.1;0.35;1" dur="{period}s" begin="{frac*period:.2f}s" repeatCount="indefinite"/></text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="300" viewBox="0 0 800 300" {SANS}>
  <defs>
    <linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{PURPLE}"/><stop offset="0.5" stop-color="#d63af9"/><stop offset="1" stop-color="{ORANGE}"/></linearGradient>
    <filter id="glow" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="800" height="300" rx="16" fill="#0d1117"/>
  <text x="270" y="160" text-anchor="middle" fill="{PURPLE}" fill-opacity="0.25" font-size="40" font-weight="800">DEV</text>
  <text x="530" y="160" text-anchor="middle" fill="{ORANGE}" fill-opacity="0.25" font-size="40" font-weight="800">OPS</text>
  <path id="loop" d="{d}" fill="none" stroke="url(#g)" stroke-width="14" stroke-linecap="round" opacity="0.9"/>
  <path d="{d}" fill="none" stroke="#ffffff" stroke-opacity="0.25" stroke-width="2" stroke-dasharray="4 10">
    <animate attributeName="stroke-dashoffset" from="0" to="-140" dur="3s" repeatCount="indefinite"/>
  </path>
  {''.join(labels)}
  <circle r="8" fill="#ffffff" filter="url(#glow)"><animateMotion dur="{period}s" repeatCount="indefinite"><mpath href="#loop"/></animateMotion></circle>
  <path d="M400 116 L430 127 V151 C430 172 416 185 400 192 C384 185 370 172 370 151 V127 Z" fill="#0d1117" stroke="{ORANGE}" stroke-width="3"/>
  <text x="400" y="162" text-anchor="middle" fill="#ffffff" font-size="13" font-weight="800" letter-spacing="1">SEC</text>
  <text x="24" y="32" fill="#8b949e" font-size="12" letter-spacing="2">SECURITY AT EVERY STAGE</text>
</svg>
"""


# ------------------------------------------------------------------ divider
def divider():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="16" viewBox="0 0 800 16">
  <defs>
    <linearGradient id="line" x1="0" x2="1"><stop offset="0" stop-color="{PURPLE}" stop-opacity="0"/><stop offset="0.5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></linearGradient>
    <radialGradient id="pulse"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>
  </defs>
  <rect x="0" y="7" width="800" height="2" fill="url(#line)"/>
  <ellipse cy="8" rx="40" ry="5" fill="url(#pulse)">
    <animate attributeName="cx" values="-40;840" dur="3.5s" repeatCount="indefinite"/>
  </ellipse>
</svg>
"""


# --------------------------------------------------------------- CTF board
def ctf():
    challenges = [
        ("01", "ENCODING", "Plain sight", ["Hidden in plain sight.", "Well, in the source."], 100, 1, VIOLET),
        ("02", "FORENSICS", "The dump", ["Somewhere in a dump.", "Read it carefully."], 200, 2, "#22d3ee"),
        ("03", "STEGANOGRAPHY", "Source code", ["Images have source", "code too."], 300, 3, ORANGE),
    ]
    cards = []
    for i, (num, category, title, hint, points, level, color) in enumerate(challenges):
        x, y, w, h = 28 + i * 256, 96, 232, 156
        hint_svg = "".join(
            f'<text x="{x+18}" y="{y+96+k*18}" fill="#8b949e" font-size="12" {MONO}>{escape(line)}</text>'
            for k, line in enumerate(hint)
        )
        dots = "".join(
            f'<circle cx="{x+w-58+k*12}" cy="{y+h-22}" r="4" fill="{color if k < level else "#30363d"}"/>' for k in range(3)
        )
        cards.append(f"""
  <g>
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#161b22" stroke="{color}" stroke-opacity="0.35">
      <animate attributeName="stroke-opacity" values="0.35;0.9;0.35" dur="3s" begin="{i}s" repeatCount="indefinite"/>
    </rect>
    <rect x="{x}" y="{y}" width="{w}" height="4" rx="2" fill="{color}"/>
    <g transform="translate({x+w-62} {y+50})" fill="{color}" opacity="0.14"><rect width="4" height="68"/><path d="M4 0 h40 l-10 14 l10 14 h-40z"/></g>
    <text x="{x+18}" y="{y+32}" fill="{color}" font-size="13" font-weight="700" {MONO}>#{num}</text>
    <text x="{x+w-18}" y="{y+32}" fill="#8b949e" font-size="10" letter-spacing="2" text-anchor="end">{category}</text>
    <text x="{x+18}" y="{y+66}" fill="#ffffff" font-size="20" font-weight="700">{escape(title)}</text>
    {hint_svg}
    <text x="{x+18}" y="{y+h-18}" fill="{color}" font-size="12" font-weight="700" {MONO}>{points} PTS</text>
    {dots}
  </g>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="280" viewBox="0 0 800 280" {SANS}>
  <rect width="800" height="280" rx="16" fill="#0d1117" stroke="#30363d"/>
  <rect x="28" y="31" width="9" height="9" fill="{ORANGE}"><animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite"/></rect>
  <text x="46" y="40" fill="{VIOLET}" font-size="12" font-weight="700" letter-spacing="3">CAPTURE THE FLAG</text>
  <text x="772" y="40" fill="#6e7681" font-size="11" text-anchor="end" {MONO}>3 flags · format: flag{{...}}</text>
  <text x="28" y="72" fill="#e6edf3" font-size="15">Three flags are hidden in this profile. Found them all? You know where to find me.</text>
  {''.join(cards)}
</svg>
"""


def main():
    write("hero.svg", hero())
    write("terminal.svg", terminal())
    write("loop.svg", loop())
    write("divider.svg", divider())
    write("ctf.svg", ctf())


if __name__ == "__main__":
    main()
