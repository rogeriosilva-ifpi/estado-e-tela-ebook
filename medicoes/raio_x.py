"""raio-x do bundle: o que cada tag entrega ao navegador.

uso: python3 medicoes/raio_x.py TAG [TAG...]
Para cada tag, faz o build do Vite três vezes num worktree e mostra cada
arquivo JavaScript de dist/assets (bytes e gzip) e a mediana do tempo de
build. O nome do arquivo perde o hash.
"""
import gzip
import re
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from tela import WEB

for tag in sys.argv[1:]:
    pasta = Path(tempfile.mkdtemp(prefix=f"raio-{tag}-"))
    subprocess.run(["git", "-C", str(WEB), "worktree", "add", "--detach",
                    str(pasta), tag], check=True, capture_output=True)
    (pasta / "node_modules").symlink_to(WEB / "node_modules")
    try:
        tempos = []
        for _ in range(3):
            t0 = time.perf_counter()
            subprocess.run(["node", str(WEB / "node_modules/vite/bin/vite.js"),
                            "build"], cwd=pasta, check=True,
                           capture_output=True)
            tempos.append(time.perf_counter() - t0)
        print(f"== {tag} · build em {statistics.median(tempos):.1f} s"
              " (mediana de 3)")
        total = [0, 0]
        for js in sorted((pasta / "dist/assets").glob("*.js")):
            bruto = js.read_bytes()
            gz = len(gzip.compress(bruto, 9))
            nome = re.sub(r"-[\w-]{8}\.js$", ".js", js.name)
            total[0] += len(bruto)
            total[1] += gz
            print(f"  {nome:<16}{len(bruto)/1000:>8.1f} kB{gz/1000:>8.1f} kB gzip")
        print(f"  {'total':<16}{total[0]/1000:>8.1f} kB{total[1]/1000:>8.1f} kB gzip")
    finally:
        subprocess.run(["git", "-C", str(WEB), "worktree", "remove",
                        "--force", str(pasta)], capture_output=True)
