"""Monta o livro (index.html na raiz) a partir de head.html + pN.html.

uso: cd fonte && python3 build.py      (o PDF sai do pdf.py)

Placeholders aceitos nas partes:
  {{ARTE:nome}}                  cena de abertura (arte.py)
  {{FIG:nome}}                   figura técnica (fonte/fig_nome.svg)
  {{SAIDA:arquivo|opções}}       saída real guardada em saidas/
  {{BLOCO:tag:caminho|opções}}   código do repositório web na tag git
  {{DIFF:tagA:tagB:caminho}}     diferença real entre duas tags

Opções: linhas=a-b · destaque=texto;texto · rotulo=texto
O código impresso sai do git, nunca de cópia: se a tag mudar, o livro
muda junto. Linha de código com mais de 46 caracteres derruba o build.
"""
import html
import os
import re
import subprocess
import sys
from pathlib import Path

import arte

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
SAIDAS = RAIZ / "saidas"
WEB = Path(os.environ.get("ESTADO_WEB", RAIZ.parent / "web"))
API = Path(os.environ.get("ESTADO_API", RAIZ.parent / "api"))
NEXT = Path(os.environ.get("ESTADO_NEXT", RAIZ.parent / "next"))
LARGURA = 46

PALAVRAS = (r"\b(import|from|export|default|function|const|let|return|if|"
            r"else|for|of|await|async|try|catch|type|interface|new|"
            r"continue|true|false|null|undefined)\b")
TOKENS = re.compile(
    r"(?P<c>//[^\n]*|/\*[\s\S]*?\*/|<!--[\s\S]*?-->)"
    r"|(?P<s>\"(?:\\.|[^\"\\\n])*\"|`(?:\\.|[^`\\])*`)"
    rf"|(?P<k>{PALAVRAS})")


def realce(codigo):
    """Realce mínimo e previsível: comentário, string, palavra-chave."""
    out, pos = [], 0
    for m in TOKENS.finditer(codigo):
        out.append(html.escape(codigo[pos:m.start()]))
        classe = m.lastgroup
        out.append(f'<span class="{classe}">{html.escape(m.group(0))}</span>')
        pos = m.end()
    out.append(html.escape(codigo[pos:]))
    return "".join(out)


def opcoes(texto):
    d = {}
    for parte in texto.split("|")[1:]:
        k, _, v = parte.partition("=")
        d[k.strip()] = v.strip()
    return d


def recorte(linhas, faixa):
    if not faixa:
        return linhas
    a, _, b = faixa.partition("-")
    return linhas[int(a) - 1:int(b or a)]


def git_show(repo, tag, caminho):
    r = subprocess.run(["git", "-C", str(repo), "show", f"{tag}:{caminho}"],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"git show {tag}:{caminho} em {repo}: {r.stderr.strip()}")
    return r.stdout


def bloco(arg):
    alvo, op = arg.split("|")[0], opcoes(arg)
    repo = API if alvo.startswith("api@") else \
        NEXT if alvo.startswith("next@") else WEB
    tag, caminho = alvo.removeprefix("api@").removeprefix("next@") \
        .split(":", 1)
    linhas = recorte(git_show(repo, tag, caminho).rstrip("\n").split("\n"),
                     op.get("linhas"))
    for n, l in enumerate(linhas, 1):
        if len(l) > LARGURA:
            sys.exit(f"linha com {len(l)} caracteres em {tag}:{caminho} "
                     f"(trecho, linha {n}): {l}")
    rotulo = op.get("rotulo", caminho)
    corpo = realce("\n".join(linhas))
    if "linhas" in op:
        corpo = '<span class="c">…</span>\n' + corpo + '\n<span class="c">…</span>' \
            if op.get("reticencias") == "sim" else corpo
    return (f'<div class="term"><div class="term-bar"><span class="arq">'
            f'{html.escape(rotulo)}</span><span class="tag-git">{tag}</span>'
            f'</div><pre>{corpo}</pre></div>')


def diff(arg):
    a, b, caminho = arg.split(":", 2)
    r = subprocess.run(["git", "-C", str(WEB), "diff", "-U1", a, b, "--",
                        caminho], capture_output=True, text=True)
    linhas = [l for l in r.stdout.split("\n")
              if l and not l.startswith(("diff ", "index ", "--- ", "+++ "))]
    out = []
    for l in linhas:
        t = html.escape(l)
        if l.startswith("@@"):
            out.append('<span class="c">…</span>')
        elif l.startswith("-"):
            out.append(f'<span class="w">{t}</span>')
        elif l.startswith("+"):
            out.append(f'<span class="s">{t}</span>')
        else:
            out.append(t)
    return (f'<div class="term"><div class="term-bar"><span class="arq">'
            f'{html.escape(caminho)}</span><span class="tag-git">{a} → {b}'
            f'</span></div><pre>{chr(10).join(out)}</pre></div>')


def saida(arg):
    arquivo, op = arg.split("|")[0], opcoes(arg)
    texto = (SAIDAS / arquivo).read_text(encoding="utf-8").rstrip("\n")
    linhas = [l for l in recorte(texto.split("\n"), op.get("linhas"))]
    if op.get("sem_vazias") == "sim":
        linhas = [l for l in linhas if l.strip()]
    t = html.escape("\n".join(linhas))
    for d in filter(None, op.get("destaque", "").split(";")):
        t = t.replace(html.escape(d), f'<span class="w">{html.escape(d)}</span>')
    return t


def figura(nome):
    return (AQUI / f"fig_{nome}.svg").read_text(encoding="utf-8")


def pagina(cap):
    """Página de abertura medida no PDF anterior (medir.py --json)."""
    arq = SAIDAS / "paginas.json"
    if not arq.exists():
        return "p. —"
    import json
    p = json.loads(arq.read_text()).get(cap)
    return f"p. {p}" if p else "p. —"


def resolver(chave):
    tipo, _, arg = chave.partition(":")
    if tipo == "PAG":
        return pagina(arg)
    if tipo == "ARTE":
        return getattr(arte, arg)()
    if tipo == "FIG":
        return figura(arg)
    if tipo == "SAIDA":
        return saida(arg)
    if tipo == "BLOCO":
        return bloco(arg)
    if tipo == "DIFF":
        return diff(arg)
    sys.exit(f"placeholder desconhecido: {chave}")


SCRIPT = """
<script>
document.addEventListener('click', async (e) => {
  const b = e.target.closest('button.copy');
  if (!b) return;
  const el = document.getElementById(b.dataset.copy);
  if (!el) return;
  const label = b.textContent;
  try { await navigator.clipboard.writeText(el.textContent.trim()); b.textContent = 'Copiado'; }
  catch (err) {
    const r = document.createRange(); r.selectNodeContents(el);
    const s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
    b.textContent = 'Selecionado';
  }
  setTimeout(() => { b.textContent = label; }, 1600);
});
</script>"""


def main():
    partes = sorted(AQUI.glob("p[0-9]*.html"),
                    key=lambda f: int(re.findall(r"\d+", f.name)[0]))
    corpo = "\n".join(f.read_text(encoding="utf-8") for f in partes)
    chaves = re.findall(r"\{\{([^{}]+)\}\}", corpo)
    for chave in dict.fromkeys(chaves):
        corpo = corpo.replace("{{" + chave + "}}", resolver(chave))

    # tabela sempre dentro de .tbl-wrap (rola sozinha no celular)
    soltas = len(re.findall(r"<table", corpo)) - len(
        re.findall(r'<div class="tbl-wrap[^"]*"><table', corpo))
    if soltas:
        sys.exit(f"{soltas} tabela(s) fora de <div class=\"tbl-wrap\">")

    def marcar_curto(m):
        b = m.group(0)
        pre = re.search(r"<pre[^>]*>(.*?)</pre>", b, re.S)
        if pre and pre.group(1).count("\n") < 12:
            return b.replace('<div class="term">', '<div class="term t-curto">', 1)
        return b
    corpo = re.sub(r'<div class="term">.*?</pre>', marcar_curto, corpo, flags=re.S)

    head = (AQUI / "head.html").read_text(encoding="utf-8")
    (RAIZ / "index.html").write_text(head + corpo + "\n</div>\n" + SCRIPT,
                                     encoding="utf-8")
    print(f"{len(partes)} partes · {len(set(chaves))} placeholders")


if __name__ == "__main__":
    main()
