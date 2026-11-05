"""porta-dos-fundos: o que a tela esconde de um papel, a API proíbe?

uso: python3 medicoes/porta_dos_fundos.py TAG_TELA TAG_API
Caixa-preta, sem ler o código da tela. Para cada página da lista:
  1. entra como profissional e como recepção, em navegadores separados,
     e anota os botões de ação de cada um;
  2. botão que o profissional vê e a recepção não é uma ação escondida;
  3. o profissional clica (e confirma, se abrir diálogo) com a rede
     interceptada: o pedido é anotado e não chega ao servidor;
  4. a recepção faz o mesmo pedido direto, com a sessão dela. Tem de
     receber 403. Qualquer outra resposta é uma porta dos fundos.
Sai com código 1 se achar alguma.
"""
import sys
from tela import api, sessao

TELA, TAG_API = sys.argv[1], sys.argv[2]
BASE = "http://localhost:5173"
CONTAS = {"profissional": ("ana@hospital.dev", "cajueiro-em-flor-no-quintal"),
          "recepcao": ("carla@hospital.dev", "rede-na-varanda-de-tarde")}
PAGINAS = {"/pacientes/p3": ("article", "Paciente aberto")}


def entrar(pg, conta):
    pg.goto(BASE + "/entrar")
    pg.get_by_label("E-mail").fill(conta[0])
    pg.get_by_label("Senha").fill(conta[1])
    pg.get_by_role("button", name="Entrar").click()
    pg.wait_for_timeout(700)


def botoes(pg, url, regiao):
    pg.goto(BASE + url)
    pg.wait_for_timeout(800)
    area = pg.get_by_role(regiao[0], name=regiao[1])
    return [b.inner_text() for b in area.get_by_role("button").all()
            if b.is_visible()]


def pedido_do_botao(pg, url, regiao, nome):
    anotados = []

    def segura(rota):
        r = rota.request
        if r.method != "GET":
            anotados.append((r.method, r.url.split("5173")[1]))
            return rota.abort()
        return rota.continue_()
    pg.route("**/api/**", segura)
    pg.goto(BASE + url)
    pg.wait_for_timeout(800)
    pg.get_by_role(regiao[0], name=regiao[1]) \
        .get_by_role("button", name=nome, exact=True).click()
    dialogo = pg.get_by_role("dialog")
    if dialogo.count() and dialogo.is_visible():
        dialogo.get_by_role("button").last.click()   # confirmar
    pg.wait_for_timeout(500)
    pg.unroute("**/api/**", segura)
    return anotados


achou = 0
with api(TAG_API), sessao(TELA, porta=5173) as (pg, _v):
    carla = pg.context.browser.new_context().new_page()
    entrar(pg, CONTAS["profissional"])
    entrar(carla, CONTAS["recepcao"])
    print(f"porta-dos-fundos · tela {TELA} · API {TAG_API}")
    for url, regiao in PAGINAS.items():
        prof = botoes(pg, url, regiao)
        rec = botoes(carla, url, regiao)
        escondidos = [b for b in prof if b not in rec]
        print(f"{url}: profissional vê {prof}; recepcao vê {rec}")
        print(f"  escondidos de recepcao: {escondidos or 'nenhum'}")
        for nome in escondidos:
            for metodo, caminho in pedido_do_botao(pg, url, regiao, nome):
                st = carla.evaluate("""async ([m, c]) =>
                  (await fetch(c, {method: m})).status""", [metodo, caminho])
                ok = st == 403
                achou += not ok
                print(f"  {nome} → {metodo} {caminho}")
                print(f"    recepcao, chamando direto: {st}"
                      + ("  ✓" if ok else "  ✗ esperado 403"))
print("nenhuma porta dos fundos" if not achou
      else f"{achou} porta(s) dos fundos")
sys.exit(1 if achou else 0)
