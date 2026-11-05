"""Testes que mentem, jornada E2E e o React Compiler (capítulo 16).

uso: python3 medicoes/cap16.py [e2e|compilador|piramide]
  e2e: roda e2e/jornada.spec.ts (da tag cap16) contra a API cap15, com a
       tela cap16-antes e com a tela cap16. Pede PW_CHROMIUM se o
       Chromium instalado não for o do @playwright/test.
  compilador: na Ala B, com o Renderômetro também em volta do Resumo e do
       Detalhe (cap16-paineis.patch), digita "a" na busca, alterna a
       prioridade de Maria e seleciona João. cap16-antes não tem o
       compilador; cap16 tem.
  piramide: roda o Vitest da tag cap16 e agrupa testes e tempo por
       camada (o E2E está na saída de "e2e").
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from tela import WEB, api, rodada, sessao

QUAL = sys.argv[1] if len(sys.argv) > 1 else "e2e"
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def e2e(tag):
    pasta = Path(tempfile.mkdtemp(prefix=f"e2e-{tag}-"))
    subprocess.run(["git", "-C", str(WEB), "worktree", "add", "--detach",
                    str(pasta), tag], check=True, capture_output=True)
    (pasta / "node_modules").symlink_to(WEB / "node_modules")
    for arq in ("playwright.config.ts", "e2e/jornada.spec.ts"):
        destino = pasta / arq
        destino.parent.mkdir(exist_ok=True)
        destino.write_text(subprocess.run(
            ["git", "-C", str(WEB), "show", f"cap16:{arq}"],
            capture_output=True, text=True, check=True).stdout)
    try:
        r = subprocess.run(["npx", "playwright", "test", "--reporter=line"],
                           cwd=pasta, capture_output=True, text=True,
                           env={**os.environ, "CI": "1"})
        saida = ANSI.sub("", r.stdout + r.stderr).replace(str(pasta), "web")
        linhas = [l for l in saida.splitlines()
                  if l.strip() and "HydrateFallback" not in l
                  and not l.startswith("[WebServer]")]
        return "\n".join(linhas)
    finally:
        subprocess.run(["git", "-C", str(WEB), "worktree", "remove",
                        "--force", str(pasta)], capture_output=True)


if QUAL == "e2e":
    for tag in ("cap16-antes", "cap16"):
        with api("cap15"):
            print(f"== tela {tag} · API cap15 · e2e/jornada.spec.ts")
            print(e2e(tag))
            print()

if QUAL == "compilador":
    for tag in ("cap16-antes", "cap16"):
        with sessao(tag + "+cap16-paineis.patch") as (pg, versao):
            if tag == "cap16-antes":
                print(f"Chromium {versao} · modo dev")
            print(f"\n== {tag}"
                  + (" · React Compiler" if tag == "cap16" else ""))
            print(f"  {'ação':<21}cartões · painéis")
            total = 0
            for rotulo, acao in (
                    ('digitar "a"',
                     lambda: pg.get_by_label("Buscar paciente").type("a")),
                    ("prioridade de Maria",
                     lambda: pg.get_by_role("button", name="Prioridade")
                     .first.click()),
                    ("selecionar João",
                     lambda: pg.get_by_role("button", name="João Lima")
                     .click())):
                regs, _d = rodada(pg, rotulo, acao, mostrar=False)
                quem = [r.split(" · ")[0] for r in regs]
                cartoes = sum(q not in ("ResumoAla", "PainelDetalhe")
                              for q in quem)
                paineis = [q.replace("Ala", "").replace("Painel", "")
                           for q in quem
                           if q in ("ResumoAla", "PainelDetalhe")]
                total += len(quem)
                print(f"  {rotulo:<21}{cartoes}/6 · "
                      f"{', '.join(paineis) or 'nenhum'}")
            print(f"  renders no total: {total}")

CAMADAS = {"unidade, sem tela": ("assistente.test.ts", "tokens.test.ts"),
           "componente, rede à mão": ("Ala.test.tsx", "Busca.test.tsx",
                                      "LimiteDeErro.test.tsx",
                                      "Assistente.test.tsx"),
           "aplicação + MSW": ("rotas.test.tsx",)}

if QUAL == "piramide":
    pasta = Path(tempfile.mkdtemp(prefix="pir-"))
    subprocess.run(["git", "-C", str(WEB), "worktree", "add", "--detach",
                    str(pasta), "cap16"], check=True, capture_output=True)
    (pasta / "node_modules").symlink_to(WEB / "node_modules")
    try:
        subprocess.run(["npx", "vitest", "run", "--reporter=json",
                        "--outputFile=v.json"], cwd=pasta,
                       capture_output=True)
        d = json.loads((pasta / "v.json").read_text())
    finally:
        subprocess.run(["git", "-C", str(WEB), "worktree", "remove",
                        "--force", str(pasta)], capture_output=True)
    print("tag cap16 · Vitest 5 · jsdom")
    for camada, arquivos in CAMADAS.items():
        n = ms = 0
        for f in d["testResults"]:
            if Path(f["name"]).name in arquivos:
                n += len(f["assertionResults"])
                ms += sum(a.get("duration") or 0 for a in f["assertionResults"])
        print(f"  {camada:<24}{n:>3} testes {ms/1000:>6.2f} s")
