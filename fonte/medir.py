"""medir.py <pdf> : páginas por capítulo, contra o orçamento do plano."""
import re
import subprocess
import sys

ORC = {"Frente": 6, "01": 8, "02": 7, "03": 11, "04": 8, "05": 8, "06": 10,
       "07": 13, "08": 8, "09": 9, "10": 9, "11": 9, "12": 9, "13": 10,
       "14": 13, "15": 12, "16": 12, "17": 11, "18": 7, "19": 16, "20": 8}
TETO = 220

txt = subprocess.run(["pdftotext", "-layout", sys.argv[1], "-"],
                     capture_output=True, text=True).stdout
paginas = txt.split("\f")
if not paginas[-1].strip():
    paginas = paginas[:-1]
inicio = {}
for i, p in enumerate(paginas):
    topo = re.sub(r"\s", "", p[:300]).upper()
    m = re.search(r"^\s*(0[0-9]|1[0-9]|20)\s*$", p[:500], re.M)
    marca = "PARTE" in topo or "ANTESDECOMEÇAR" in topo
    if m and marca and m.group(1) not in inicio and i > 1:
        inicio[m.group(1)] = i
caps = sorted(inicio.items(), key=lambda kv: kv[1])
limites = [("Frente", 0)] + [c for c in caps if c[0] != "00"] + [("fim", len(paginas))]
total = orc = 0
for (nome, ini), (_, prox) in zip(limites, limites[1:]):
    n = prox - ini
    o = ORC.get(nome, 0)
    total, orc = total + n, orc + o
    marca = "OK" if n <= o else f"ESTOURO +{n - o}"
    print(f"{nome:<7}{n:>4} p   orçamento {o:>3}   {marca}")
print(f"total  {total:>4} p   orçamento {orc:>3}   teto do livro {TETO}")
if "--json" in sys.argv:
    import json
    from pathlib import Path
    destino = Path(__file__).resolve().parent.parent / "saidas" / "paginas.json"
    destino.write_text(json.dumps({k: v + 1 for k, v in inicio.items()}))
