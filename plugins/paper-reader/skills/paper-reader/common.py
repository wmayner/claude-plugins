"""Shared helpers for paper-reader converters: KaTeX CSS with inlined fonts, template filling, publish batches."""
import base64, json, re, subprocess, urllib.request
from pathlib import Path

SKILL = Path(__file__).parent
CACHE = Path.home() / ".cache/paper-reader"
KATEX = "0.16.11"  # must match the katex.min.js version in template.html
UA = {"User-Agent": "paper-reader/1.0 (personal reading copy)"}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60)


def download(url, dest: Path):
    """Fetch a file with curl (arXiv's CDN answers some of urllib's requests with 406 that curl gets fine)."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["curl", "-sfL", "--retry", "3", "-A", UA["User-Agent"], "-o", str(dest), url], check=True)


def figure_tone(path: Path):
    """'line' for figures that read correctly with lightness inverted (diagrams, plots on white: mostly white and
    low in color), 'color' for ones where color carries meaning (heatmaps, colormaps, photos). SVGs count as line art.
    Returns (tone, white fraction, saturated fraction)."""
    if path.suffix.lower() == ".svg":
        return "line", None, None
    from PIL import Image
    im = Image.open(path)
    if im.mode in ("RGBA", "LA", "P"):  # composite transparency onto white, as the page shows it
        im = im.convert("RGBA"); bg = Image.new("RGBA", im.size, "white"); bg.alpha_composite(im); im = bg
    im = im.convert("RGB"); im.thumbnail((256, 256))
    px = list(im.getdata())
    hsv = list(im.convert("HSV").getdata())
    white = sum(1 for r, g, b in px if min(r, g, b) > 235) / len(px)
    saturated = sum(1 for h, s, v in hsv if s > 90 and v > 60) / len(px)
    return ("line" if white > 0.55 and saturated < 0.06 else "color"), white, saturated  # tuned on 51 figures from two papers


def katex_css():
    """KaTeX stylesheet with its woff2 fonts as data URIs (the artifact CSP allows no other font host than Google Fonts)."""
    cache = CACHE / f"katex-{KATEX}-inline.css"
    if cache.exists():
        return cache.read_text()
    base = f"https://cdn.jsdelivr.net/npm/katex@{KATEX}/dist/"
    css = get(base + "katex.min.css").read().decode()
    def inline(m):
        if not m.group(1).endswith(".woff2"):
            return ""
        return f'url(data:font/woff2;base64,{base64.b64encode(get(base + m.group(1)).read()).decode()}) format("woff2")'
    css = re.sub(r'url\(([^)]+)\) format\("[a-z0-9]+"\)', inline, css)
    css = re.sub(r",\s*(?=[;}])", "", css)  # dangling commas left by the dropped woff/ttf sources
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(css)
    return css


def fill(**slots):
    """template.html with {{NAME}} / /*{{NAME}}*/ / <!--{{NAME}}--> slots replaced; unfilled slots become empty."""
    html = (SKILL / "template.html").read_text()
    slots.setdefault("KATEX_CSS", katex_css())
    for name, value in slots.items():
        for pat in (f"/*{{{{{name}}}}}*/", f"<!--{{{{{name}}}}}-->", f"{{{{{name}}}}}"):
            html = html.replace(pat, value)
    return re.sub(r"/\*\{\{[A-Z_]+\}\}\*/|<!--\{\{[A-Z_]+\}\}-->|\{\{[A-Z_]+\}\}", "", html)


def write_batches(out: Path, limit_bytes=58e6, limit_files=250):
    """Split out/'s supporting files into publish calls under the artifact host's limits (64 MB, 255 files per publish).
    index.html counts toward the first batch. Writes out/batches.json and returns the batches."""
    files = sorted(str(p.relative_to(out)) for p in out.rglob("*")
                   if p.is_file() and p.name not in ("index.html", "batches.json"))
    batches, size = [[]], (out / "index.html").stat().st_size
    for f in files:
        s = (out / f).stat().st_size
        if size + s > limit_bytes or len(batches[-1]) >= limit_files:
            batches.append([]); size = 0
        batches[-1].append(f); size += s
    (out / "batches.json").write_text(json.dumps(batches, indent=1))
    return batches
