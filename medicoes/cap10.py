"""Confirmação de alta pelo teclado (capítulo 10), no Chromium.

uso: python3 medicoes/cap10.py [tag ...]
Abre a confirmação de alta de Maria Souza com Enter no botão Alta e mede:
para onde vai o foco, quantas paradas de Tab escapam para o fundo, o que
a árvore de acessibilidade expõe, se Esc fecha e para onde o foco volta.
"""
import sys
from tela import sessao

TAGS = sys.argv[1:] or ["cap10-antes", "cap10"]

FOCO = """() => {
  const el = document.activeElement;
  const caixa = [...document.querySelectorAll("dialog, div")]
    .filter((d) => d.textContent.includes("Dar alta a")
      && d.querySelector("button"))
    .sort((a, b) => a.contains(b) ? 1 : -1)[0];
  const quem = el === document.body ? "body"
    : `${el.tagName.toLowerCase()} “${(el.getAttribute("aria-label")
      || el.textContent).trim().slice(0, 22)}”`;
  return { quem, dentro: !!caixa && caixa.contains(el),
    aberta: !!caixa && caixa.checkVisibility() };
}"""


def abrir(pg, nome="Maria Souza"):
    cartao = pg.locator("li").filter(has_text=nome)
    cartao.get_by_role("button", name="Alta").focus()
    pg.keyboard.press("Enter")
    pg.wait_for_timeout(200)


for tag in TAGS:
    print(f"\ntela {tag}")
    with sessao(tag) as (pg, _v):
        abrir(pg)
        f = pg.evaluate(FOCO)
        print(f"  ao abrir, foco em: {f['quem']}"
              f" ({'dentro' if f['dentro'] else 'fora'} da caixa)")
        # a árvore que o leitor de tela recebe, direto do Chromium
        cdp = pg.context.new_cdp_session(pg)
        papeis = [n["role"]["value"] for n in
                  cdp.send("Accessibility.getFullAXTree")["nodes"]
                  if not n.get("ignored") and "role" in n]
        print(f"  árvore de acessibilidade: "
              f"{papeis.count('dialog')} diálogo(s), "
              f"{papeis.count('button')} botões expostos")
        fundo = barra = 0
        for _ in range(8):
            pg.keyboard.press("Tab")
            f = pg.evaluate(FOCO)
            # body durante o Tab: o foco saiu para a barra do navegador
            barra += f["quem"] == "body"
            fundo += f["quem"] != "body" and not f["dentro"]
        print(f"  8 Tabs: {fundo} no fundo da página, "
              f"{barra} na barra do navegador")
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(200)
        f = pg.evaluate(FOCO)
        print(f"  Esc: caixa {'continua aberta' if f['aberta'] else 'fechou'}")
        if f["aberta"]:
            pg.get_by_role("button", name="Cancelar").click()
            pg.wait_for_timeout(200)
            print("  (fechada pelo botão Cancelar)")
        print(f"  ao fechar, foco em: {pg.evaluate(FOCO)['quem']}")
        abrir(pg)
        pg.get_by_role("button", name="Confirmar alta").click()
        pg.wait_for_timeout(200)
        print(f"  depois da alta, foco em: {pg.evaluate(FOCO)['quem']}")
