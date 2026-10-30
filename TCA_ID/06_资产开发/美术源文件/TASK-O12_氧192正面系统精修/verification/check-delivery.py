"""Read-only checks against the original Aseprite project and actual reopened exports."""
from pathlib import Path
from PIL import Image
from collections import Counter
import hashlib
import json

root=Path(__file__).resolve().parents[1]
old_project=root.parent/'TASK-O11_氧正面_Aseprite忠实提取/oxygen-front-h192-refined-v002.aseprite'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(old_project)==sha(root/'backup/character_original.aseprite')
before=Image.open(root/'backup/character_before.png').convert('RGBA')
after=Image.open(root/'character_refined.png').convert('RGBA')
cli=Image.open(root/'verification/cli-reopened-final.png').convert('RGBA')
mcp=Image.open(root/'verification/mcp-reopened-final-v2.png').convert('RGBA')
preview=Image.open(root/'character_refined_4x.png').convert('RGBA')
twice=Image.open(root/'verification/character_refined_2x.png').convert('RGBA')
comp=Image.open(root/'character_before_after.png').convert('RGBA')
assert before.size==after.size==(104,208)
assert before.getchannel('A').tobytes()==after.getchannel('A').tobytes()
assert before.getbbox()==after.getbbox()==(8,8,96,200)
assert set(after.getchannel('A').get_flattened_data())=={0,255}
assert cli.tobytes()==mcp.tobytes()==after.tobytes()
assert preview.size==(416,832)
assert preview.tobytes()==after.resize((416,832),Image.Resampling.NEAREST).tobytes()
assert twice.size==(208,416)
assert twice.tobytes()==after.resize((208,416),Image.Resampling.NEAREST).tobytes()
assert comp.size==(864,832)
assert set(comp.getchannel('A').get_flattened_data())=={255}
for image,offset in [(before,0),(after,448)]:
    for y in range(image.height):
        for x in range(image.width):
            pixel=image.getpixel((x,y))
            if pixel[3]:
                assert comp.getpixel((offset+x*4,y*4))==pixel
layers=json.loads((root/'verification/layer-preservation.json').read_text())
engine=json.loads((root/'verification/final-engine-state.json').read_text())
assert layers['originalLayerNamesVisibilityLocksOpacityBlendAndPixelsUnchanged']
assert engine['layers']==8 and engine['frames']==1 and engine['paletteEntries']==46
color_count=lambda im: len(Counter(c for c in im.get_flattened_data() if c[3]))
result={
 'status':'passed','dimensions':[104,208],'subjectHeight':192,
 'transparentBackground':True,'alphaAndSilhouetteUnchanged':True,
 'originalProjectBackupSHA256':sha(old_project),'backupMatchesUnmodifiedSource':True,
 'originalThreeLayersPreservedExactly':True,'fiveEditableCorrectionLayers':True,
 'singleFrontFramePreserved':True,'originalFrameDurationMs':100,
 'beforeUsedOpaqueColors':color_count(before),'afterUsedOpaqueColors':color_count(after),
 'paletteEntries':46,'MCPAndCLIRereadExportPixelIdentical':True,
 'previewIsExactly4xNearest':True,'preview2xIsExactlyNearest':True,
 'comparisonLeftBeforeRightAfterSameDisplayScale':True,
 'visualReviewScales':[1,2,4,8],
 'visualReview':'Silhouette, asymmetry, hair streaks, hat, gems, white ruffles and floral arrangement retained. Rose masses separated with warm ivory against cool cloth. Black fabric uses long controlled fold planes rather than horizontal quantization bands. Hair and eye edits remain restrained. One front view only.',
 'limits':'Artistic acceptance is for the user. 192px cannot reproduce every fine chain or petal. No side/back pixels were present or added; no animation or engine validation.',
 'files':{p.name:sha(p) for p in [root/'character_refined.aseprite',root/'character_refined.png',root/'character_refined_4x.png',root/'character_before_after.png']}
}
(root/'verification/delivery-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:result[k] for k in ('status','dimensions','originalThreeLayersPreservedExactly','MCPAndCLIRereadExportPixelIdentical','afterUsedOpaqueColors')}))
