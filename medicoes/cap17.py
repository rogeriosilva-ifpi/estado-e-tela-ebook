"""Servidor, cliente e a fronteira (capítulo 17).

uso: python3 medicoes/cap17.py [chegada|hidratacao|fronteira]
  chegada: a ficha de Maria (/pacientes/p1), com Ana logada, servida pela
      SPA (web cap16, build de produção no vite preview :4173) e pelo
      Next (next cap17, next start :5174). Rede emulada de 4G lenta
      (150 ms de latência, 1,6 Mbps). Para cada uma: o CNS está no HTML?
      quanto JavaScript, quantos pedidos à API saem do navegador, e em
      quanto tempo o CNS aparece (mediana de 3 cargas sem cache).
  hidratacao: next cap17-antes e cap17, servidor em UTC e en-US, navegador
      em pt-BR e America/Fortaleza. Data no HTML, data na tela, erros.
  fronteira: next cap17 + cap17-cliente-importa-api.patch: o build.
Sobe a API cap15 aceitando as origens :4173 e :5174.
"""
import contextlib
import os
import re
import signal
import statistics
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright
from tela import WEB, api

# importado (por cap18.py), não mede nada
QUAL = (sys.argv[1] if len(sys.argv) > 1 else "chegada") \
    if __name__ == "__main__" else None
NEXT = Path(__file__).resolve().parents[2] / "next"
AQUI = Path(__file__).resolve().parent
ANSI = re.compile(r"\x1b\[[0-9;]*m")
ANA = ("ana@hospital.dev", "cajueiro-em-flor-no-quintal")
CNS = "898001234567890"
os.environ["CORS_ORIGINS"] = ("http://localhost:5173,http://localhost:4173,"
                              "http://localhost:5174")


@contextlib.contextmanager
def worktree(repo, tag, patch=None):
    if repo == NEXT:
        # o Turbopack recusa node_modules fora da raiz (link simbólico):
        # o Next é construído no próprio repositório, na tag pedida
        subprocess.run(["git", "checkout", "-q", "--detach", tag], cwd=repo,
                       check=True)
        if patch:
            subprocess.run(["git", "apply", str(AQUI / patch)], cwd=repo,
                           check=True)
        try:
            yield repo
        finally:
            subprocess.run(["git", "checkout", "-q", "."], cwd=repo)
            subprocess.run(["git", "checkout", "-q", "main"], cwd=repo)
        return
    pasta = Path(tempfile.mkdtemp(prefix=f"{repo.name}-{tag}-"))
    subprocess.run(["git", "-C", str(repo), "worktree", "add", "--detach",
                    str(pasta), tag], check=True, capture_output=True)
    (pasta / "node_modules").symlink_to(repo / "node_modules")
    if patch:
        subprocess.run(["git", "apply", str(AQUI / patch)], cwd=pasta,
                       check=True)
    try:
        yield pasta
    finally:
        subprocess.run(["git", "-C", str(repo), "worktree", "remove",
                        "--force", str(pasta)], capture_output=True)


@contextlib.contextmanager
def servidor(cmd, cwd, url, env=None):
    proc = subprocess.Popen(cmd, cwd=cwd, env={**os.environ, **(env or {})},
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            start_new_session=True)
    try:
        for _ in range(120):
            try:
                urllib.request.urlopen(url, timeout=1)
                break
            except OSError:
                time.sleep(0.25)
        yield
    finally:
        os.killpg(proc.pid, signal.SIGTERM)   # npx deixa o next-server vivo
        proc.wait(timeout=10)


def construir(pasta, cmd, env=None):
    r = subprocess.run(cmd, cwd=pasta, capture_output=True, text=True,
                       env={**os.environ, **(env or {})})
    return r.returncode, ANSI.sub("", r.stdout + r.stderr)


def entrar(pg, base):
    pg.goto(base + "/entrar")
    pg.get_by_label("E-mail").fill(ANA[0])
    pg.get_by_label("Senha").fill(ANA[1])
    pg.get_by_role("button", name="Entrar").click()
    pg.wait_for_timeout(1200)


def carga(pg, cdp, url):
    cdp.send("Network.clearBrowserCache")
    pedidos = []
    ouvir = lambda r: pedidos.append(r.url)  # noqa: E731
    pg.on("request", ouvir)
    resp = pg.goto(url, wait_until="commit")
    pg.get_by_text(CNS, exact=True).wait_for()
    ms = pg.evaluate("performance.now()")
    pg.wait_for_load_state("networkidle")
    pg.remove_listener("request", ouvir)
    js = pg.evaluate("""() => performance.getEntriesByType("resource")
      .filter(e => e.name.endsWith(".js") || e.initiatorType === "script")
      .map(e => [e.decodedBodySize, e.transferSize])""")
    return {"html": CNS in resp.text(), "ms": ms, "js": js,
            "api": sorted({re.sub(r"\?.*", "", u.split("/api/")[1])
                           for u in pedidos if "/api/" in u})}


def medir(nome, base):
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(locale="pt-BR", timezone_id="America/Fortaleza")
        pg = ctx.new_page()
        entrar(pg, base)
        cdp = ctx.new_cdp_session(pg)
        cdp.send("Network.enable")
        cdp.send("Network.emulateNetworkConditions", {
            "offline": False, "latency": 150,
            "downloadThroughput": 1.6e6 / 8, "uploadThroughput": 750e3 / 8})
        cargas = [carga(pg, cdp, base + "/pacientes/p1") for _ in range(3)]
        c = cargas[-1]
        print(f"{nome}")
        print(f"  CNS no HTML recebido: {'sim' if c['html'] else 'não'}")
        bruto = sum(x[0] for x in c["js"]) / 1000
        rede = sum(x[1] for x in c["js"]) / 1000
        print(f"  JavaScript: {len(c['js'])} arquivo(s), {bruto:.0f} kB;"
              f" {rede:.0f} kB pela rede")
        print(f"  pedidos do navegador à API: "
              f"{', '.join(c['api']) or 'nenhum'}")
        ms = statistics.median(x["ms"] for x in cargas)
        print(f"  CNS na tela em {ms:.0f} ms (mediana de 3)")
        b.close()


if QUAL == "chegada":
    print("Chromium 141 · 4G lenta emulada: 150 ms, 1,6 Mbps")
    with api("cap15"):
        with worktree(WEB, "cap16") as pasta:
            construir(pasta, ["node", "node_modules/vite/bin/vite.js", "build"])
            with servidor(["node", "node_modules/vite/bin/vite.js", "preview",
                           "--port", "4173", "--strictPort"], pasta,
                          "http://localhost:4173"):
                medir("SPA · web cap16 · vite preview", "http://localhost:4173")
        with worktree(NEXT, "cap17") as pasta:
            construir(pasta, ["npx", "next", "build"])
            with servidor(["npx", "next", "start", "-p", "5174"], pasta,
                          "http://localhost:5174"):
                medir("Next · next cap17 · next start", "http://localhost:5174")

if QUAL == "hidratacao":
    print("servidor: TZ=UTC, LANG=en_US.UTF-8 · navegador: pt-BR, "
          "America/Fortaleza")
    print("cadastro de Maria: nascimento 1958-03-14")
    env = {"TZ": "UTC", "LANG": "en_US.UTF-8"}
    with api("cap15"):
        for tag in ("cap17-antes", "cap17"):
            with worktree(NEXT, tag) as pasta:
                construir(pasta, ["npx", "next", "build"], env)
                with servidor(["npx", "next", "start", "-p", "5174"], pasta,
                              "http://localhost:5174", env), \
                        sync_playwright() as p:
                    b = p.chromium.launch()
                    ctx = b.new_context(locale="pt-BR",
                                        timezone_id="America/Fortaleza")
                    pg = ctx.new_page()
                    entrar(pg, "http://localhost:5174")
                    erros = []
                    pg.on("pageerror", lambda e: erros.append(str(e)))
                    resp = pg.goto("http://localhost:5174/pacientes/p1")
                    pg.get_by_text(CNS, exact=True).wait_for()
                    pg.wait_for_timeout(1000)
                    html = re.search(r"<dt>Nascimento</dt><dd>([^<]*)</dd>",
                                     resp.text())
                    tela = pg.locator("dt", has_text="Nascimento").locator("xpath=following-sibling::dd[1]").inner_text()
                    print(f"\nnext {tag}")
                    print(f"  no HTML do servidor: {html.group(1) if html else '?'}")
                    print(f"  na tela, depois de hidratar: {tela}")
                    for e in erros:
                        print(f"  erro: {e.split(';')[0]}")
                    if not erros:
                        print("  erros: nenhum")
                    b.close()

if QUAL == "fronteira":
    with worktree(NEXT, "cap17", "cap17-cliente-importa-api.patch") as pasta:
        cod, saida = construir(pasta, ["npx", "next", "build"])
        print("next cap17 + CopiarCns importando lib/api.ts")
        print(f"$ next build   (código de saída {cod})")
        linhas = [l for l in saida.splitlines()
                  if re.search(r"Error|server-only|Client Component|"
                               r"import \"server", l)]
        print("\n".join(dict.fromkeys(linhas)))
