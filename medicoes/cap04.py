"""Componente definido dentro de outro (capítulo 4), no Chromium.

uso: python3 medicoes/cap04.py
Mesmo roteiro nas tags cap04-antes e cap04: anotar em João Lima e
digitar uma letra na busca.
"""
from tela import rodada, sessao

for tag in ("cap04-antes", "cap04"):
    with sessao(tag) as (pg, versao):
        if tag == "cap04-antes":
            print(f"Chromium {versao} · modo dev")
        print(f"\n== {tag}")
        campo = pg.get_by_label("Anotação de João Lima")
        campo.fill("ver febre")
        rodada(pg, 'digitar "o" na busca',
               lambda: pg.get_by_label("Buscar paciente").type("o"))
        nota = pg.get_by_label("Anotação de João Lima").input_value()
        print(f"  anotação de João: {nota!r}")
