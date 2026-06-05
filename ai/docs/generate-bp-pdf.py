#!/usr/bin/env python3
"""Generate branded PDF from the BC Best Practice Playbook."""

import re
import base64
from pathlib import Path
import markdown
from weasyprint import HTML

ROOT = Path("/Users/chris/PycharmProjects/chris-business-central")
MD_PATH = ROOT / "ai/reports/bc-best-practice-playbook.md"
DIAGRAM_DIR = ROOT / "ai/docs/diagrams/bp"
GFX_DIR = ROOT / "gfx"
OUT_PATH = ROOT / "ai/docs/bc-best-practice-playbook.pdf"

def img_to_data_uri(path):
    data = Path(path).read_bytes()
    b64 = base64.b64encode(data).decode()
    return f"data:image/png;base64,{b64}"

def load_logo():
    logo_path = GFX_DIR / "tentixo_wordmark_white.png"
    if logo_path.exists():
        return img_to_data_uri(logo_path)
    return ""

def convert_md_to_html(md_text):
    counter = [0]
    def replace_mermaid(match):
        counter[0] += 1
        img_path = DIAGRAM_DIR / f"bp-{counter[0]}.png"
        if img_path.exists():
            uri = img_to_data_uri(img_path)
            return f'<div class="diagram"><img src="{uri}" alt="Diagram {counter[0]}"></div>'
        return f'<p>[Diagram {counter[0]} not found]</p>'

    md_text = re.sub(r'```mermaid\n.*?```', replace_mermaid, md_text, flags=re.DOTALL)

    # Remove the YAML-style header block (Version/Status/etc) - we put it on cover
    md_text = re.sub(r'^# .*\n', '', md_text, count=1)
    md_text = re.sub(r'^\*\*Version\*\*:.*\n', '', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^\*\*Status\*\*:.*\n', '', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^\*\*Created\*\*:.*\n', '', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^\*\*Author\*\*:.*\n', '', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^\*\*Scope\*\*:.*\n', '', md_text, flags=re.MULTILINE)

    html = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
    return html

logo_uri = load_logo()
md_text = MD_PATH.read_text()
body_html = convert_md_to_html(md_text)

full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page {{
    size: A4;
    margin: 25mm 20mm 30mm 20mm;
    @bottom-center {{
        content: counter(page);
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        font-size: 8.5pt;
        font-weight: 600;
        color: #AAAAAA;
        letter-spacing: 2pt;
    }}
    @bottom-left {{
        content: "TENTIXO AB — CONFIDENTIAL";
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        font-size: 7pt;
        font-weight: 600;
        color: #AAAAAA;
        letter-spacing: 2pt;
    }}
}}

@page :first {{
    margin: 0;
    @bottom-center {{ content: none; }}
    @bottom-left {{ content: none; }}
}}

body {{
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 10pt;
    font-weight: 400;
    color: #333333;
    line-height: 1.55;
}}

/* --- COVER PAGE --- */
.cover {{
    page-break-after: always;
    width: 210mm;
    height: 297mm;
    position: relative;
    background: #00838F;
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 0;
    margin: 0;
}}

.cover-strip {{
    position: absolute;
    top: 0;
    right: 0;
    width: 50mm;
    height: 100%;
    background: #006D75;
}}

.cover-content {{
    position: relative;
    z-index: 1;
    padding: 60mm 30mm 40mm 30mm;
}}

.cover-logo {{
    margin-bottom: 20mm;
}}

.cover-logo img {{
    height: 18mm;
}}

.cover-title {{
    font-size: 38pt;
    font-weight: 300;
    color: #E0F7FA;
    line-height: 1.15;
    margin-bottom: 8mm;
}}

.cover-subtitle {{
    font-size: 14pt;
    font-weight: 400;
    color: #B2DFDB;
    margin-bottom: 15mm;
}}

.cover-meta {{
    margin-top: 30mm;
    font-size: 10pt;
    color: #B2EBF2;
}}

.cover-meta table {{
    border-collapse: collapse;
}}

.cover-meta td {{
    padding: 2mm 5mm 2mm 0;
    vertical-align: top;
    border: none !important;
    background: transparent !important;
}}

.cover-meta tr:nth-child(even) td {{
    background: transparent !important;
}}

.cover-meta .label {{
    color: #B2EBF2;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 8pt;
    letter-spacing: 1pt;
    width: 30mm;
}}

.cover-meta .value {{
    color: #E0F7FA;
}}

/* --- HEADINGS --- */
h2 {{
    font-size: 16pt;
    font-weight: 300;
    color: #1E3A45;
    border-bottom: 2px solid #00838F;
    padding-bottom: 3mm;
    margin-top: 12mm;
    margin-bottom: 5mm;
    page-break-after: avoid;
}}

h3 {{
    font-size: 11.5pt;
    font-weight: 700;
    color: #1E3A45;
    margin-top: 8mm;
    margin-bottom: 3mm;
    page-break-after: avoid;
}}

h4 {{
    font-size: 10pt;
    font-weight: 700;
    color: #00838F;
    margin-top: 5mm;
    margin-bottom: 2mm;
}}

/* --- BLOCKQUOTE (used for the intro callout) --- */
blockquote {{
    background: #F0F4F8;
    border-left: 4px solid #00838F;
    margin: 5mm 0;
    padding: 4mm 5mm;
    font-style: italic;
    color: #555555;
}}

blockquote p {{
    margin: 0;
}}

/* --- TABLES --- */
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 4mm 0 5mm 0;
    font-size: 9pt;
}}

th {{
    background: #1E3A45;
    color: #fff;
    font-weight: 600;
    text-align: left;
    padding: 2.5mm 3mm;
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 0.5pt;
}}

td {{
    padding: 2.5mm 3mm;
    border-bottom: 1px solid #E8E8E8;
    vertical-align: top;
}}

tr:nth-child(even) td {{
    background: #FAFBFC;
}}

/* --- CODE --- */
code {{
    background: #E0F2F1;
    color: #00695C;
    padding: 0.5mm 1.5mm;
    border-radius: 2px;
    font-size: 9pt;
    font-family: "SF Mono", Menlo, Consolas, monospace;
}}

pre {{
    background: #E0F2F1;
    padding: 4mm;
    border-radius: 3px;
    overflow-x: auto;
    font-size: 8.5pt;
    line-height: 1.5;
}}

pre code {{
    background: none;
    padding: 0;
}}

/* --- DIAGRAMS --- */
.diagram {{
    text-align: center;
    margin: 5mm 0;
    page-break-inside: avoid;
}}

.diagram img {{
    max-width: 100%;
    height: auto;
}}

/* --- LISTS --- */
ul, ol {{
    margin: 2mm 0 3mm 0;
    padding-left: 6mm;
}}

li {{
    margin-bottom: 1.5mm;
}}

/* --- HORIZONTAL RULE --- */
hr {{
    border: none;
    border-top: 1px solid #E8E8E8;
    margin: 8mm 0;
}}

/* --- STRONG --- */
strong {{
    color: #1E3A45;
}}

/* --- PAGE BREAKS --- */
h2 {{
    page-break-before: auto;
}}

/* Prevent orphaned headings */
h2, h3, h4 {{
    page-break-after: avoid;
}}

p, li, table {{
    page-break-inside: avoid;
}}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover">
    <div class="cover-strip"></div>
    <div class="cover-content">
        <div class="cover-logo">
            {"<img src='" + logo_uri + "'>" if logo_uri else ""}
        </div>
        <div class="cover-title">Business Central<br>Best Practice Playbook</div>
        <div class="cover-subtitle">Recommended patterns for setup, posting architecture,<br>and project management</div>
        <div class="cover-meta">
            <table>
                <tr><td class="label">Version</td><td class="value">0.1 — Draft</td></tr>
                <tr><td class="label">Date</td><td class="value">June 2026</td></tr>
                <tr><td class="label">Classification</td><td class="value">Client Document</td></tr>
                <tr><td class="label">Author</td><td class="value">Tentixo AB</td></tr>
            </table>
        </div>
    </div>
</div>

<!-- BODY -->
{body_html}

</body>
</html>
"""

HTML(string=full_html).write_pdf(str(OUT_PATH))
print(f"PDF generated: {OUT_PATH}")
print(f"Size: {OUT_PATH.stat().st_size / 1024:.0f} KB")
