"""Sessão pelo proxy do Vite (capítulos 2 e 15), num navegador real.

uso: python3 medicoes/cap02_cookie.py [chromium|firefox|webkit]
Pré-requisito: API em :3000 e `npm run dev` em :5173.
"""
import sys
from playwright.sync_api import sync_playwright

MOTOR = sys.argv[1] if len(sys.argv) > 1 else "chromium"
TELA = "http://localhost:5173/"
LOGIN = """async () => {
  const r = await fetch("/api/auth/login", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({email: "ana@hospital.dev",
      senha: "cajueiro-em-flor-no-quintal"})});
  return r.status;
}"""
ME = """async () => {
  const r = await fetch("/api/auth/me");
  const j = r.ok ? await r.json() : {};
  return [r.status, j.usuario?.email ?? ""];
}"""

with sync_playwright() as p:
    nav = getattr(p, MOTOR).launch()
    pg = nav.new_page()
    pg.goto(TELA)
    pg.get_by_role("button", name="Verificar API").click()
    pg.get_by_text("ok", exact=True).wait_for()
    print(f"{MOTOR} {nav.version} · {TELA}")
    print("tela: API ok (via proxy /health)")
    print(f"POST /api/auth/login  -> {pg.evaluate(LOGIN)}")
    for c in pg.context.cookies():
        print(f"cookie {c['name']}: httpOnly={c['httpOnly']}"
              f" secure={c['secure']} sameSite={c['sameSite']}")
    print(f"document.cookie       -> {pg.evaluate('document.cookie')!r}")
    status, email = pg.evaluate(ME)
    print(f"GET  /api/auth/me     -> {status} {email}")
    nav.close()
