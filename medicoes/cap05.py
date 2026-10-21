"""Mutação × atualização imutável (capítulo 5), no Chromium.

uso: python3 medicoes/cap05.py
Nas tags cap05-antes e cap05: clicar em Prioridade de João Lima e,
depois, digitar uma letra na busca, que não tem relação nenhuma com
a prioridade.
"""
from tela import rodada, sessao


def estrela(pg):
    li = pg.locator("li", has_text="João Lima")
    return "sim" if li.get_by_label("prioridade").count() else "não"


for tag in ("cap05-antes", "cap05"):
    with sessao(tag) as (pg, versao):
        if tag == "cap05-antes":
            print(f"Chromium {versao} · modo dev")
        print(f"\n== {tag}")
        joao = pg.locator("li", has_text="João Lima")
        regs, d = rodada(pg, "", lambda: joao.get_by_role(
            "button", name="Prioridade").click(), mostrar=False)
        print(f"clique em Prioridade: {len(regs)} render(s),"
              f" ★ na tela: {estrela(pg)}")
        regs, d = rodada(pg, "", lambda: pg.get_by_label(
            "Buscar paciente").type("o"), mostrar=False)
        print(f"tecla na busca:       {len(regs)} render(s),"
              f" ★ na tela: {estrela(pg)}")
