"""medir.py <pdf> : páginas por capítulo, contra o orçamento do plano."""
import re
import subprocess
import sys

ORC = {"Frente": 6, "01": 11, "02": 10, "03": 13, "04": 10, "05": 10,
       "06": 12, "07": 15, "08": 10, "09": 11, "10": 11, "11": 11,
       "12": 11, "13": 12, "14": 15, "15": 14, "16": 14, "17": 13,
       "18": 8, "19": 18, "20": 9}
TETO = 250

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
