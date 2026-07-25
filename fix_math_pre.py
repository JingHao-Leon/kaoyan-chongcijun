from pathlib import Path

p = Path(__file__).resolve().parent / "math1.html"
s = p.read_text(encoding="utf-8")
s = s.replace('<p><pre style="white-space:pre-wrap;margin:0;background:#fafbfe;padding:12px;border-radius:8px">', '<pre style="white-space:pre-wrap;margin:0;background:#fafbfe;padding:12px;border-radius:8px">')
s = s.replace('</pre></p><p><a href="../../11408_zhenti/shuxue1/shuxue1_2024.pdf"', '</pre><p><a href="../../11408_zhenti/shuxue1/shuxue1_2024.pdf"')
p.write_text(s, encoding="utf-8")
print('fixed original question markup')
