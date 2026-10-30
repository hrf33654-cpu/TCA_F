"""Read-only pixel audit of the Aseprite deliverables."""
from pathlib import Path
from PIL import Image
from collections import Counter
import hashlib
import json

root = Path(__file__).resolve().parents[1]
metadata = json.loads((root / 'verification/extraction.json').read_text())
source = Image.open(root / 'references/oxygen-user-reference.png').convert('RGBA')
native = Image.open(root / 'exports/oxygen-front-original-resolution.png').convert('RGBA')
live = Image.open(root / 'verification/live-aseprite-export-v2.png').convert('RGBA')
small = Image.open(root / 'exports/oxygen-front-h192.png').convert('RGBA')
sx, sy = metadata['cropOrigin']
pixels = list(native.get_flattened_data())
rgb_mismatches = 0
for y in range(native.height):
    for x in range(native.width):
        p = native.getpixel((x, y))
        if p[3] and p[:3] != source.getpixel((sx+x, sy+y))[:3]:
            rgb_mismatches += 1
assert rgb_mismatches == 0
assert native.size == tuple(metadata['canvas'])
assert native.getbbox() == (24, 24, native.width-24, native.height-24)
assert set(Counter(p[3] for p in pixels)) == {0, 255}
assert sum(p[3] == 255 for p in pixels) == metadata['retainedPixels']
assert live.size == native.size and live.tobytes() == native.tobytes()
assert small.size == (104, 208) and small.getbbox() == (8, 8, 96, 200)
assert set(small.getchannel('A').get_flattened_data()) == {0, 255}
preview = Image.open(root / 'exports/oxygen-front-h192-preview4x.png').convert('RGBA')
assert preview.size == (416,832)
assert preview.tobytes() == small.resize((416,832), Image.Resampling.NEAREST).tobytes()
checker = Image.open(root / 'exports/oxygen-front-h192-preview4x-checker.png').convert('RGBA')
assert checker.size == (416,832)
assert set(checker.getchannel('A').get_flattened_data()) == {255}
for y in range(832):
    for x in range(416):
        p = small.getpixel((x//4,y//4))
        if p[3]:
            assert checker.getpixel((x,y)) == p
# Verify that the h192 edition is a direct nearest-neighbour sample of this reference,
# rather than the older O08 design or an independently generated character.
bw, bh = metadata['subjectBounds'][2:]
factor = 192 / bh
for y in range(192):
    for x in range(small.width-16):
        px = 24 + min(bw-1, int((x+0.5)/factor))
        py = 24 + min(bh-1, int((y+0.5)/factor))
        assert small.getpixel((x+8,y+8)) == native.getpixel((px,py))
files = [root / 'oxygen-front-faithful-v001.aseprite',
         root / 'oxygen-front-h192-v001.aseprite',
         *sorted((root / 'exports').glob('*.png'))]
result = {
    'status': 'passed',
    'source': str(root / 'references/oxygen-user-reference.png'),
    'nativeSize': native.size,
    'nativeSubjectHeight': bh,
    'nativeRetainedPixels': metadata['retainedPixels'],
    'nativeRetainedRGBMismatchCount': rgb_mismatches,
    'liveAsepriteExportEqualsNativePNG': True,
    'smallSize': small.size,
    'smallSubjectHeight': 192,
    'smallExactlyMatchesRecordedNearestSampling': True,
    'alphaValues': [0, 255],
    'visualReview': 'Reference front identity, facial details, hat, blue-white hair streaks, left cape, right floral ruffles and black skirt retained; heading and other views excluded. Background antialiasing comes from the supplied raster; no RGB recoloring or invented details.',
    'scope': 'Front static view only; user visual acceptance and engine/animation validation are separate.',
    'sha256': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
}
(root / 'verification/delivery-checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: result[k] for k in ('status','nativeSize','nativeRetainedRGBMismatchCount','liveAsepriteExportEqualsNativePNG','smallSubjectHeight')}))
