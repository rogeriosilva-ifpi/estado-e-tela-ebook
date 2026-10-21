"""Renderizar × mudar o DOM (capítulo 3), no Chromium.

uso: python3 medicoes/cap03.py   (com `npm run dev` em :5173)
Cruza o que o Renderometro anotou com o que um MutationObserver viu.
"""
from playwright.sync_api import sync_playwright

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


def rodada(pg, rotulo, acao):
    pg.evaluate("registros.length = 0; "
                "Object.assign(dom, {entram: 0, saem: 0, trocas: 0})")
    acao()
    pg.wait_for_timeout(200)
    regs = pg.evaluate("[...registros]")
    d = pg.evaluate("({...dom})")
    print(f"\n{rotulo}")
    for r in regs:
        print(f"  {r.split(' · ')[0]:<16}{r.split(' · ')[1]}")
    print(f"  DOM: +{d['entram']} −{d['saem']} ~{d['trocas']}")


with sync_playwright() as p:
    nav = p.chromium.launch()
    pg = nav.new_page()
    pg.goto("http://localhost:5173/")
    pg.wait_for_selector("li")
    pg.evaluate(OBSERVADOR)
    print(f"Chromium {nav.version} · modo dev · StrictMode")
    busca = pg.get_by_label("Buscar paciente")
    rodada(pg, 'digitar "o" na busca', lambda: busca.type("o"))
    rodada(pg, "apagar a busca", lambda: busca.fill(""))
    maria = pg.locator("li", has_text="Maria Souza")
    rodada(pg, "alta de Maria Souza",
           lambda: maria.get_by_role("button").click())
    rodada(pg, "anotar em João Lima",
           lambda: pg.get_by_label("Anotação de João Lima")
           .type("ver"))
    nav.close()
