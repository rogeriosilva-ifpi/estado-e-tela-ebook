"""Capítulo 19: a entrega em 12 passos, medida.

uso: python3 medicoes/cap19.py [REV]      (REV padrão: cap19)
Grava em saidas/:
  c19-passos.txt     git log dos 12 passos (cap16..REV)
  c19-depuracao.txt  a recepção abre /atendimentos/e1: passo 08 e REV
  c19-plantao.txt    a Dra. Ana prescreve com a API de dia e de noite
  c19-gate.txt       npm run gate:completo na REV, com a API de dia
A API sobe na tag cap19 com TZ escolhido: a escala de plantão usa a hora
local do processo da API (Ana: 07h às 19h).
"""
import datetime
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from tela import WEB, api, sessao, sessao_api

REV = sys.argv[1] if len(sys.argv) > 1 else "cap19"
SAIDAS = Path(__file__).resolve().parents[1] / "saidas"
BASE = "http://localhost:5173"
ANA = ("ana@hospital.dev", "cajueiro-em-flor-no-quintal")


def fuso_para(hora):
    """TZ POSIX em que agora são `hora` horas (o sinal é invertido)."""
    utc = datetime.datetime.now(datetime.timezone.utc).hour
    d = (hora - utc + 12) % 24 - 12
    return f"Etc/GMT{-d:+d}" if d else "Etc/GMT", (utc + d) % 24


def grava(nome, linhas):
    texto = "\n".join(linhas) + "\n"
    (SAIDAS / nome).write_text(texto)
    print(f"== {nome}\n{texto}")


def passos():
    log = subprocess.run(["git", "-C", str(WEB), "log", "--oneline",
                          "--reverse", f"cap16..{REV}"],
                         capture_output=True, text=True, check=True)
    # no livro, só o assunto até os dois-pontos (a mensagem inteira
    # está no repositório)
    linhas = [f"$ git log --oneline --reverse cap16..{REV}"]
    for l in log.stdout.splitlines():
        h, _, msg = l.partition(" ")
        linhas.append(f"{h[:7]} {msg.split(': ')[0]}")
    grava("c19-passos.txt", linhas)


def recepcao_abre_ficha(rev):
    """Carla (recepção) abre a ficha e1. Anota a rede e o que aparece."""
    out = [f"tela {rev} · recepção abre /atendimentos/e1"]
    with sessao_api(rev) as (pg, _v):
        rede = []
        pg.on("response", lambda r: "5173/api/" in r.url and rede.append(
            f"  {r.request.method} {r.url.split('5173')[1]} → {r.status}"))
        pg.goto(BASE + "/atendimentos/e1")
        pg.wait_for_timeout(1500)
        out += sorted(set(rede))
        ficha = pg.get_by_role("article", name="Atendimento")
        if ficha.count():
            txt = ficha.inner_text()
        else:
            txt = pg.locator("main > section").last.inner_text()
        out.append("  na tela:")
        out += ["    " + l.strip() for l in txt.splitlines()
                if l.strip()][:9]
    return out


def ana_prescreve(fuso, hora):
    out = [f"API com TZ={fuso}: são {hora:02d}h na API"]
    with api("cap19", fuso=fuso), sessao(REV, porta=5173) as (pg, _v):
        pg.goto(BASE + "/entrar")
        pg.get_by_label("E-mail").fill(ANA[0])
        pg.get_by_label("Senha").fill(ANA[1])
        pg.get_by_role("button", name="Entrar").click()
        pg.wait_for_timeout(700)
        st = []
        pg.on("response", lambda r: r.request.method == "POST" and
              "medication" in r.url and st.append(
              (r.status, r.url.split("5173")[1])))
        pg.goto(BASE + "/atendimentos/e1")
        ficha = pg.get_by_role("article", name="Atendimento")
        form = ficha.get_by_role("form", name="Nova prescrição")
        form.get_by_label("Medicamento").fill("Dipirona 500 mg")
        form.get_by_label("Posologia").fill("6/6h se dor")
        form.get_by_role("button", name="Prescrever").click()
        pg.wait_for_timeout(1000)
        out.append(f"  POST {st[0][1]}")
        out.append(f"    → {st[0][0]}")
        aviso = ficha.get_by_role("alert")
        lista = ficha.get_by_role("list", name="Prescrições")
        if aviso.count():
            out.append(f"  aviso: {aviso.first.inner_text().strip()}")
        out.append("  prescrições na ficha:")
        out += [f"    {i.strip()}" for i in
                lista.get_by_role("listitem").all_inner_texts()]
        val = form.get_by_label("Medicamento").input_value()
        out.append(f"  campo Medicamento depois: {val!r}")
    return out


def a11y():
    """axe-core (WCAG 2.2 AA) nas rotas novas, como a Dra. Ana."""
    axe = Path(__file__).parent / "node_modules/axe-core/axe.min.js"
    regras = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]
    out = [f"axe-core · tela {REV} · Dra. Ana"]
    with api("cap19", fuso=fuso_para(12)[0]), \
            sessao_api(REV, *ANA) as (pg, _v):
        for rota in ("/atendimentos", "/atendimentos/e1"):
            pg.goto(BASE + rota)
            pg.wait_for_timeout(1200)
            pg.add_script_tag(path=str(axe))
            for tema in ("light", "dark"):
                pg.emulate_media(color_scheme=tema)
                r = pg.evaluate("""(t) => axe.run(document,
                    { runOnly: { type: "tag", values: t } })""", regras)
                v = r["violations"]
                out.append(f"  {rota:<17} {tema:<5} {len(v)} violação(ões)"
                           + "".join(f"; {x['id']}" for x in v))
    grava("c19-a11y.txt", out)


def gate():
    fuso, hora = fuso_para(12)
    pasta = Path(tempfile.mkdtemp(prefix="gate-cap19-"))
    subprocess.run(["git", "-C", str(WEB), "worktree", "add", "--detach",
                    str(pasta), REV], check=True, capture_output=True)
    (pasta / "node_modules").symlink_to(WEB / "node_modules")
    try:
        with api("cap19", fuso=fuso):
            r = subprocess.run(["npm", "run", "gate:completo"], cwd=pasta,
                               capture_output=True, text=True,
                               env={**os.environ, "CI": "1",
                                    "NO_COLOR": "1", "PW_CHROMIUM":
                                    "/opt/pw-browsers/chromium-1194/"
                                    "chrome-linux/chrome"})
    finally:
        subprocess.run(["git", "-C", str(WEB), "worktree", "remove",
                        "--force", str(pasta)], capture_output=True)
    chaves = ("Test Files", "Tests ", "passed", "failed", "✓ built",
              "no dependency violations", "Found 0")
    linhas = [f"$ npm run gate:completo   (tela {REV}; API cap19, "
              f"{hora:02d}h)"]
    for l in re.sub(r"\x1b\[[0-9;]*m", "", r.stdout).splitlines():
        if any(k in l for k in chaves):
            linhas.append(l.strip())
    linhas.append(f"código de saída: {r.returncode}")
    grava("c19-gate.txt", linhas)


if __name__ == "__main__":
    passos()
    with api("cap19", fuso=fuso_para(12)[0]):
        dep = recepcao_abre_ficha("cap19-passo08") + [""] + \
            recepcao_abre_ficha(REV)
    grava("c19-depuracao.txt", dep)
    dia, noite = fuso_para(12), fuso_para(23)
    grava("c19-plantao.txt", ana_prescreve(*dia) + [""]
          + ana_prescreve(*noite))
    a11y()
    gate()
