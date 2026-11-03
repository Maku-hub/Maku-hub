"""Build the self-updating SVGs in assets/generated/ from public GitHub data.

Runs daily in GitHub Actions (.github/workflows/profile.yml); standard library only.
Each card is built independently — if one source fails, the previous file is kept.
"""

import hashlib
import json
import os
import sys
import textwrap
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

USER = os.environ.get("GITHUB_REPOSITORY_OWNER", "Maku-hub")
TOKEN = os.environ.get("GITHUB_TOKEN")
OUT = Path(__file__).resolve().parent.parent / "assets" / "generated"

MONO = "font-family=\"'Cascadia Code','Consolas','Courier New',monospace\""
SANS = "font-family=\"'Segoe UI',Helvetica,Arial,sans-serif\""
PURPLE, VIOLET, ORANGE = "#7b2fff", "#a66bff", "#ff6a00"
LANE_COLORS = [ORANGE, "#22d3ee", "#4ade80", "#f87171", "#facc15"]
LANG_COLORS = {
    "Python": "#3572A5", "C++": "#f34b7d", "C": "#555555", "TypeScript": "#3178c6",
    "JavaScript": "#f1e05a", "Go": "#00ADD8", "HTML": "#e34c26", "CSS": "#563d7c",
    "Shell": "#89e051", "PowerShell": "#5391FE", "Dockerfile": "#384d54", "Rust": "#dea584",
    "Java": "#b07219", "C#": "#178600", "HCL": "#844FBA", "Lua": "#000080",
}
FALLBACK_COLORS = ["#a66bff", "#ff6a00", "#22d3ee", "#4ade80", "#facc15", "#f87171"]


def get(url, raw=False):
    req = urllib.request.Request(url, headers={"User-Agent": f"{USER}-profile"})
    if not raw:
        req.add_header("Accept", "application/vnd.github+json")
        if TOKEN:
            req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
    return body if raw else json.loads(body)


def api(path):
    return get(f"https://api.github.com{path}")


def truncate(text, limit):
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def own_repos():
    repos = [
        r for r in api(f"/users/{USER}/repos?per_page=100&type=owner")
        if not r["fork"] and r["name"].lower() != USER.lower()
    ]
    repos.sort(key=lambda r: r["created_at"], reverse=True)
    return repos


# ------------------------------------------------------------------ git log
def prompt(command):
    """Shell prompt line styled like assets/terminal.svg."""
    return (
        f'<tspan fill="#7ee787">maku@hub</tspan><tspan fill="#8b949e">:</tspan><tspan fill="{VIOLET}">~</tspan>'
        f'<tspan fill="#8b949e">$ </tspan><tspan fill="#f0f6fc">{escape(command)}</tspan>'
    )


def gitlog(user, repos, max_repos=9, max_lanes=5, width=800):
    shown = repos[:max_repos]
    langs = [r["language"] or "docs" for r in shown]
    ranked = sorted(set(langs), key=lambda l: (-langs.count(l), langs.index(l)))
    if len(ranked) <= max_lanes:
        lanes = {lang: i for i, lang in enumerate(ranked)}
    else:
        lanes = {lang: i for i, lang in enumerate(ranked[: max_lanes - 1])}
        lanes["other"] = max_lanes - 1
    lane_of = lambda r: lanes.get(r["language"] or "docs", lanes.get("other"))
    main_x = 40
    lane_x = lambda i: 68 + i * 26
    lane_color = lambda i: LANE_COLORS[i % len(LANE_COLORS)]

    now = datetime.now(timezone.utc).strftime("%Y-%m")
    rows = [("main", now, f"Merge: {len(repos)} repositories and counting", "HEAD -> main")]
    rows += [(lane_of(r), r["created_at"][:7], r["description"] or f"feat: {r['name']}", r["name"]) for r in shown]
    rows.append(("main", user["created_at"][:7], "init: hello, world", "first commit"))

    y0, dy = 66, 34
    n = len(rows)
    ys = [y0 + i * dy for i in range(n)]
    total_t = 6.0
    appear = lambda i: 0.3 + (n - 1 - i) * (total_t / n)  # rows appear bottom-up

    def drawn(d, color, begin, end):
        # pathLength="1" lets every line grow in step with the commits it connects
        return (
            f'<path d="{d}" stroke="{color}" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1">'
            f'<animate attributeName="stroke-dashoffset" from="1" to="0" begin="{begin:.2f}s" dur="{max(end - begin, 0.3):.2f}s" fill="freeze"/></path>'
        )

    paths = [drawn(f"M{main_x} {ys[-1]} V{ys[0]}", VIOLET, appear(n - 1), appear(0))]
    for lane in set(lanes.values()):
        idx = [i for i, row in enumerate(rows) if row[0] == lane]
        if not idx:
            continue
        lx, color = lane_x(lane), lane_color(lane)
        yb, yt = ys[max(idx)] + 19, ys[0] + 16
        d = (
            f"M{main_x} {yb+12} C{main_x} {yb} {lx} {yb+9} {lx} {yb-5} V{yt+9} "
            f"C{lx} {yt-4} {main_x} {yt+6} {main_x} {ys[0]}"
        )
        paths.append(drawn(d, color, appear(max(idx)) - 0.2, appear(0)))
    body = []
    for i, (lane, month, msg, ref) in enumerate(rows):
        lx, color = (main_x, VIOLET) if lane == "main" else (lane_x(lane), lane_color(lane))
        y = ys[i]
        sha = hashlib.sha1(f"{ref}{month}".encode()).hexdigest()[:7]
        t = appear(i)
        ref = truncate(ref, 24)
        refw = len(ref) * 6.6 + 14
        msg_x = 322 + refw + 10
        msg = truncate(msg, int((width - msg_x - 24) / 7.2))
        body.append(
            f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
            f'<circle cx="{lx}" cy="{y}" r="6" fill="#0d1117" stroke="{color}" stroke-width="2.5"/>'
            f'<text x="190" y="{y+4}" fill="#e3b341">{sha}</text>'
            f'<text x="252" y="{y+4}" fill="#8b949e">{month}</text>'
            f'<rect x="322" y="{y-9}" width="{refw:.0f}" height="18" rx="9" fill="none" stroke="{color}"/>'
            f'<text x="{322+refw/2:.0f}" y="{y+4}" fill="{color}" text-anchor="middle" font-size="11">{escape(ref)}</text>'
            f'<text x="{msg_x:.0f}" y="{y+4}" fill="#e6edf3">{escape(msg)}</text></g>'
        )
    legend_top = ys[-1] + 40
    legend, x, ly = [], 24, legend_top
    for name, i in [("me", None)] + sorted(lanes.items(), key=lambda kv: kv[1]):
        color = VIOLET if i is None else lane_color(i)
        label = name.lower()
        item_w = 16 + len(label) * 6.6 + 22
        if x + item_w > width - 24:
            x, ly = 24, ly + 20
        legend.append(
            f'<circle cx="{x+5}" cy="{ly-4}" r="4.5" fill="none" stroke="{color}" stroke-width="2"/>'
            f'<text x="{x+16}" y="{ly}" fill="#8b949e" font-size="11">{escape(label)}</text>'
        )
        x += item_w
    h = ly + 20
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{h}" viewBox="0 0 {width} {h}" {MONO} font-size="12">
  <rect width="{width}" height="{h}" rx="12" fill="#0d1117" stroke="#30363d"/>
  <text x="24" y="36">{prompt(f"gh repo list {USER.lower()} --source")}</text>
  <g fill="none" stroke-width="2.5" stroke-linecap="round">{''.join(paths)}</g>
  {''.join(body)}
  <line x1="24" y1="{legend_top-20}" x2="{width-24}" y2="{legend_top-20}" stroke="#21262d"/>
  {''.join(legend)}
</svg>
"""


# ---------------------------------------------------------------- languages
def languages(user, repos, width=800):
    totals = {}
    for r in repos:
        for lang, size in api(f"/repos/{r['full_name']}/languages").items():
            totals[lang] = totals.get(lang, 0) + size
    ranked = sorted(totals.items(), key=lambda kv: -kv[1])
    top = ranked[:6]
    rest = sum(v for _, v in ranked[6:])
    if rest:
        top.append(("Other", rest))
    grand = sum(v for _, v in top) or 1
    color_of = lambda i, lang: LANG_COLORS.get(lang, FALLBACK_COLORS[i % len(FALLBACK_COLORS)]) if lang != "Other" else "#6e7681"

    bar_x, bar_w, bar_y = 28, width - 56, 92
    segs, x = [], bar_x
    for i, (lang, size) in enumerate(top):
        w = bar_w * size / grand
        segs.append(
            f'<rect x="{x:.1f}" y="{bar_y}" width="0" height="14" fill="{color_of(i, lang)}">'
            f'<animate attributeName="width" from="0" to="{max(w - 2, 1):.1f}" begin="{0.2 + i * 0.12:.2f}s" dur="0.8s" fill="freeze"/></rect>'
        )
        x += w
    legend = []
    for i, (lang, size) in enumerate(top):
        col, row = i % 4, i // 4
        lx, ly = 28 + col * 186, 140 + row * 28
        legend.append(
            f'<circle cx="{lx+6}" cy="{ly-4}" r="6" fill="{color_of(i, lang)}"/>'
            f'<text x="{lx+20}" y="{ly}" fill="#e6edf3" font-size="13">{escape(lang)} '
            f'<tspan fill="#8b949e">{100 * size / grand:.1f}%</tspan></text>'
        )
    stars = sum(r["stargazers_count"] for r in repos)
    years = (datetime.now(timezone.utc) - datetime.fromisoformat(user["created_at"].replace("Z", "+00:00"))).days / 365.25
    facts = [
        (str(len(repos)), "repositories"),
        (str(len(totals)), "languages"),
        (str(stars), "stars"),
        (f"{years:.1f}", "years on GitHub"),
    ]
    fact_svg = []
    for i, (value, label) in enumerate(facts):
        fx = 28 + i * 186
        fact_svg.append(
            f'<text x="{fx}" y="238" fill="#ffffff" font-size="26" font-weight="700">{escape(value)}</text>'
            f'<text x="{fx}" y="258" fill="#8b949e" font-size="12">{escape(label)}</text>'
        )
    h = 280
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{h}" viewBox="0 0 {width} {h}" {SANS}>
  <rect width="{width}" height="{h}" rx="16" fill="#0d1117" stroke="#30363d"/>
  <text x="28" y="44" fill="{VIOLET}" font-size="12" font-weight="700" letter-spacing="3">CODE DNA</text>
  <text x="28" y="72" fill="#e6edf3" font-size="20" font-weight="700">What my public code is made of</text>
  <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="14" rx="7" fill="#21262d"/>
  {''.join(segs)}
  {''.join(legend)}
  <line x1="28" y1="200" x2="{width-28}" y2="200" stroke="#21262d"/>
  {''.join(fact_svg)}
  <text x="{width-28}" y="44" fill="#6e7681" font-size="11" text-anchor="end" {MONO}>updated {date.today().isoformat()}</text>
</svg>
"""


# ------------------------------------------------------------------ fortune
FORTUNES = [
    ("Simplicity is prerequisite for reliability.", "Edsger W. Dijkstra"),
    ("Everything fails, all the time.", "Werner Vogels"),
    ("Security is a process, not a product.", "Bruce Schneier"),
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("There are only two hard things in Computer Science: cache invalidation and naming things.", "Phil Karlton"),
    ("It's not DNS. There's no way it's DNS. It was DNS.", None),
    ("If you do it twice, script it. If you script it twice, make it a pipeline.", None),
    ("Hope is not a strategy.", None),
    ("The S in IoT stands for security.", None),
    ("chmod 777 is not a fix, it's a confession.", None),
    ("Works on my machine — so we shipped your machine. That's how Docker was born.", None),
    ("A secret in git history is a secret no more.", None),
    ("Monitoring tells you something is broken. Observability tells you why.", None),
    ("Every alert should be actionable. Every action should be automated.", None),
    ("Friday deploys are fine if your rollback is boring.", None),
    ("Least privilege: because 'admin' is not a personality.", None),
    ("Pin your dependencies. Future you will send a thank-you card.", None),
    ("The cloud is just someone else's computer. Patch it anyway.", None),
    ("Infrastructure as Code: because clicking is not reproducible.", None),
    ("Logs are love letters to your future self at 3 AM.", None),
    ("Defense in depth: assume the first wall is made of cardboard.", None),
    ("An SBOM a day keeps the supply-chain attack away.", None),
    ("Blameless postmortems, blame-full TODOs.", None),
    ("Rotate your keys before someone else does.", None),
    ("If it's not in version control, it doesn't exist.", None),
    ("Shift left, but don't fall off the edge.", None),
    ("Zero trust, one coffee.", None),
    ("The best incident is the one your pipeline caught.", None),
    ("Automate the boring stuff, document the weird stuff.", None),
    ("Uptime is a team sport.", None),
]

COW = r"""        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||"""


def fortune(width=800):
    today = date.today()
    quote, author = FORTUNES[today.toordinal() % len(FORTUNES)]
    lines = textwrap.wrap(quote, 52)
    if author:
        lines.append(f"  — {author}")
    inner = max(len(l) for l in lines)
    bubble = [" " + "_" * (inner + 2)]
    if len(lines) == 1:
        bubble.append(f"< {lines[0].ljust(inner)} >")
    else:
        for i, l in enumerate(lines):
            left, right = ("/", "\\") if i == 0 else ("\\", "/") if i == len(lines) - 1 else ("|", "|")
            bubble.append(f"{left} {l.ljust(inner)} {right}")
    bubble.append(" " + "-" * (inner + 2))
    art = bubble + COW.splitlines()
    y0, dy = 64, 17
    text = "".join(
        f'<text x="24" y="{y0 + i * dy}" fill="{"#e6edf3" if i < len(bubble) else "#c4b5fd"}">{escape(line).replace(" ", chr(160))}</text>'
        for i, line in enumerate(art)
    )
    h = y0 + len(art) * dy + 12
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{h}" viewBox="0 0 {width} {h}" {MONO} font-size="12" xml:space="preserve" style="white-space:pre">
  <rect width="{width}" height="{h}" rx="12" fill="#0d1117" stroke="#30363d"/>
  <text x="24" y="36">{prompt("fortune platform | cowsay")}</text>
  <text x="{width-24}" y="36" fill="#6e7681" font-size="11" text-anchor="end">quote of the day · {today.isoformat()}</text>
  {text}
</svg>
"""


# ------------------------------------------------------------ recent commits
def ago(when, now):
    seconds = (now - when).total_seconds()
    for unit, size in (("y", 365 * 86400), ("mo", 30 * 86400), ("w", 7 * 86400), ("d", 86400), ("h", 3600), ("m", 60)):
        if seconds >= size:
            return f"{int(seconds // size)}{unit} ago"
    return "just now"


def recent_commits(repos, limit=10, width=800):
    # No author filter: commits made with an email not linked to the account
    # have no GitHub login, but they are still the owner's work in the owner's repos.
    commits = []
    for r in repos:
        try:
            items = api(f"/repos/{r['full_name']}/commits?per_page={limit}")
        except Exception:  # empty repositories answer 409
            continue
        for c in items:
            if (c.get("author") or {}).get("type") == "Bot":
                continue
            commits.append({
                "repo": r["name"],
                "sha": c["sha"][:7],
                "when": datetime.fromisoformat(c["commit"]["author"]["date"].replace("Z", "+00:00")),
                "msg": c["commit"]["message"].splitlines()[0] if c["commit"]["message"] else "",
            })
    commits.sort(key=lambda c: c["when"], reverse=True)
    commits = commits[:limit]

    palette = [VIOLET, ORANGE, "#22d3ee", "#4ade80", "#f87171", "#facc15", "#60a5fa", "#f472b6"]
    colors = {}
    for c in commits:
        colors.setdefault(c["repo"], palette[len(colors) % len(palette)])

    now = datetime.now(timezone.utc)
    y0, dy = 66, 30
    line_x = 36
    rows = []
    for i, c in enumerate(commits):
        y = y0 + i * dy
        color = colors[c["repo"]]
        t = 0.3 + i * 0.25
        ref = truncate(c["repo"], 22)
        refw = len(ref) * 6.6 + 14
        msg_x = 244 + refw + 10
        msg = truncate(c["msg"], int((width - msg_x - 24) / 7.2))
        rows.append(
            f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
            f'<circle cx="{line_x}" cy="{y}" r="5" fill="#0d1117" stroke="{color}" stroke-width="2.5"/>'
            f'<text x="60" y="{y+4}" fill="#e3b341">{c["sha"]}</text>'
            f'<text x="124" y="{y+4}" fill="#8b949e">{ago(c["when"], now)}</text>'
            f'<rect x="244" y="{y-9}" width="{refw:.0f}" height="18" rx="9" fill="none" stroke="{color}"/>'
            f'<text x="{244+refw/2:.0f}" y="{y+4}" fill="{color}" text-anchor="middle" font-size="11">{escape(ref)}</text>'
            f'<text x="{msg_x:.0f}" y="{y+4}" fill="#e6edf3">{escape(msg)}</text></g>'
        )
    if not commits:
        rows.append(f'<text x="60" y="{y0+4}" fill="#8b949e">no public commits yet</text>')
    last_y = y0 + max(len(commits) - 1, 0) * dy
    h = last_y + 30
    line = (
        f'<path d="M{line_x} {y0} V{last_y}" stroke="#30363d" stroke-width="2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1">'
        f'<animate attributeName="stroke-dashoffset" from="1" to="0" begin="0.3s" dur="{0.25 * max(len(commits), 1):.2f}s" fill="freeze"/></path>'
        if len(commits) > 1 else ""
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{h}" viewBox="0 0 {width} {h}" {MONO} font-size="12">
  <rect width="{width}" height="{h}" rx="12" fill="#0d1117" stroke="#30363d"/>
  <text x="24" y="36">{prompt(f"git log --all-repos --oneline -n {limit} --author={USER.lower()}")}</text>
  {line}
  {''.join(rows)}
</svg>
"""


# --------------------------------------------------------------------- main
def build(name, make):
    try:
        (OUT / name).write_text(make(), encoding="utf-8", newline="\n")
        print(f"ok    {name}")
        return True
    except Exception as exc:  # keep the previous file if a source is down
        print(f"FAIL  {name}: {exc}", file=sys.stderr)
        return False


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = [build("fortune.svg", fortune)]
    try:
        user, repos = api(f"/users/{USER}"), own_repos()
    except Exception as exc:
        print(f"FAIL  GitHub API: {exc}", file=sys.stderr)
        sys.exit(1)
    results.append(build("gitlog.svg", lambda: gitlog(user, repos)))
    results.append(build("commits.svg", lambda: recent_commits(repos)))
    results.append(build("languages.svg", lambda: languages(user, repos)))
    if not any(results):
        sys.exit(1)


if __name__ == "__main__":
    main()
