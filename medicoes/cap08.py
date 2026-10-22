"""Busca no prontuário quando a resposta não é a esperada (capítulo 8).

uso: python3 medicoes/cap08.py
Para cada tag, três cenários no Chromium: sem login (a API responde 401
com um objeto), API fora do ar (o proxy do Vite responde 500) e logado.
Em cada um, digita "ma" na busca e conta o que ficou de pé na tela.
"""
import contextlib
from tela import api, sessao, sessao_api

SECAO = "section:has(h2:text-is('Busca no prontuário'))"


def olhar(pg, erros):
    pg.get_by_label("Buscar no prontuário").type("ma")
    pg.wait_for_timeout(1000)
    paineis = pg.locator("h2").count()
    if pg.locator(SECAO).count():
        diz = pg.locator(SECAO).inner_text().split("\n")
        diz = " / ".join(x for x in diz[1:] if x.strip())
    else:
        diz = "(a seção sumiu)"
    print(f"  painéis na tela: {paineis}")
    print(f"  a busca diz: {diz}")
    for e in erros or ["nenhum"]:
        print(f"  erro na página: {e}")


CENARIOS = [
    ("sem login", lambda t: (api("cap07"), sessao(t, porta=5173))),
    ("API fora do ar", lambda t: (contextlib.nullcontext(),
                                  sessao(t, porta=5173))),
    ("logado", lambda t: (api("cap07"), sessao_api(t))),
]

for tag in ("cap08-antes", "cap08"):
    print(f"\ntela {tag}")
    for nome, fazer in CENARIOS:
        a, s = fazer(tag)
        with a, s as (pg, _v):
            erros = []
            pg.on("pageerror", lambda e: erros.append(
                f"{e.name}: {e.message[:60]}"))
            print(f" {nome}")
            olhar(pg, erros)
