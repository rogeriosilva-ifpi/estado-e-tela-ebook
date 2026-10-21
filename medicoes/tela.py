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
def sessao(tag):
    pasta = Path(tempfile.mkdtemp(prefix=f"tela-{tag}-"))
    subprocess.run(["git", "-C", str(WEB), "worktree", "add", "--detach",
                    str(pasta), tag], check=True, capture_output=True)
    (pasta / "node_modules").symlink_to(WEB / "node_modules")
    porta = _porta_livre()
    vite = subprocess.Popen(
        ["node", str(WEB / "node_modules/vite/bin/vite.js"),
         "--port", str(porta), "--strictPort", "--host", "127.0.0.1"],
        cwd=pasta, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    url = f"http://127.0.0.1:{porta}/"
    try:
        for _ in range(60):
            try:
                urllib.request.urlopen(url, timeout=1)
                break
            except OSError:
                time.sleep(0.25)
        with sync_playwright() as p:
            nav = p.chromium.launch()
            pg = nav.new_page()
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
