from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
PDF_ROOT = ROOT.parent / "11408_zhenti" / "shuxue1"
TXT_ROOT = ROOT / "tmp" / "pdfs" / "math1"
OUT_ROOT = ROOT / "website" / "images" / "math_papers"

def pages_for(year):
    path = TXT_ROOT / f"shuxue1_{year}.txt"
    if not path.exists(): return set()
    raw = path.read_text(encoding="utf-8", errors="ignore")
    matches = list(re.finditer(r"(?:【(\d+)】|\n\s*\(?([1-9]|1[0-9]|2[0-2])[】)、.．])", raw))
    pages = set()
    for m in matches:
        n = int(m.group(1) or m.group(2))
        if n <= 22:
            pages.add(raw[:m.start()].count("\f") + 1)
    return pages

count = 0
for year in range(2014, 2025):
    pdf = PDF_ROOT / f"shuxue1_{year}.pdf"
    if not pdf.exists():
        continue
    out = OUT_ROOT / str(year)
    out.mkdir(parents=True, exist_ok=True)
    for page in sorted(pages_for(year)):
        target = out / f"page-{page}.png"
        if target.exists():
            continue
        subprocess.run(["pdftoppm", "-png", "-r", "140", "-f", str(page), "-l", str(page), str(pdf), str(out / "page")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        count += 1
print(f"rendered {count} source pages")
