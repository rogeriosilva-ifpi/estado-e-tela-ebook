"""Preferências de exibição: quem renderiza quando uma muda (capítulo 11).

uso: python3 medicoes/cap11.py [tag-final]
Três versões no Chromium, modo dev: props descendo do App (cap11-antes),
um contexto só com o valor recriado a cada render (cap11 com o patch
cap11-contexto-unico.patch) e três contextos separados (cap11). Em cada
uma, troca o tema para Escuro e depois liga o modo discreto; o
Renderometro conta os cartões da Ala que renderizaram em cada ação.
"""
import sys
from tela import rodada, sessao

FINAL = sys.argv[1] if len(sys.argv) > 1 else "cap11"
VERSOES = [("cap11-antes", "props a partir do App"),
           (f"{FINAL}+cap11-contexto-unico.patch", "contexto único"),
           (FINAL, "três contextos")]

for tag, nome in VERSOES:
    with sessao(tag) as (pg, versao):
        if tag == VERSOES[0][0]:
            print(f"Chromium {versao} · modo dev")
        print(f"\n== {nome}")
        for rotulo, acao in (
            ("tema → Escuro",
             lambda: pg.get_by_label("Tema").select_option("escuro")),
            ("modo discreto ligado",
             lambda: pg.get_by_label("Modo discreto (só iniciais)")
             .check()),
        ):
            regs, _ = rodada(pg, rotulo, acao, mostrar=False)
            cartoes = {r.split(" · ")[0] for r in regs}
            print(f"  {rotulo:<22} {len(cartoes)} de 6 cartões renderizaram")
        print(f"  primeiro cartão: {pg.locator('li').first.inner_text().split(chr(10))[0]}")
