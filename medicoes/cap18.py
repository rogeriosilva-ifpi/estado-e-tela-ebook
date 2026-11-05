"""O mapa do Next.js no laboratório (capítulo 18).

uso: python3 medicoes/cap18.py
Constrói next cap18 e mostra a tabela de rotas do next build. Depois,
com a API cap15 e o next start em :5174, pede sem navegador:
  /pacientes/p1 sem cookie (o proxy responde antes de renderizar);
  /pacientes/p1 com um cookie inventado (o proxy deixa passar; a API
  recusa, e a ficha manda para o login);
  /saude (Route Handler).
"""
import re
import urllib.error
import urllib.request

from cap17 import ANSI, NEXT, construir, servidor, worktree
from tela import api

BASE = "http://localhost:5174"


class SemSeguir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


abrir = urllib.request.build_opener(SemSeguir).open


def pedir(caminho, cookie=None):
    req = urllib.request.Request(BASE + caminho)
    if cookie:
        req.add_header("Cookie", cookie)
    try:
        r = abrir(req)
        return r.status, r.headers.get("Location"), r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location"), e.read().decode()


with worktree(NEXT, "cap18") as pasta:
    _cod, saida = construir(pasta, ["npx", "next", "build"])
    tabela = saida[saida.index("Route (app)"):].strip()
    print("$ next build   (next cap18)")
    print(ANSI.sub("", tabela))
    with api("cap15"), servidor(["npx", "next", "start", "-p", "5174"],
                                pasta, BASE):
        print()
        st, loc, _ = pedir("/pacientes/p1")
        print(f"GET /pacientes/p1, sem cookie: {st} → {loc}")
        st, loc, corpo = pedir("/pacientes/p1",
                               "__Host-sessao=inventado")
        destino = re.search(r'/entrar\?volta=[^"&;]*', corpo)
        print(f"GET /pacientes/p1, cookie inventado: {st}; o HTML traz "
              f"{'o redirecionamento para ' + destino.group(0) if destino else 'a ficha'}")
        st, _, corpo = pedir("/saude")
        print(f"GET /saude: {st} {corpo}")
