"""Exporta o notebook executado para HTML e PDF, e os documentos .md para PDF.

Uso:  python exportar.py [--pasta pasta_com_o_notebook_e_docs] [--so-docs]
Requer nbconvert e markdown (pip) e o Google Chrome instalado (impressão em PDF sem interface).
"""
import subprocess
import sys
from pathlib import Path

import markdown
from nbconvert import HTMLExporter

RAIZ = (Path(sys.argv[sys.argv.index("--pasta") + 1]) if "--pasta" in sys.argv else Path(__file__).parent.parent).resolve()
NOTEBOOK = RAIZ / "Quantum_Finance_ML_Segmentacao_de_Clientes.ipynb"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS_IMPRESSAO = """
<style>
@page { size: A4 landscape; margin: 11mm 10mm; }
@media print {
  body { font-size: 12.5px; }
  pre, .highlight pre, .jp-OutputArea-output pre { white-space: pre-wrap !important; word-break: break-word !important; font-size: 10px !important; }
  .jp-RenderedHTMLCommon table, table.dataframe { font-size: 10px !important; }
  img { max-width: 100% !important; height: auto !important; }
  .jp-InputPrompt, .jp-OutputPrompt { display: none !important; }
  h1, h2, h3 { break-after: avoid; }
  table, img { break-inside: avoid; }
}
</style>
"""

CSS_DOC = """
<style>
@page { size: A4; margin: 18mm 16mm; }
body { font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; font-size: 11.5pt; line-height: 1.5; color: #0b0b0b; max-width: 820px; margin: 0 auto; padding: 24px; }
h1 { font-size: 21pt; margin-bottom: 4px; } h2 { font-size: 15pt; margin-top: 28px; border-bottom: 1px solid #e6e5e1; padding-bottom: 4px; }
h3 { font-size: 12.5pt; margin-top: 20px; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 10pt; }
th, td { border: 1px solid #d9d8d3; padding: 6px 8px; text-align: left; vertical-align: top; }
th { background: #f3f2ee; }
code { background: #f3f2ee; padding: 1px 4px; border-radius: 3px; font-size: 10pt; }
pre code { display: block; padding: 10px; white-space: pre-wrap; }
blockquote { border-left: 3px solid #c9c8c3; margin-left: 0; padding-left: 14px; color: #52514e; }
h2, h3 { break-after: avoid; } tr { break-inside: avoid; }
</style>
"""


def imprimir_pdf(html: Path, pdf: Path):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=20000",
                    f"--print-to-pdf={pdf}", html.as_uri()], check=True, capture_output=True)
    print(f"{pdf.name}: {pdf.stat().st_size / 1e6:.1f} MB")


def exportar_notebook():
    corpo, _ = HTMLExporter().from_filename(str(NOTEBOOK))
    corpo = corpo.replace("</head>", CSS_IMPRESSAO + "</head>", 1)
    html = NOTEBOOK.with_suffix(".html")
    html.write_text(corpo, encoding="utf-8")
    print(f"{html.name}: {html.stat().st_size / 1e6:.1f} MB")
    imprimir_pdf(html, NOTEBOOK.with_suffix(".pdf"))


def exportar_documentos():
    for md in sorted((RAIZ / "docs").glob("*.md")):
        corpo = markdown.markdown(md.read_text(encoding="utf-8"), extensions=["tables", "fenced_code", "sane_lists"])
        titulo = md.stem.replace("_", " ")
        html = md.with_suffix(".html")
        html.write_text(f"<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><title>{titulo}</title>{CSS_DOC}</head>"
                        f"<body>{corpo}</body></html>", encoding="utf-8")
        imprimir_pdf(html, md.with_suffix(".pdf"))
        html.unlink()


if __name__ == "__main__":
    if "--so-docs" not in sys.argv:
        exportar_notebook()
    exportar_documentos()
