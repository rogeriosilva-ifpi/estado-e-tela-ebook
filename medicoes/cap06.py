"""Envio duplo contra a API real (capítulo 6), no Chromium.

uso: python3 medicoes/cap06.py [tag-da-tela ...]
Sobe uma API nova (banco em memória) para cada caso, na tag indicada
do repositório api. A rede fica 800 ms mais lenta, como num 4G ruim, e
o roteiro dá dois cliques em seguida no botão Admitir, no mesmo instante.
"""
import sys
import time
from tela import api, pacientes_na_api, sessao_api

CASOS = [("cap06-antes", "base"),
         ("cap06+cap06-so-disabled.patch", "base"),
         ("cap06", "base"), ("cap06", "cap06")]
if len(sys.argv) > 1:
    CASOS = [tuple(a.rsplit("@", 1)) for a in sys.argv[1:]]

for tela, versao_api in CASOS:
    with api(versao_api), sessao_api(tela) as (pg, versao):
        if (tela, versao_api) == CASOS[0]:
            print(f"Chromium {versao} · API real · rede +800 ms")
        pg.route("**/api/patients", lambda r: (
            time.sleep(0.8) if r.request.method == "POST" else None,
            r.continue_()))
        pg.get_by_label("Nome").fill("Rosa Amaral")
        pg.get_by_label("CNS").fill("898001112223334")
        pg.get_by_label("Nascimento").fill("1971-05-20")
        botao = pg.locator("form").filter(
            has=pg.get_by_label("CNS")).get_by_role("button")
        botao.evaluate("b => { b.click(); b.click(); }")
        pg.wait_for_timeout(2500)
        rosas = [p["id"] for p in pacientes_na_api(pg)
                 if p["nome"] == "Rosa Amaral"]
        tela_diz = pg.locator("[role=status], [role=alert]")
        aviso = tela_diz.first.inner_text() if tela_diz.count() else "—"
        rotulo = tela.replace("+cap06-so-disabled.patch", " sem ref")
        print(f"\ntela {rotulo} · api {versao_api}")
        print(f"  prontuários de Rosa: {len(rosas)} {rosas}")
        print(f"  a tela diz: {aviso}")


# Segunda barreira: duas abas, cada uma com o seu formulário. A trava
# do cliente não alcança a outra aba; só o servidor pode recusar.
print("\nduas abas, mesmo paciente")
for versao_api in ("base", "cap06"):
    with api(versao_api), sessao_api(CASOS[-1][0]) as (pg, _v):
        aba2 = pg.context.new_page()
        aba2.goto(pg.url)
        aba2.wait_for_selector("li")
        for p in (pg, aba2):
            p.get_by_label("Nome").fill("Rosa Amaral")
            p.get_by_label("CNS").fill("898001112223334")
            p.get_by_label("Nascimento").fill("1971-05-20")
            p.locator("form").filter(has=p.get_by_label("CNS")) \
                .get_by_role("button").click()
            p.wait_for_timeout(1200)
        rosas = [p["id"] for p in pacientes_na_api(pg)
                 if p["nome"] == "Rosa Amaral"]
        aviso = aba2.locator("[role=status], [role=alert]").first
        print(f"  api {versao_api}: {len(rosas)} prontuário(s)")
        print(f"    aba 2 diz: {aviso.inner_text()}")
