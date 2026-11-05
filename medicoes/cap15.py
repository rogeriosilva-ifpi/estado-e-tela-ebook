"""Sessão na interface: localStorage × sessão vinda do servidor (capítulo 15).

uso: python3 medicoes/cap15.py
Tela cap15-antes com a API cap14; tela cap15 com a API cap15. Em cada par:
  1. Ana entra pela tela e busca "ma"; o servidor encerra todas as sessões
     dela (outro navegador chama /api/auth/logout-all); recarregar.
  2. Ana abre João e troca o nome; a sessão cai; Salvar. Na tag cap15,
     entra de novo pelo formulário: para onde volta?
  3. Sem sessão, abre /pacientes/p1: que pedidos saem antes do login?
  4. O que um script da página enxerga com Ana logada: document.cookie e
     localStorage. Na antes, Carla edita o próprio papel no localStorage.
"""
from tela import api, sessao

ANA = ("ana@hospital.dev", "cajueiro-em-flor-no-quintal")
CARLA = ("carla@hospital.dev", "rede-na-varanda-de-tarde")
BASE = "http://localhost:5173"
PARES = (("cap15-antes", "cap14"), ("cap15", "cap15"))


def entrar_pela_tela(pg, conta, url="/entrar"):
    if url:
        pg.goto(BASE + url)
    pg.get_by_label("E-mail").fill(conta[0])
    pg.get_by_label("Senha").fill(conta[1])
    pg.get_by_role("button", name="Entrar").click()
    pg.wait_for_timeout(700)


def encerrar_no_servidor(pg, conta):
    """Outro navegador entra como a mesma pessoa e sai de todos."""
    outro = pg.context.browser.new_context()
    p2 = outro.new_page()
    p2.goto(BASE + "/entrar")
    st = p2.evaluate("""async ([email, senha]) => {
      const json = {"Content-Type": "application/json"};
      await fetch("/api/auth/login", {method: "POST", headers: json,
        body: JSON.stringify({email, senha})});
      return (await fetch("/api/auth/logout-all",
        {method: "POST"})).status; }""", list(conta))
    outro.close()
    assert st == 204, st


def quem(pg):
    sair = pg.get_by_role("button", name="Sair")
    if sair.count():
        return sair.locator("xpath=..").inner_text() \
            .replace("\n", " ").replace(" Sair", "") + " · botão Sair"
    return "ninguém · link Entrar"


def onde(pg):
    return pg.evaluate("location.pathname + location.search")


def avisos(pg):
    a = pg.get_by_role("alert").all_inner_texts() + \
        pg.get_by_role("status").all_inner_texts()
    return "; ".join(a)


for tela, tag_api in PARES:
    with api(tag_api), sessao(tela, porta=5173) as (pg, versao):
        if tela == "cap15-antes":
            print(f"Chromium {versao}")
        print(f"\ntela {tela} · API {tag_api}")

        # 1. a sessão acaba no servidor; a tela recarrega
        entrar_pela_tela(pg, ANA)
        pg.goto(BASE + "/pacientes?q=ma")
        pg.wait_for_timeout(700)
        encerrar_no_servidor(pg, ANA)
        pg.reload()
        pg.wait_for_timeout(900)
        print("  1. sessão encerrada no servidor, recarregar")
        print(f"     endereço: {onde(pg)}")
        print(f"     cabeçalho: {quem(pg)}")
        print(f"     avisos: {avisos(pg) or '—'}")

        # 2. a sessão cai no meio da edição
        entrar_pela_tela(pg, ANA)
        pg.goto(BASE + "/pacientes/p2?q=jo")
        pg.wait_for_timeout(700)
        artigo = pg.get_by_role("article", name="Paciente aberto")
        artigo.get_by_label("Nome").fill("João Lima Filho")
        encerrar_no_servidor(pg, ANA)
        artigo.get_by_role("button", name="Salvar").click()
        pg.wait_for_timeout(900)
        print("  2. sessão cai, Salvar")
        print(f"     endereço: {onde(pg)}")
        print(f"     cabeçalho: {quem(pg)}")
        print(f"     avisos: {avisos(pg) or '—'}")
        if pg.get_by_label("E-mail").count():
            entrar_pela_tela(pg, ANA, url=None)
            cns = pg.get_by_text("898009876543210").count()
            print(f"     entra de novo: {onde(pg)}"
                  f" · CNS de João na tela: {'sim' if cns else 'não'}")

        # 3. sem sessão, abrir o detalhe
        pg.goto(BASE + "/")
        pg.evaluate("localStorage.clear()")
        pg.context.clear_cookies()
        pedidos = []

        def anota(r):
            caminho = r.url.split("5173")[1]
            if caminho.startswith("/api/"):
                pedidos.append(r.method + " " + caminho)
        pg.on("request", anota)
        pg.goto(BASE + "/pacientes/p1")
        pg.wait_for_timeout(900)
        pg.remove_listener("request", anota)
        print("  3. sem sessão, abrir /pacientes/p1")
        print(f"     endereço: {onde(pg)}")
        print(f"     pedidos à API: {', '.join(pedidos) or 'nenhum'}")
        pedidos.clear()

        # 4. o que um script da página enxerga
        entrar_pela_tela(pg, ANA)
        olho = pg.evaluate("""() => ({cookie: document.cookie,
          local: {...localStorage}})""")
        print("  4. Ana logada; um script da página lê")
        print(f"     document.cookie: {olho['cookie']!r}")
        if not olho["local"]:
            print("     localStorage: vazio")
        for k, v in olho["local"].items():
            print(f"     localStorage[{k!r}]:")
            print(f"       {v}")
        if tela == "cap15-antes":
            pg.get_by_role("button", name="Sair").click()
            pg.wait_for_timeout(500)
            entrar_pela_tela(pg, CARLA)
            pg.goto(BASE + "/pacientes/p4")
            pg.wait_for_timeout(700)
            antes = pg.get_by_role("button", name="Inativar").count()
            pg.evaluate("""() => localStorage.setItem("usuario",
              JSON.stringify({...JSON.parse(localStorage.usuario),
                papel: "profissional"}))""")
            pg.reload()
            pg.wait_for_timeout(700)
            depois = pg.get_by_role("button", name="Inativar").count()
            print("     Carla troca o papel no localStorage e recarrega:")
            print(f"     botão Inativar: {antes} → {depois}")
            if depois:
                pg.get_by_role("button", name="Inativar").click()
                pg.get_by_role("button", name="Confirmar inativação").click()
                pg.wait_for_timeout(700)
                p4 = pg.evaluate("""async () => (await (await fetch(
                  "/api/patients/p4")).json())""")
                print(f"     na API: {p4['nome']} · ativo: {p4.get('ativo')}")
