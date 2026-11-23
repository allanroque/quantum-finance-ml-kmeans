"""Monta o notebook a partir de _build/src/*.src, executa e grava o resultado.

Uso:  python build.py <pasta_de_execucao> [--identificacao arquivo.json] [--saida pasta] [--sem-executar]

A pasta de execução recebe data/ (download e cache) e saidas/; fica fora do repositório.
Cada arquivo .src alterna blocos iniciados por uma linha '#%% md' ou '#%% code'.

Sem --identificacao, o notebook sai na versão pública: sem instituição, professor e integrantes.
Com --identificacao, esses textos vêm de um arquivo JSON mantido fora do repositório, com as
chaves "capa" e "referencia_disciplina" (e "readme", usada por entrega.py).
"""
import json
import re
import sys
import time
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

RAIZ = Path(__file__).resolve().parent
REPOSITORIO = RAIZ.parent
NOME = "Quantum_Finance_ML_Segmentacao_de_Clientes.ipynb"
EMPRESA = "Quantum Finance"
PUBLICO = {
    "capa": "**Trabalho final** de uma disciplina de Machine Learning em nível de pós-graduação",
    "referencia_disciplina": "* Slides e notebooks das Aulas 1 a 4 da disciplina.",
}


def argumento(nome):
    return sys.argv[sys.argv.index(nome) + 1] if nome in sys.argv else None


def ler_celulas(textos):
    trocas = {"{{EMPRESA}}": EMPRESA, "{{CAPA_IDENTIFICACAO}}": textos["capa"],
              "{{REFERENCIA_DISCIPLINA}}": textos["referencia_disciplina"]}
    celulas = []
    for arq in sorted((RAIZ / "src").glob("*.src")):
        tipo, buf = None, []
        for linha in arq.read_text(encoding="utf-8").splitlines():
            m = re.fullmatch(r"#%% (md|code)\s*", linha)
            if m:
                if tipo:
                    celulas.append((tipo, "\n".join(buf).strip("\n")))
                tipo, buf = m.group(1), []
            else:
                buf.append(linha)
        if tipo:
            celulas.append((tipo, "\n".join(buf).strip("\n")))
    saida = []
    for tipo, fonte in celulas:
        for marca, valor in trocas.items():
            fonte = fonte.replace(marca, valor)
        assert "{{" not in fonte, f"marcador sem valor: {fonte[:80]}"
        if fonte.strip():
            saida.append((tipo, fonte))
    return saida


def montar(textos):
    nb = new_notebook()
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
        "colab": {"provenance": [], "toc_visible": True},
    }
    for i, (tipo, fonte) in enumerate(ler_celulas(textos)):
        cel = new_markdown_cell(fonte) if tipo == "md" else new_code_cell(fonte)
        cel["id"] = f"c{i:03d}"
        nb.cells.append(cel)
    return nb


if __name__ == "__main__":
    pasta_exec = Path(sys.argv[1]).resolve()
    pasta_exec.mkdir(parents=True, exist_ok=True)
    textos = dict(PUBLICO)
    if argumento("--identificacao"):
        textos.update(json.loads(Path(argumento("--identificacao")).read_text(encoding="utf-8")))
    destino = Path(argumento("--saida")).resolve() if argumento("--saida") else REPOSITORIO
    nb = montar(textos)
    if "--sem-executar" not in sys.argv:
        from nbclient import NotebookClient

        t0 = time.time()
        NotebookClient(nb, timeout=1800, kernel_name="python3",
                       resources={"metadata": {"path": str(pasta_exec)}}).execute()
        print(f"Executado em {time.time() - t0:.0f} s")
    destino.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, destino / NOME)
    n_code = sum(c.cell_type == "code" for c in nb.cells)
    versao = "com identificação" if argumento("--identificacao") else "pública"
    print(f"{len(nb.cells)} células ({n_code} de código), versão {versao} -> {destino / NOME}")
