"""Vigia de acessibilidade (capítulo 9): axe-core + teclado, nos dois temas.

uso: python3 medicoes/vigia_a11y.py TAG [TAG ...]
     (antes: cd medicoes && npm install, para baixar o axe-core)
Para cada tag, sobe a tela, roda o axe com as regras WCAG 2.2 AA no tema
claro e no escuro, e percorre a página com Tab conferindo se cada parada
do foco tem indicação visível (contorno ou sombra).
"""
import sys
from pathlib import Path
from tela import sessao

AXE = Path(__file__).parent / "node_modules/axe-core/axe.min.js"
REGRAS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]

FOCO = """() => {
  const el = document.activeElement;
  const s = getComputedStyle(el);
  const contorno = s.outlineStyle !== "none"
    && parseFloat(s.outlineWidth) > 0;
  return { tag: el.tagName.toLowerCase(),
    nome: (el.getAttribute("aria-label") || el.textContent
      || el.name || "").trim().slice(0, 18),
    visivel: contorno || s.boxShadow !== "none" };
}"""


def axe(pg, tema):
    pg.emulate_media(color_scheme=tema)
    pg.add_script_tag(path=str(AXE))
    r = pg.evaluate("""(tags) => axe.run(document,
        { runOnly: { type: "tag", values: tags } })""", REGRAS)
    total = sum(len(v["nodes"]) for v in r["violations"])
    print(f"  tema {tema}: {len(r['violations'])} regra(s), "
          f"{total} elemento(s)")
    for v in r["violations"]:
        print(f"    {v['id']} ({v['impact']}): {len(v['nodes'])}")
        if v["id"] == "color-contrast":
            vistos = set()
            for n in v["nodes"]:
                d = n["any"][0]["data"]
                k = (d["fgColor"], d["bgColor"])
                if k in vistos:
                    continue
                vistos.add(k)
                print(f"      {d['fgColor']} sobre {d['bgColor']}: "
                      f"{d['contrastRatio']}:1 (mínimo "
                      f"{d['expectedContrastRatio']})")
    return total


def teclado(pg):
    pg.emulate_media(color_scheme="light")
    pg.evaluate("document.activeElement.blur()")
    paradas, sem = 0, []
    for _ in range(80):
        pg.keyboard.press("Tab")
        f = pg.evaluate(FOCO)
        if f["tag"] == "body":
            break
        paradas += 1
        if not f["visivel"]:
            sem.append(f"{f['tag']} “{f['nome']}”")
    print(f"  teclado: {paradas} paradas, {len(sem)} sem foco visível")
    for s in sem[:4]:
        print(f"    {s}")
    if len(sem) > 4:
        print(f"    … e mais {len(sem) - 4}")


for tag in sys.argv[1:]:
    print(f"\ntela {tag}")
    with sessao(tag) as (pg, versao):
        for tema in ("light", "dark"):
            axe(pg, tema)
        teclado(pg)
