"""Voltar durante o envio, com a API real (capítulo 12), no Chromium.

uso: python3 medicoes/cap12.py [tag-final]
API na tag cap12. O roteiro segura o POST até mandar: preenche a
admissão, chega à confirmação, clica Admitir e, com a resposta retida,
clica Voltar; só então libera o POST. Depois conta o que a tela mostra e o que a API guardou, e
tenta seguir o fluxo de novo.
"""
import sys
from tela import api, pacientes_na_api, sessao_api

FINAL = sys.argv[1] if len(sys.argv) > 1 else "cap12"


def tela_diz(pg):
    h = pg.locator("h3").first.inner_text() if pg.locator("h3").count() \
        else "(fim do assistente)"
    avisos = [a.inner_text() for a in
              pg.locator("[role=status], [role=alert]").all()]
    return h, avisos


for tag in ("cap12-antes", FINAL):
    with api("cap12"), sessao_api(tag) as (pg, versao):
        if tag == "cap12-antes":
            print(f"Chromium {versao} · API cap12 · POST retido")
        retidos = []
        pg.route("**/api/patients", lambda r: retidos.append(r)
                 if r.request.method == "POST" else r.continue_())
        pg.get_by_label("Nome").fill("Rosa Amaral")
        pg.get_by_label("CNS").fill("898001112223334")
        pg.get_by_label("Nascimento").fill("1971-05-20")
        av = lambda: pg.get_by_role("button", name="Avançar").click()
        av(); av()
        pg.get_by_role("button", name="Admitir").click()
        voltar = pg.get_by_role("button", name="Voltar")
        pg.wait_for_timeout(300)
        print(f"\ntela {tag}")
        print(f"  Voltar durante o envio: "
              f"{'desabilitado' if voltar.is_disabled() else 'clicado'}")
        if voltar.is_enabled():
            voltar.click()
        for r in retidos:
            r.continue_()
        retidos.clear()
        pg.unroute("**/api/patients")
        pg.wait_for_timeout(1500)
        h, avisos = tela_diz(pg)
        rosas = [p["id"] for p in pacientes_na_api(pg)
                 if p["nome"] == "Rosa Amaral"]
        print(f"  a tela mostra: {h}")
        for a in avisos:
            print(f"  aviso: {a}")
        print(f"  prontuários de Rosa na API: {len(rosas)}")
        if pg.get_by_role("button", name="Avançar").count():
            av()
            pg.get_by_role("button", name="Admitir").click()
            pg.wait_for_timeout(1500)
            h, avisos = tela_diz(pg)
            print(f"  segue o fluxo e admite de novo: {h}")
            for a in avisos:
                print(f"  aviso: {a}")
