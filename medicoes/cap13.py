"""Rotas no navegador de verdade (capítulo 13), no Chromium.

uso: python3 medicoes/cap13.py [tag-final]
Com a API cap12 e login feito, em cada tag:
  1. liga o modo discreto e clica "Prontuário" no menu: conta quantos
     documentos o navegador baixou e se a preferência sobreviveu;
  2. busca "ma", abre o primeiro resultado e volta com o botão Voltar;
  3. abre direto /pacientes/p999 e /nada-aqui.
Na tag final, compara com a variante cap13-sem-flushsync.patch: digita
"maria souza" 20 vezes, sem pausa e com 50 ms entre teclas, e conta
quantas vezes o campo terminou diferente do digitado.
Depois faz o build de cada tag e mede os arquivos JS, e serve o build
de duas formas para ver quem devolve a página em /pacientes/p1.
"""
import gzip
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path
from tela import WEB, api, sessao_api

FINAL = sys.argv[1] if len(sys.argv) > 1 else "cap13"


def texto(pg):
    # o painel da rota, ou a página inteira se o layout sumiu
    alvo = pg.locator("section").last if pg.locator("main").count() \
        else pg.locator("body")
    prefixo = "" if pg.locator("main").count() else "(sem layout) "
    return prefixo + " ".join(alvo.inner_text().split())[:60]


for tag in ("cap13-antes", FINAL):
    with api("cap12"), sessao_api(tag) as (pg, versao):
        if tag == "cap13-antes":
            print(f"Chromium {versao} · API cap12 · logado como carla@")
        print(f"\ntela {tag}")
        docs = []
        pg.on("request", lambda r: docs.append(r.url)
              if r.resource_type == "document" else None)
        pg.get_by_label("Modo discreto (só iniciais)").check()
        pg.get_by_role("navigation").get_by_text("Prontuário").click()
        pg.wait_for_url("**/pacientes")
        pg.wait_for_timeout(500)
        ligado = pg.get_by_label("Modo discreto (só iniciais)").is_checked()
        print(f"  menu → Prontuário: {len(docs)} documento(s) baixado(s); "
              f"modo discreto {'ligado' if ligado else 'desligado'}")
        pg.get_by_label("Modo discreto (só iniciais)").set_checked(False)
        pg.get_by_label("Buscar no prontuário").type("ma")
        pg.wait_for_timeout(800)
        pg.get_by_role("list", name="Resultados").get_by_role(
            "link").first.click()
        pg.wait_for_url("**/pacientes/p*")
        pg.wait_for_timeout(300)
        print(f"  abre o 1º resultado: {pg.url.split('5173')[1]}")
        pg.go_back()
        pg.wait_for_timeout(800)
        campo = pg.get_by_label("Buscar no prontuário").input_value()
        n = pg.get_by_role("list", name="Resultados") \
            .get_by_role("listitem").count()
        print(f"  Voltar: {pg.url.split('5173')[1]} · campo {campo!r} · "
              f"{n} resultado(s)")
        for url in ("/pacientes/p999", "/nada-aqui"):
            pg.goto(f"http://localhost:5173{url}")
            pg.wait_for_timeout(800)
            print(f"  {url}: {texto(pg)}")


TXT = "maria souza"
print(f"\ndigitar {TXT!r} na busca 20 vezes; quantas perdem tecla")
for variante in (f"{FINAL}+cap13-sem-flushsync.patch", FINAL):
    with api("cap12"), sessao_api(variante) as (pg, _v):
        rotulo = "sem flushSync" if "+" in variante else "com flushSync"
        for atraso in (0, 50):
            perdas = 0
            for _ in range(20):
                pg.goto("http://localhost:5173/pacientes")
                campo = pg.get_by_label("Buscar no prontuário")
                campo.type(TXT, delay=atraso)
                pg.wait_for_timeout(300)
                perdas += campo.input_value() != TXT
            print(f"  {rotulo}, {atraso:>2} ms entre teclas: "
                  f"{perdas} de 20 perderam tecla")


def construir(tag):
    pasta = Path(tempfile.mkdtemp(prefix=f"build-{tag}-"))
    subprocess.run(["git", "-C", str(WEB), "worktree", "add", "--detach",
                    str(pasta), tag], check=True, capture_output=True)
    (pasta / "node_modules").symlink_to(WEB / "node_modules")
    subprocess.run(["node", "node_modules/vite/bin/vite.js", "build",
                    "--logLevel", "silent"], cwd=pasta, check=True)
    return pasta


def status(url):
    try:
        return urllib.request.urlopen(url).status
    except urllib.error.HTTPError as e:
        return e.code


print("\nbuild de produção (JS, com gzip)")
for tag in ("cap13-antes", FINAL):
    pasta = construir(tag)
    try:
        arqs = sorted((pasta / "dist/assets").glob("*.js"),
                      key=lambda a: -a.stat().st_size)
        partes = [f"{a.name.split('-')[0]} "
                  f"{len(gzip.compress(a.read_bytes(), 9)) / 1024:.1f} kB"
                  for a in arqs]
        print(f"  {tag}: {' + '.join(partes)}")
        if tag != FINAL:
            continue
        print("\nquem responde GET /pacientes/p1 com o build")
        servidores = [
            ("python -m http.server", ["python3", "-m", "http.server",
                                       "4180", "-d", "dist"], 4180),
            ("vite preview", ["node", "node_modules/vite/bin/vite.js",
                              "preview", "--port", "4181",
                              "--strictPort"], 4181)]
        for nome, cmd, porta in servidores:
            p = subprocess.Popen(cmd, cwd=pasta, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
            try:
                time.sleep(2)
                print(f"  {nome}: "
                      f"{status(f'http://127.0.0.1:{porta}/pacientes/p1')}")
            finally:
                p.terminate()
                p.wait()
    finally:
        subprocess.run(["git", "-C", str(WEB), "worktree", "remove",
                        "--force", str(pasta)], capture_output=True)
