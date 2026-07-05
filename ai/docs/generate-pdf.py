#!/usr/bin/env python3
"""Generate branded Tentixo PDFs from markdown playbooks.

Usage:
    python3 ai/docs/generate-pdf.py client     # client-facing best practice playbook
    python3 ai/docs/generate-pdf.py internal    # internal Tentixo playbook
    python3 ai/docs/generate-pdf.py all         # both
"""

import re
import sys
import base64
from pathlib import Path
import markdown
from weasyprint import HTML

ROOT = Path("/Users/chris/PycharmProjects/chris-business-central")
GFX_DIR = ROOT / "gfx"

CONFIGS = {
    "client": {
        "md": ROOT / "ai/reports/bc-best-practice-playbook.md",
        "diagrams": ROOT / "ai/docs/diagrams/bp",
        "diagram_prefix": "bp",
        "out": ROOT / "ai/docs/bc-best-practice-playbook.pdf",
        "cover_bg": "#00838F",
        "cover_strip": "#006D75",
        "cover_title": "Business Central<br>Best Practice Playbook",
        "cover_subtitle": "Recommended patterns for setup, posting architecture,<br>and project management",
        "meta": [
            ("Version", "0.1 — Draft"),
            ("Date", "June 2026"),
            ("Classification", "Client Document"),
            ("Author", "Tentixo AB"),
        ],
        "footer_text": "TENTIXO AB — CONFIDENTIAL",
    },
    "internal": {
        "md": ROOT / "ai/reports/business-central-playbook.md",
        "diagrams": ROOT / "ai/docs/diagrams",
        "diagram_prefix": "diagram",
        "out": ROOT / "ai/docs/business-central-playbook.pdf",
        "cover_bg": "#1E3A45",
        "cover_strip": "#00838F",
        "cover_title": "Business Central<br>Tentixo Playbook",
        "cover_subtitle": "Architecture, operations, bookkeeping,<br>and client engagement reference",
        "meta": [
            ("Version", "1.1"),
            ("Updated", "June 2026"),
            ("Classification", "Internal"),
            ("Author", "Chris Mansson / Tentixo AB"),
        ],
        "footer_text": "TENTIXO AB — INTERNAL",
    },
    "morre": {
        "md": ROOT / "ai/reports/bc-progress-summary-for-morre_v1.0.md",
        "diagrams": ROOT / "ai/docs/diagrams",
        "diagram_prefix": "diagram",
        "out": ROOT / "ai/docs/bc-progress-summary-for-morre.pdf",
        "cover_bg": "#1E3A45",
        "cover_strip": "#00838F",
        "cover_title": "Business Central<br>Progress Update",
        "cover_subtitle": "Gap analysis and next steps<br>— prepared for Morre",
        "meta": [
            ("Version", "1.0"),
            ("Date", "July 2026"),
            ("Classification", "Internal"),
            ("Author", "Chris Mansson / Tentixo AB"),
        ],
        "footer_text": "TENTIXO AB — INTERNAL",
    },
}


def img_to_data_uri(path):
    data = Path(path).read_bytes()
    b64 = base64.b64encode(data).decode()
    return f"data:image/png;base64,{b64}"


def load_logo():
    logo_path = GFX_DIR / "tentixo_wordmark_white.png"
    if logo_path.exists():
        return img_to_data_uri(logo_path)
    return ""


def convert_md_to_html(md_text, diagram_dir, diagram_prefix):
    counter = [0]

    def replace_mermaid(match):
        counter[0] += 1
        img_path = diagram_dir / f"{diagram_prefix}-{counter[0]}.png"
        if img_path.exists():
            uri = img_to_data_uri(img_path)
            return f'<div class="diagram"><img src="{uri}" alt="Diagram {counter[0]}"></div>'
        return f'<p>[Diagram {counter[0]} not found]</p>'

    md_text = re.sub(r'```mermaid\n.*?```', replace_mermaid, md_text, flags=re.DOTALL)

    # Remove the title and metadata block — we put it on cover
    md_text = re.sub(r'^# .*\n', '', md_text, count=1)
    for field in ['Version', 'Status', 'Created', 'Updated', 'Author', 'Scope']:
        md_text = re.sub(rf'^\*\*{field}\*\*:.*\n', '', md_text, flags=re.MULTILINE)

    html = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])

    # Convert <!-- page-break --> markers to CSS page breaks
    html = html.replace('<!-- page-break -->', '<div style="page-break-before: always;"></div>')

    return html


def generate_pdf(config_name):
    cfg = CONFIGS[config_name]
    logo_uri = load_logo()
    md_text = cfg["md"].read_text()
    body_html = convert_md_to_html(md_text, cfg["diagrams"], cfg["diagram_prefix"])

    meta_rows = "\n".join(
        f'<tr><td class="label">{k}</td><td class="value">{v}</td></tr>'
        for k, v in cfg["meta"]
    )

    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page {{
    size: A4;
    margin: 25mm 20mm 25mm 20mm;
    @bottom-center {{
        content: counter(page);
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        font-size: 8.5pt;
        font-weight: 600;
        color: #AAAAAA;
        letter-spacing: 2pt;
    }}
    @bottom-left {{
        content: "{cfg['footer_text']}";
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
    background: {cfg['cover_bg']};
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
    background: {cfg['cover_strip']};
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
    color: #8EE1EC;
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
    margin-top: 10mm;
    margin-bottom: 4mm;
}}

h3 {{
    font-size: 11.5pt;
    font-weight: 700;
    color: #1E3A45;
    margin-top: 6mm;
    margin-bottom: 2mm;
}}

h4 {{
    font-size: 10pt;
    font-weight: 700;
    color: #00838F;
    margin-top: 4mm;
    margin-bottom: 2mm;
}}

/* --- BLOCKQUOTE --- */
blockquote {{
    background: #F0F4F8;
    border-left: 4px solid #00838F;
    margin: 4mm 0;
    padding: 3mm 5mm;
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
    margin: 3mm 0 4mm 0;
    font-size: 9pt;
}}

th {{
    background: #1E3A45;
    color: #fff;
    font-weight: 600;
    text-align: left;
    padding: 2mm 3mm;
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 0.5pt;
}}

td {{
    padding: 2mm 3mm;
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
    padding: 3mm;
    border-radius: 3px;
    overflow-x: auto;
    font-size: 8.5pt;
    line-height: 1.4;
}}

pre code {{
    background: none;
    padding: 0;
}}

/* --- DIAGRAMS --- */
.diagram {{
    text-align: center;
    margin: 3mm 0;
}}

.diagram img {{
    max-width: 100%;
    max-height: 180mm;
    height: auto;
}}

/* --- LISTS --- */
ul, ol {{
    margin: 2mm 0 2mm 0;
    padding-left: 6mm;
}}

li {{
    margin-bottom: 1mm;
}}

/* --- HORIZONTAL RULE --- */
hr {{
    border: none;
    border-top: 1px solid #E8E8E8;
    margin: 5mm 0;
}}

/* --- STRONG --- */
strong {{
    color: #1E3A45;
}}

/* --- PAGE BREAK CONTROL --- */
h2 {{
    page-break-after: avoid;
    page-break-before: auto;
}}

h3, h4 {{
    page-break-after: avoid;
}}

/* Headings must keep at least 5 lines of content with them */
h2 + *, h3 + *, h4 + * {{
    page-break-before: avoid;
}}

/* Allow tables and diagrams to break across pages if needed */
table {{
    page-break-inside: auto;
}}

tr {{
    page-break-inside: avoid;
}}

.diagram {{
    page-break-inside: avoid;
}}

/* Keep paragraphs together only if short */
p {{
    orphans: 3;
    widows: 3;
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
        <div class="cover-title">{cfg['cover_title']}</div>
        <div class="cover-subtitle">{cfg['cover_subtitle']}</div>
        <div class="cover-meta">
            <table>
                {meta_rows}
            </table>
        </div>
    </div>
</div>

<!-- BODY -->
{body_html}

</body>
</html>
"""

    HTML(string=full_html).write_pdf(str(cfg["out"]))
    print(f"  {config_name}: {cfg['out'].name} ({cfg['out'].stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["all"]

    if "all" in targets:
        targets = ["client", "internal"]

    logo_uri = load_logo()
    for t in targets:
        if t not in CONFIGS:
            print(f"Unknown target: {t}. Use: client, internal, all")
            sys.exit(1)

    print("Generating PDFs...")
    for t in targets:
        generate_pdf(t)
    print("Done.")
