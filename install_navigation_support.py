from pathlib import Path

ROOT = Path(__file__).resolve().parent
TAG = '<script defer src="assets/navigation.js"></script>'

for path in ROOT.glob('*.html'):
    text = path.read_text(encoding='utf-8')
    if TAG in text:
        continue
    if '</head>' not in text:
        raise SystemExit(f'{path.name}: missing </head>')
    path.write_text(text.replace('</head>', TAG + '</head>', 1), encoding='utf-8')
    print(f'updated {path.name}')

COURSE_PAGES = ('math1.html', 'english1.html', 'ds.html', 'co.html', 'os.html', 'cn.html')
COURSE_TAGS = (
    '<script defer src="assets/chapter-mode.js"></script>',
    '<script defer src="assets/interactive-labs.js"></script>',
)

for filename in COURSE_PAGES:
    path = ROOT / filename
    text = path.read_text(encoding='utf-8')
    missing = ''.join(tag for tag in COURSE_TAGS if tag not in text)
    if missing:
        path.write_text(text.replace('</head>', missing + '</head>', 1), encoding='utf-8')
        print(f'added chapter features to {filename}')
