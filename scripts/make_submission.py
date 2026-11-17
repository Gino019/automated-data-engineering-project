from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
root = Path(__file__).resolve().parents[1]
text = (root / 'submission/links_template.txt').read_text(encoding='utf-8')
if 'REPLACE_WITH_' in text:
    raise SystemExit('Replace both Medium/video placeholders before generating the final submission ZIP.')
output = root / 'FlowForge_DE_submission_links.zip'
with ZipFile(output, 'w', ZIP_DEFLATED) as z:
    z.writestr('FlowForge_DE_links.txt', text)
print(output)
