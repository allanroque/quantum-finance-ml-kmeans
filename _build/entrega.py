"""Monta a versão de entrega, com identificação, fora do repositório, e gera o zip.

Uso:  python entrega.py <pasta_de_execucao> <arquivo_de_identificacao.json> <pasta_de_entrega>

O arquivo de identificação fica fora do repositório. Chaves: "capa" e "referencia_disciplina"
(usadas no notebook) e "readme" (substitui a frase genérica de abertura do README).
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
REPOSITORIO = RAIZ.parent
FRASE_PUBLICA = "Trabalho final de uma disciplina de Machine Learning em nível de pós-graduação."
NOTA_PUBLICA_INICIO = "Este repositório traz a versão pública do trabalho"

if __name__ == "__main__":
    pasta_exec, identificacao, entrega = (Path(a).resolve() for a in sys.argv[1:4])
    textos = json.loads(identificacao.read_text(encoding="utf-8"))
    if entrega.exists():
        shutil.rmtree(entrega)
    (entrega / "docs").mkdir(parents=True)

    subprocess.run([sys.executable, str(RAIZ / "build.py"), str(pasta_exec), "--identificacao", str(identificacao),
                    "--saida", str(entrega)], check=True)

    readme = (REPOSITORIO / "README.md").read_text(encoding="utf-8")
    assert readme.count(FRASE_PUBLICA) == 1
    readme = readme.replace(FRASE_PUBLICA, textos["readme"])
    readme = "\n".join(l for l in readme.split("\n") if not l.startswith(NOTA_PUBLICA_INICIO)).rstrip() + "\n"
    (entrega / "README.md").write_text(readme, encoding="utf-8")
    shutil.copy(REPOSITORIO / "requirements.txt", entrega)
    for md in (REPOSITORIO / "docs").glob("*.md"):
        shutil.copy(md, entrega / "docs")
    (entrega / "saidas").mkdir()
    for nome in ["segmentos_clientes.csv", "perfil_dos_segmentos.csv", "manifesto_modelo.json"]:
        shutil.copy(pasta_exec / "saidas" / nome, entrega / "saidas")

    subprocess.run([sys.executable, str(RAIZ / "exportar.py"), "--pasta", str(entrega)], check=True)
    pacote = shutil.make_archive(str(entrega.parent / "Quantum_Finance_ML_Trabalho_Final"), "zip", root_dir=entrega)
    print("Pacote de entrega:", pacote)
