"""Corrida entre respostas (capítulo 7), no Chromium, com a API real.

uso: python3 medicoes/cap07.py
A página abre com ?atraso=900:lento:ma: a API segura só a busca "ma".
O roteiro digita "ma" e, logo depois, um "r" ("mar"), e registra
cada pedido, cada resposta e o que a tela mostra no fim.
"""
import time
from tela import api, sessao_api

for tag in ("cap07-antes", "cap07"):
    with api("cap07"), sessao_api(tag) as (pg, versao):
        if tag == "cap07-antes":
            print(f"Chromium {versao} · API real · ?atraso=900:lento:ma")
        pg.goto(pg.url + "?atraso=900:lento:ma")
        pg.wait_for_selector("li")
        t0 = time.monotonic()
        linhas = []

        def ms():
            return f"{(time.monotonic() - t0) * 1000:5.0f} ms"

        def termo(url):
            return url.split("q=")[1].split("&")[0]

        pg.on("request", lambda r: linhas.append(
            f"{ms()}  pede  q={termo(r.url)}")
            if "q=" in r.url else None)
        pg.on("requestfailed", lambda r: linhas.append(
            f"{ms()}  cancelado q={termo(r.url)}")
            if "q=" in r.url else None)
        pg.on("requestfinished", lambda r: linhas.append(
            f"{ms()}  chega q={termo(r.url)}")
            if "q=" in r.url else None)
        campo = pg.get_by_label("Buscar no prontuário")
        campo.type("ma")
        pg.wait_for_timeout(150)
        campo.type("r")
        pg.wait_for_timeout(1500)
        res = pg.get_by_role("list", name="Resultados") \
            .get_by_role("listitem").all_inner_texts()
        print(f"\n== {tag}")
        print("\n".join(linhas))
        print(f"  termo na tela: {campo.input_value()!r}")
        print(f"  resultados:    {res}")
