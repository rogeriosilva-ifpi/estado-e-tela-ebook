"""CSS Modules × Tailwind na mesma tela (capítulo 9).

uso: python3 medicoes/cap09.py   (antes: cd medicoes && npm install)
Compara as tags cap09 (tokens + CSS Modules) e cap09-tailwind (tokens +
Tailwind 4.3 sem preflight): CSS do build, linhas de estilo do cartão e
do selo, a classe que chega ao DOM e o axe nos dois temas.
"""
import gzip
import subprocess
import tempfile
from pathlib import Path
from tela import WEB, sessao
from vigia_a11y import axe

ARQS = ["src/features/pacientes/CartaoPaciente.tsx",
        "src/features/pacientes/CartaoPaciente.module.css",
        "src/features/pacientes/SeloRisco.tsx",
        "src/features/pacientes/SeloRisco.module.css"]


def preparar(tag):
    pasta = Path(tempfile.mkdtemp(prefix=f"build-{tag}-"))
    subprocess.run(["git", "-C", str(WEB), "worktree", "add", "--detach",
                    str(pasta), tag], check=True, capture_output=True)
    subprocess.run(["npm", "ci", "--silent"], cwd=pasta, check=True)
    subprocess.run(["npx", "vite", "build", "--logLevel", "silent"],
                   cwd=pasta, check=True)
    return pasta


for tag in ("cap09", "cap09-tailwind"):
    pasta = preparar(tag)
    try:
        css = next((pasta / "dist/assets").glob("*.css")).read_bytes()
        linhas = sum(len((pasta / a).read_text().splitlines())
                     for a in ARQS if (pasta / a).exists())
        print(f"\ntela {tag}")
        print(f"  CSS do build: {len(css)} bytes, "
              f"{len(gzip.compress(css, 9))} com gzip")
        print(f"  cartão + selo: {linhas} linhas, "
              f"{sum((pasta / a).exists() for a in ARQS)} arquivos")
        with sessao(tag, modulos=pasta / "node_modules") as (pg, _v):
            classe = pg.locator("li").first.get_attribute("class")
            print(f"  classe no DOM: {' '.join(classe.split())[:44]}")
            for tema in ("light", "dark"):
                axe(pg, tema)
    finally:
        subprocess.run(["git", "-C", str(WEB), "worktree", "remove",
                        "--force", str(pasta)], capture_output=True)
