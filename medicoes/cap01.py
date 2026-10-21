"""Mede as três versões da Ala B (capítulo 1) num Chromium real.

uso: python3 medicoes/cap01.py <pasta laboratorio/cap01> <vendor.js>

React 19 não publica build UMD e o laboratório importa React do esm.sh
por importmap. Aqui as duas URLs do importmap são servidas a partir de
um bundle local das mesmas versões (19.3.1), para rodar sem internet.
"""
import functools, http.server, sys, threading
from pathlib import Path
from playwright.sync_api import sync_playwright

PASTA, VENDOR = Path(sys.argv[1]), Path(sys.argv[2]).read_text()
PAGINAS = [("imperativo", "1-imperativo.html"),
           ("render()", "2-render.html"),
           ("React", "3-react.html")]
SHIM = {
    "https://esm.sh/react@19.3.1":
        "import {React} from '/__vendor.js';\n"
        "export const {createElement,useState} = React;\n"
        "export default React;",
    "https://esm.sh/react-dom@19.3.1/client":
        "export {createRoot} from '/__vendor.js';",
}

Handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                            directory=str(PASTA))
Handler.log_message = lambda *a, **k: None
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{srv.server_port}/"


def delta(antes, depois):
    return (f"+{depois['entram'] - antes['entram']}"
            f" −{depois['saem'] - antes['saem']}"
            f" ~{depois['trocas'] - antes['trocas']}")


def medidas(pg):
    pg.wait_for_timeout(150)
    return pg.evaluate("({...window.medidas})")


def linha_de(pg, nome):
    return pg.locator("li", has_text=nome)


with sync_playwright() as p:
    nav = p.chromium.launch()
    print(f"Chromium {nav.version}\n")
    print(f"{'versão':<11}{'busca o':<12}{'alta Maria':<12}"
          f"{'nota':<8}alto")
    for rotulo, arquivo in PAGINAS:
        pg = nav.new_page()
        pg.route("https://esm.sh/**", lambda r: r.fulfill(
            body=SHIM[r.request.url], content_type="text/javascript"))
        pg.route("**/__vendor.js", lambda r: r.fulfill(
            body=VENDOR, content_type="text/javascript"))
        pg.goto(BASE + arquivo)
        pg.wait_for_selector("li")
        linha_de(pg, "João Lima").locator("input").fill("ver febre")
        m0 = medidas(pg)
        pg.get_by_placeholder("buscar").type("o")
        m1 = medidas(pg)
        nota = linha_de(pg, "João Lima").locator("input").input_value()
        pg.get_by_placeholder("buscar").fill("")
        m2 = medidas(pg)
        linha_de(pg, "Maria Souza").get_by_role("button").click()
        m3 = medidas(pg)
        txt = pg.locator("#app p").inner_text()
        alto = txt.split("alto risco:")[1].strip()
        print(f"{rotulo:<11}{delta(m0, m1):<12}{delta(m2, m3):<12}"
              f"{'fica' if nota else 'some':<8}{alto}")
    nav.close()
print("\n+ elementos que entram  − que saem\n"
      "~ textos ou atributos trocados")
