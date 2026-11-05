"""O cookie __Host-sessao em http://localhost, motor por motor (pendência do lote 1).

uso: xvfb-run -a python3 medicoes/cookie_navegadores.py
A API (cap15) emite __Host-sessao com Secure, HttpOnly, SameSite=Lax e
Path=/. A tela (web cap16) roda no Vite em http://localhost:5173, com o
proxy de /api. Em cada navegador: entrar pelo formulário, abrir a busca e
perguntar /api/auth/me. Se o navegador recusar cookie Secure em http, o
login "funciona" e a sessão some no pedido seguinte.

Chromium pelo Playwright; WebKitGTK (o motor do Safari, com a pilha de
rede do GTK) pelo WebKitWebDriver. Firefox não entra: o ambiente não
consegue baixar o navegador.

Depois, o remédio do capítulo 19: a tela cap19 em https://localhost:5173
(npm run dev:https, certificado autoassinado) com a API cap19, que aceita
essa origem. O WebKitGTK repete o roteiro.
"""
import subprocess
import tempfile
import time
import urllib.request
import ssl
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from playwright.sync_api import sync_playwright
from tela import WEB, api, sessao

BASE = "http://localhost:5173"
ANA = ("ana@hospital.dev", "cajueiro-em-flor-no-quintal")
ME = """const feito = arguments[arguments.length - 1];
fetch("/api/auth/me").then(r => feito(r.status));"""


def relatar(nome, versao, me, cns, cookie_js):
    print(f"{nome} {versao}")
    print(f"  /api/auth/me depois do login: {me}")
    print(f"  CNS de Maria na ficha: {'sim' if cns else 'não'}")
    print(f"  document.cookie: {cookie_js!r}")


def webkit(base=BASE, nome="WebKitGTK"):
    opcoes = webdriver.WebKitGTKOptions()
    opcoes.accept_insecure_certs = True
    opcoes.binary_location = \
        "/usr/lib/x86_64-linux-gnu/webkit2gtk-4.1/MiniBrowser"
    opcoes.add_argument("--automation")
    nav = webdriver.WebKitGTK(options=opcoes)
    try:
        nav.get(base + "/entrar")
        espera = WebDriverWait(nav, 15)
        espera.until(lambda n: n.find_elements(By.CSS_SELECTOR,
                                               "input[type=email]"))
        nav.find_element(By.CSS_SELECTOR, "input[type=email]").send_keys(ANA[0])
        nav.find_element(By.CSS_SELECTOR,
                         "input[type=password]").send_keys(ANA[1])
        nav.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
        espera.until(lambda n: "/entrar" not in n.current_url)
        me = nav.execute_async_script(ME)
        nav.get(base + "/pacientes/p1")
        try:
            espera.until(lambda n: "898001234567890" in n.page_source)
            cns = True
        except Exception:
            cns = False
        versao = nav.capabilities.get("browserVersion", "?")
        relatar(nome, versao, me, cns,
                nav.execute_script("return document.cookie"))
    finally:
        nav.quit()


with api("cap15"):
    with sessao("cap16", porta=5173) as (pg, versao):
        pg.goto(BASE + "/entrar")
        pg.get_by_label("E-mail").fill(ANA[0])
        pg.get_by_label("Senha").fill(ANA[1])
        pg.get_by_role("button", name="Entrar").click()
        pg.wait_for_timeout(800)
        me = pg.evaluate("fetch('/api/auth/me').then(r => r.status)")
        pg.goto(BASE + "/pacientes/p1")
        cns = pg.get_by_text("898001234567890").count() > 0 or \
            pg.wait_for_timeout(1500) or \
            pg.get_by_text("898001234567890").count() > 0
        relatar("Chromium", versao, me, cns, pg.evaluate("document.cookie"))
        webkit()


def vite_https(tag):
    """Sobe a tela da tag com `vite --mode https` em :5173."""
    pasta = Path(tempfile.mkdtemp(prefix=f"https-{tag}-"))
    subprocess.run(["git", "-C", str(WEB), "worktree", "add", "--detach",
                    str(pasta), tag], check=True, capture_output=True)
    (pasta / "node_modules").symlink_to(WEB / "node_modules")
    proc = subprocess.Popen(
        ["node", str(WEB / "node_modules/vite/bin/vite.js"), "--mode",
         "https", "--port", "5173", "--strictPort", "--host", "localhost"],
        cwd=pasta, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ctx = ssl._create_unverified_context()
    for _ in range(60):
        try:
            urllib.request.urlopen("https://localhost:5173/", timeout=1,
                                   context=ctx)
            break
        except OSError:
            time.sleep(0.25)
    return proc, pasta


print()
with api("cap19"):
    proc, pasta = vite_https("cap19")
    try:
        webkit("https://localhost:5173", "WebKitGTK, https (dev:https)")
    finally:
        proc.terminate()
        proc.wait(timeout=10)
        subprocess.run(["git", "-C", str(WEB), "worktree", "remove",
                        "--force", str(pasta)], capture_output=True)
