"""Estado remoto: cópia em useState × cache do TanStack Query (capítulo 14).

uso: python3 medicoes/cap14.py [tag-final]
API na tag cap14, logado como carla@. Em cada tag da tela:
  1. busca "a", abre Maria e depois João: de quem é o CNS no detalhe?
  2. na URL de João, troca o nome para "João Lima Neto" e salva: quem
     mudou na API, e o que a lista mostra?
  3. inativa o paciente aberto: ele some da lista?
  4. vai à Ala B e volta com o Voltar: quantas buscas foram à rede?
Na tag final, mede também a edição otimista: o servidor demora e
responde 500.
"""
import sys
from tela import api, sessao_api

FINAL = sys.argv[1] if len(sys.argv) > 1 else "cap14"
BASE = "http://localhost:5173"


def nomes(pg):
    return pg.get_by_role("list", name="Resultados") \
        .get_by_role("link").all_inner_texts()


def na_api(pg, pid):
    return pg.evaluate("""async (id) => (await (await fetch(
        `/api/patients/${id}`)).json()).nome""", pid)


def abrir(pg, nome):
    pg.get_by_role("list", name="Resultados") \
        .get_by_role("link", name=nome, exact=True).click()
    pg.wait_for_timeout(600)


for tag in ("cap14-antes", FINAL):
    with api("cap14"), sessao_api(tag) as (pg, versao):
        if tag == "cap14-antes":
            print(f"Chromium {versao} · API cap14 · logado como carla@")
        print(f"\ntela {tag}")
        pg.goto(f"{BASE}/pacientes?q=a")
        pg.wait_for_timeout(800)
        abrir(pg, "Maria Souza")
        abrir(pg, "João Lima")
        cns = pg.get_by_role("article").locator("dd").first.inner_text()
        dono = {"898001234567890": "Maria", "898009876543210": "João"}
        print(f"  URL {pg.url.split('5173')[1]} · CNS no detalhe: "
              f"{dono.get(cns, cns)}")

        campo = pg.get_by_role("article").get_by_label("Nome")
        campo.fill("João Lima Neto")
        pg.get_by_role("article").get_by_role("button",
                                              name="Salvar").click()
        pg.wait_for_timeout(1000)
        print(f"  salvou: p1 na API = {na_api(pg, 'p1')!r} · "
              f"p2 na API = {na_api(pg, 'p2')!r}")
        print(f"  lista: {', '.join(nomes(pg))}")

        pg.get_by_role("article").get_by_role("button",
                                              name="Inativar").click()
        pg.get_by_role("button", name="Confirmar inativação").click()
        pg.wait_for_timeout(1000)
        print(f"  inativou o aberto · lista: {', '.join(nomes(pg))}")

        buscas = []
        pg.on("request", lambda r: buscas.append(r.url)
              if "/api/patients?" in r.url else None)
        pg.get_by_role("navigation").get_by_text("Ala B").click()
        pg.wait_for_timeout(500)
        pg.go_back()
        pg.wait_for_timeout(1000)
        print(f"  Ala B e Voltar: {len(buscas)} busca(s) à rede")

        if tag != FINAL:
            continue
        print("\n  edição otimista, servidor lento que responde 500")
        pg.goto(f"{BASE}/pacientes/p3?q=an")
        pg.wait_for_timeout(800)
        retidos = []
        pg.route("**/api/patients/p3", lambda r: retidos.append(r)
                 if r.request.method == "PATCH" else r.continue_())
        titulo = pg.get_by_role("article").locator("h3")
        antes = titulo.inner_text()
        pg.get_by_role("article").get_by_label("Nome").fill("Ana C. Reis")
        pg.get_by_role("article").get_by_role("button",
                                              name="Salvar").click()
        pg.wait_for_timeout(200)
        print(f"    título antes: {antes!r} · logo após Salvar: "
              f"{titulo.inner_text()!r}")
        for r in retidos:
            r.fulfill(status=500, json={"error": "Falha interna."})
        pg.wait_for_timeout(1200)
        aviso = pg.get_by_role("alert").all_inner_texts()
        print(f"    depois do 500: {titulo.inner_text()!r} · "
              f"aviso: {' '.join(' '.join(aviso).split())!r}")
