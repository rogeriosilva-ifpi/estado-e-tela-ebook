"""Sobe a tela de uma tag do repositório web e entrega uma página do Chromium.

uso em roteiros:
    from tela import sessao
    with sessao("cap04-antes") as (pg, versao):
        ...

Cria um git worktree temporário da tag, reaproveita o node_modules do
repositório principal, sobe o Vite numa porta livre e encerra o processo
pelo PID no fim. A API não é necessária para os capítulos 3 a 6.
"""
import contextlib
import os
import socket
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

WEB = Path(os.environ.get("ESTADO_WEB",
                          Path(__file__).resolve().parents[2] / "web"))

OBSERVADOR = """() => {
  window.dom = { entram: 0, saem: 0, trocas: 0 };
  const conta = (ns) => [...ns].filter((n) => n.nodeType === 1)
    .reduce((t, n) => t + 1 + n.querySelectorAll("*").length, 0);
  new MutationObserver((lista) => {
    const antes = new Map();
    for (const r of lista) {
      dom.entram += conta(r.addedNodes);
      dom.saem += conta(r.removedNodes);
      if (r.type === "characterData") dom.trocas++;
      if (r.type === "childList" && r.addedNodes.length &&
          [...r.addedNodes, ...r.removedNodes]
            .every((n) => n.nodeType === 3)) dom.trocas++;
      if (r.type !== "attributes") continue;
      if (!antes.has(r.target)) antes.set(r.target, new Map());
      const at = antes.get(r.target);
      if (!at.has(r.attributeName)) at.set(r.attributeName, r.oldValue);
    }
    for (const [no, at] of antes) {
      for (const [nome, velho] of at) {
        if (no.getAttribute(nome) !== velho) dom.trocas++;
      }
    }
  }).observe(document.querySelector("main"), { childList: true,
    subtree: true, characterData: true, attributes: true,
    attributeOldValue: true });
}"""


def _porta_livre():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@contextlib.contextmanager
def sessao(tag, porta=None, modulos=None):
    """tag pode ser "tag+arquivo.patch": aplica o patch (de medicoes/).
    modulos: outro node_modules (tag com dependências próprias)."""
    tag, _, patch = tag.partition("+")
    pasta = Path(tempfile.mkdtemp(prefix=f"tela-{tag}-"))
    subprocess.run(["git", "-C", str(WEB), "worktree", "add", "--detach",
                    str(pasta), tag], check=True, capture_output=True)
    if patch:
        subprocess.run(["git", "apply", str(Path(__file__).parent / patch)],
                       cwd=pasta, check=True)
    (pasta / "node_modules").symlink_to(modulos or WEB / "node_modules")
    # Com API, a tela precisa ser http://localhost:5173: é a única
    # origem que a API aceita (CORS_ORIGINS e a defesa contra CSRF).
    host = "localhost" if porta else "127.0.0.1"
    porta = porta or _porta_livre()
    vite = subprocess.Popen(
        ["node", str(WEB / "node_modules/vite/bin/vite.js"),
         "--port", str(porta), "--strictPort", "--host", host],
        cwd=pasta, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    url = f"http://{host}:{porta}/"
    try:
        for _ in range(60):
            try:
                urllib.request.urlopen(url, timeout=1)
                break
            except OSError:
                time.sleep(0.25)
        with sync_playwright() as p:
            nav = p.chromium.launch()
            pg = nav.new_context().new_page()
            pg.goto(url)
            pg.wait_for_selector("li")
            pg.evaluate(OBSERVADOR)
            yield pg, nav.version
            nav.close()
    finally:
        vite.terminate()
        vite.wait(timeout=10)
        subprocess.run(["git", "-C", str(WEB), "worktree", "remove",
                        "--force", str(pasta)], capture_output=True)


def rodada(pg, rotulo, acao, mostrar=True):
    """Executa a ação e devolve (registros do Renderometro, DOM)."""
    pg.evaluate("registros.length = 0; "
                "Object.assign(dom, {entram: 0, saem: 0, trocas: 0})")
    acao()
    pg.wait_for_timeout(200)
    regs = pg.evaluate("[...registros]")
    d = pg.evaluate("({...dom})")
    if mostrar:
        print(f"\n{rotulo}")
        for r in regs:
            quem, fase, _ms = r.split(" · ")
            print(f"  {quem:<16}{fase}")
        print(f"  DOM: +{d['entram']} −{d['saem']} ~{d['trocas']}")
    return regs, d


@contextlib.contextmanager
def sessao_api(tag, usuario="carla@hospital.dev",
               senha="rede-na-varanda-de-tarde"):
    """Como sessao(), com a API em :3000 e login feito pela página."""
    with sessao(tag, porta=5173) as (pg, versao):
        status = pg.evaluate("""async ([email, senha]) => {
          const r = await fetch("/api/auth/login", {method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({email, senha})});
          return r.status; }""", [usuario, senha])
        assert status == 200, f"login {status}"
        yield pg, versao


def pacientes_na_api(pg):
    return pg.evaluate("""async () =>
      (await (await fetch("/api/patients")).json())""")


API = Path(os.environ.get("ESTADO_API",
                          Path(__file__).resolve().parents[2] / "api"))


@contextlib.contextmanager
def api(tag, fuso=None):
    """Sobe a API na tag indicada, em :3000, com banco novo em memória.
    fuso: TZ do processo da API (o plantão usa a hora local dela)."""
    pasta = Path(tempfile.mkdtemp(prefix=f"api-{tag}-"))
    subprocess.run(["git", "-C", str(API), "worktree", "add", "--detach",
                    str(pasta), tag], check=True, capture_output=True)
    (pasta / "node_modules").symlink_to(API / "node_modules")
    proc = subprocess.Popen(
        ["node", str(API / "node_modules/tsx/dist/cli.mjs"), "src/server.ts"],
        cwd=pasta, env={**os.environ, "PORT": "3000",
             **({"TZ": fuso} if fuso else {})},
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(80):
            try:
                urllib.request.urlopen("http://localhost:3000/health", timeout=1)
                break
            except OSError:
                time.sleep(0.25)
        yield
    finally:
        proc.terminate()
        proc.wait(timeout=10)
        subprocess.run(["git", "-C", str(API), "worktree", "remove",
                        "--force", str(pasta)], capture_output=True)
