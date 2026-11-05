#!/usr/bin/env python3
"""Gera a edição EPUB 3 do livro a partir do site (index.html) e da capa do PDF.

    pip install beautifulsoup4 html5lib pillow   # e o poppler (pdftoppm) para a capa
    python epub.py

Cada capítulo (section.chapter) vira um arquivo XHTML; as figuras SVG seguem
embutidas, a capa é a página 1 do PDF e o sumário é navegável no leitor.
O site continua sendo a fonte: rode este script depois de gerar index.html.
Adaptado do epub.py do Crachá & Porta.
"""
from __future__ import annotations

import datetime as dt
import html
import re
import subprocess
import sys
import tempfile
import uuid
import zipfile
from pathlib import Path

from bs4 import BeautifulSoup, Tag
from PIL import Image, ImageOps

# ------------------------------------------------------------------ CONFIG
CONFIG = {
    "titulo": "Estado & Tela",
    "subtitulo": "Aplicações web reativas com React, do DOM manipulado à mão até uma aplicação completa, autenticada e testada, construída com agentes de IA sem perder o controle do código.",
    "autores": [
        "Rogério Silva",
        "Claude Opus 5.5"
    ],
    "ano": "2026",
    "licenca": "Conteúdo (texto, figuras, ilustrações e estrutura) sob CC BY-SA 4.0. Código e instrumentos sob MIT.",
    "pdf": "Estado-e-Tela.pdf",
    "epub": "Estado-e-Tela.epub",
    "site": "https://rogeriosilva-ifpi.github.io/estado-e-tela-ebook/",
    "repo": "https://github.com/rogeriosilva-ifpi/estado-e-tela-ebook"
}
# --------------------------------------------------------------------------

RAIZ = Path(__file__).resolve().parent
XHTML_NS = "http://www.w3.org/1999/xhtml"
EPUB_NS = "http://www.idpf.org/2007/ops"


# ---------------------------------------------------------------- CSS

def ler_css(soup: BeautifulSoup) -> str:
    """CSS de tela do site: <link> locais (com @import resolvido) e <style>."""
    partes = []
    for el in soup.find_all(["link", "style"]):
        if el.name == "style":
            partes.append("".join(str(t) for t in el.contents))  # get_text() ignora <style>
        elif "stylesheet" in (el.get("rel") or []) and el.get("media", "all") in ("all", "screen"):
            href = el.get("href", "")
            if href.startswith(("http:", "https:", "//")):
                continue
            partes.append(resolver_imports((RAIZ / href).read_text(encoding="utf-8"), RAIZ / href))
    return "\n".join(partes)


def resolver_imports(css: str, origem: Path) -> str:
    def troca(m: re.Match) -> str:
        alvo = origem.parent / m.group(1)
        return resolver_imports(alvo.read_text(encoding="utf-8"), alvo) if alvo.exists() else ""
    return re.sub(r'@import\s+(?:url\()?["\']([^"\']+)["\']\)?\s*;', troca, css)


def remover_blocos(css: str, cabecalho: re.Pattern) -> str:
    """Remove blocos { } cujo cabeçalho casa o padrão, respeitando chaves aninhadas."""
    saida, i = [], 0
    while True:
        m = cabecalho.search(css, i)
        if not m:
            saida.append(css[i:])
            return "".join(saida)
        abre = css.find("{", m.end())
        if abre < 0:
            saida.append(css[i:])
            return "".join(saida)
        saida.append(css[i:m.start()])
        nivel, j = 1, abre + 1
        while j < len(css) and nivel:
            nivel += {"{": 1, "}": -1}.get(css[j], 0)
            j += 1
        i = j


def css_para_epub(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"@import[^;]+;", "", css)
    # Fontes, tema escuro, impressão e animação ficam com o leitor de EPUB.
    css = remover_blocos(css, re.compile(r"@font-face"))
    css = remover_blocos(css, re.compile(r"@media[^{]*(prefers-color-scheme|print|prefers-reduced-motion)[^{]*"))
    css = remover_blocos(css, re.compile(r"@page[^{]*"))
    css = remover_blocos(css, re.compile(r"[^{}]*\[data-theme=[\"']?dark[\"']?\][^{}]*"))
    css = re.sub(r"\n\s*\n+", "\n", css).strip()
    return css + "\n\n/* ---- ajustes da edição EPUB ---- */\n" + CSS_EPUB


CSS_EPUB = """
html, body { background: transparent; }
body { max-width: none !important; margin: 0 !important; padding: 0 !important; }
section.chapter { margin: 0; padding: 0; }
.chapter-open { margin-top: 0; padding-top: 0; }
.chapter-open h1 { font-size: 1.9em; line-height: 1.12; }
.chapter-open .num { font-size: 2.6em; line-height: 1; }
h2 { font-size: 1.3em; line-height: 1.25; }
h3 { font-size: 1.1em; line-height: 1.3; }
pre, pre code { white-space: pre-wrap; word-wrap: break-word; overflow-wrap: anywhere; }
pre { font-size: 0.78em; line-height: 1.45; }
figure { margin: 1.2em 0; page-break-inside: avoid; break-inside: avoid; }
figure svg, .fig-frame svg { width: 100%; height: auto; max-width: 100%; }
table { font-size: 0.85em; }
.tbl-wrap { overflow: visible; }
.topbar, .totop, .sitefoot, button, nav.topbar { display: none !important; }
.capa-ebook { margin: 0; padding: 0; text-align: center; }
.capa-ebook img { max-width: 100%; max-height: 100%; }
nav#toc ol { list-style: none; padding-left: 0; margin: 0; }
nav#toc ol ol { padding-left: 1.1em; margin: .25em 0 .6em; font-size: .92em; }
nav#toc li { margin: .3em 0; }
.colofao { font-size: 0.9em; line-height: 1.55; }
.colofao h1 { font-size: 1.6em; line-height: 1.15; margin: 0 0 .3em; }
.colofao .sub { margin: 0 0 1.4em; }
.colofao p { margin: 0 0 .8em; }
.colofao .rotulo { font-size: .72em; letter-spacing: .12em; text-transform: uppercase; font-weight: 700; margin: 1.6em 0 .3em; }
"""


# ---------------------------------------------------------------- XHTML

def limpar(no: Tag) -> None:
    for el in no.find_all(["script", "button", "noscript"]):
        el.decompose()
    for el in no.find_all(True):
        for attr in list(el.attrs):
            if attr.startswith("on") or attr in ("tabindex",):
                del el[attr]


def prefixar_ids_svg(secao: Tag, prefixo: str) -> None:
    """Ids dentro de cada SVG ganham prefixo próprio, evitando ids repetidos no arquivo."""
    for n, svg in enumerate(secao.find_all("svg")):
        ids = [el["id"] for el in svg.find_all(id=True)]
        if not ids:
            continue
        mapa = {i: f"{prefixo}s{n}-{i}" for i in ids}
        for el in [svg, *svg.find_all(True)]:
            for attr, val in list(el.attrs.items()):
                if not isinstance(val, str):
                    continue
                if attr == "id" and val in mapa:
                    el[attr] = mapa[val]
                    continue
                novo = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{mapa.get(m.group(1), m.group(1))})", val)
                if attr in ("href", "xlink:href") and novo.startswith("#") and novo[1:] in mapa:
                    novo = "#" + mapa[novo[1:]]
                el[attr] = novo


def serializar(no: Tag) -> str:
    return no.decode(formatter="minimal")


def pagina(titulo: str, corpo: str, tipo: str = "", lang: str = "pt-BR") -> str:
    tipo_attr = f' epub:type="{tipo}"' if tipo else ""
    return (f'<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
            f'<html xmlns="{XHTML_NS}" xmlns:epub="{EPUB_NS}" lang="{lang}" xml:lang="{lang}">\n'
            f'<head>\n<meta charset="utf-8"/>\n<title>{html.escape(titulo)}</title>\n'
            f'<link rel="stylesheet" type="text/css" href="estilo.css"/>\n</head>\n'
            f'<body{tipo_attr}>\n{corpo}\n</body>\n</html>\n')


def checar_xml(nome: str, conteudo: str) -> None:
    from xml.etree import ElementTree as ET
    try:
        ET.fromstring(conteudo.encode("utf-8"))
    except ET.ParseError as e:
        linha = conteudo.splitlines()[e.position[0] - 1]
        sys.exit(f"{nome}: XHTML malformado ({e}):\n  {linha[max(0, e.position[1] - 80):e.position[1] + 80]}")


# ---------------------------------------------------------------- capa

def gerar_capa(destino: Path) -> None:
    pdf = RAIZ / CONFIG["pdf"]
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-f", "1", "-l", "1", "-r", "220", "-png", str(pdf), f"{tmp}/capa"],
                       check=True, stderr=subprocess.DEVNULL)
        png = next(Path(tmp).glob("capa*.png"))
        im = Image.open(png).convert("RGB")
        caixa = ImageOps.invert(im).getbbox()  # remove margem branca da página
        if caixa:
            im = im.crop(caixa)
        largura = 1000
        im = im.resize((largura, round(im.size[1] * largura / im.size[0])), Image.LANCZOS)
        im.save(destino, "JPEG", quality=88, optimize=True, progressive=True)


# ---------------------------------------------------------------- montagem

def texto(el: Tag | None) -> str:
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip() if el else ""


def main() -> None:
    fonte = RAIZ / "index.html"
    soup = BeautifulSoup(fonte.read_text(encoding="utf-8"), "html5lib")
    css = css_para_epub(ler_css(soup))
    capitulos = soup.select("section.chapter")
    if not capitulos:
        sys.exit("Nenhuma section.chapter encontrada em index.html")

    # 1) arquivo de cada capítulo e mapa id -> arquivo, para reescrever links internos
    arquivos, onde = [], {}
    for n, sec in enumerate(capitulos, 1):
        nome = f"cap{n:02d}.xhtml"
        arquivos.append(nome)
        if not sec.get("id"):
            sec["id"] = f"cap-{n:02d}"
        for el in [sec, *sec.find_all(id=True)]:
            onde.setdefault(el["id"], nome)
    for sec_id in [s.get("id") for s in soup.select("section.toc, section.cover") if s.get("id")]:
        onde.setdefault(sec_id, "nav.xhtml")

    # 2) sumário: capítulo + seções (h2)
    navegacao = []
    for n, (sec, nome) in enumerate(zip(capitulos, arquivos), 1):
        limpar(sec)
        prefixar_ids_svg(sec, f"c{n}")
        h1 = sec.find("h1")
        num = texto(sec.select_one(".chapter-open .num"))
        titulo = texto(h1) or f"Capítulo {n}"
        rotulo = f"{num} · {titulo}" if num and not titulo.startswith(num) else titulo
        subs = []
        for k, h2 in enumerate(sec.find_all("h2"), 1):
            if not h2.get("id"):
                h2["id"] = f"c{n}-s{k}"
            subs.append((texto(h2), f'{nome}#{h2["id"]}'))
        navegacao.append((rotulo, f'{nome}#{sec["id"]}', subs, titulo))

    for a in soup.select('a[href^="#"]'):
        alvo = a["href"][1:]
        if alvo in onde:
            a["href"] = f'{onde[alvo]}#{alvo}'
        else:
            a.unwrap()

    paginas = {}
    for (rotulo, _, _, titulo), sec, nome in zip(navegacao, capitulos, arquivos):
        sec.name = "section"
        sec["epub:type"] = "chapter"
        paginas[nome] = pagina(titulo, serializar(sec))

    agora = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    ident = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, CONFIG["repo"]))
    autores = CONFIG["autores"]
    e = html.escape

    paginas["capa.xhtml"] = pagina(CONFIG["titulo"], (
        '<section class="capa-ebook" epub:type="cover">'
        f'<img src="capa.jpg" alt="Capa: {e(CONFIG["titulo"])}"/></section>'), tipo="cover")

    paginas["colofao.xhtml"] = pagina("Sobre esta edição", f"""<section class="colofao" epub:type="colophon">
<h1>{e(CONFIG['titulo'])}</h1>
<p class="sub">{e(CONFIG['subtitulo'])}</p>
<p>Organizado por {e(' e '.join(['Prof. ' + autores[0], *autores[1:]]))} · {e(CONFIG['ano'])}</p>
<p class="rotulo">Edição EPUB</p>
<p>Gerada a partir do site do livro em {agora:%d/%m/%Y}. O conteúdo é o mesmo do site e do PDF; o EPUB se ajusta ao tamanho da tela e às preferências de fonte do seu leitor.</p>
<p class="rotulo">Onde mais ler</p>
<p>Site: <a href="{e(CONFIG['site'])}">{e(CONFIG['site'])}</a><br/>
Repositório, PDF e material: <a href="{e(CONFIG['repo'])}">{e(CONFIG['repo'])}</a><br/>
Todos os livros: <a href="https://rogeriosilva-ifpi.github.io/">rogeriosilva-ifpi.github.io</a></p>
<p class="rotulo">Licença</p>
<p>{e(CONFIG['licenca'])}</p>
</section>""", tipo="frontmatter")

    itens_nav = "\n".join(
        f'<li><a href="{href}">{e(rot)}</a>'
        + ("<ol>" + "".join(f'<li><a href="{h}">{e(t)}</a></li>' for t, h in subs) + "</ol>" if subs else "")
        + "</li>" for rot, href, subs, _ in navegacao)
    paginas["nav.xhtml"] = pagina("Sumário", f"""<nav epub:type="toc" id="toc">
<h1>Sumário</h1>
<ol>
<li><a href="colofao.xhtml">Sobre esta edição</a></li>
{itens_nav}
</ol>
</nav>
<nav epub:type="landmarks" hidden="hidden">
<ol>
<li><a epub:type="cover" href="capa.xhtml">Capa</a></li>
<li><a epub:type="toc" href="nav.xhtml">Sumário</a></li>
<li><a epub:type="bodymatter" href="{arquivos[0]}">Início do texto</a></li>
</ol>
</nav>""")

    for nome, conteudo in paginas.items():
        checar_xml(nome, conteudo)

    # NCX para leitores antigos (EPUB 2), em ordem de leitura
    seq = 1
    ncx_pontos = ['<navPoint id="np1" playOrder="1"><navLabel><text>Sobre esta edição</text></navLabel><content src="colofao.xhtml"/></navPoint>']
    for rot, href, subs, _ in navegacao:
        seq += 1
        filhos = []
        for t, h in subs:
            seq += 1
            filhos.append(f'<navPoint id="np{seq}" playOrder="{seq}"><navLabel><text>{e(t)}</text></navLabel><content src="{h}"/></navPoint>')
        inicio = seq - len(subs)
        ncx_pontos.append(f'<navPoint id="np{inicio}" playOrder="{inicio}"><navLabel><text>{e(rot)}</text></navLabel><content src="{href}"/>{"".join(filhos)}</navPoint>')
    ncx = (f'<?xml version="1.0" encoding="utf-8"?>\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">'
           f'<head><meta name="dtb:uid" content="{ident}"/></head><docTitle><text>{e(CONFIG["titulo"])}</text></docTitle>'
           f'<navMap>{"".join(ncx_pontos)}</navMap></ncx>\n')

    def ident_item(nome: str) -> str:
        return "nav" if nome == "nav.xhtml" else nome.replace(".", "-")

    def props(nome: str) -> str:
        p = (["nav"] if nome == "nav.xhtml" else []) + (["svg"] if "<svg" in paginas[nome] else [])
        return f' properties="{" ".join(p)}"' if p else ""

    ordem_spine = ["capa.xhtml", "colofao.xhtml", "nav.xhtml", *arquivos]
    manifesto = "\n".join(
        [f'<item id="{ident_item(n)}" href="{n}" media-type="application/xhtml+xml"{props(n)}/>' for n in ordem_spine]
        + ['<item id="estilo" href="estilo.css" media-type="text/css"/>',
           '<item id="capa-img" href="capa.jpg" media-type="image/jpeg" properties="cover-image"/>',
           '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>'])
    spine = "\n".join(
        f'<itemref idref="{ident_item(n)}"{" linear=\"no\"" if n == "nav.xhtml" else ""}/>' for n in ordem_spine)
    criadores = "\n".join(f'<dc:creator id="autor{i}">{e(a)}</dc:creator>' for i, a in enumerate(autores))
    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="pt-BR">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">{ident}</dc:identifier>
<dc:title>{e(CONFIG['titulo'])}</dc:title>
<dc:description>{e(CONFIG['subtitulo'])}</dc:description>
{criadores}
<dc:language>pt-BR</dc:language>
<dc:date>{e(CONFIG['ano'])}</dc:date>
<dc:rights>{e(CONFIG['licenca'])}</dc:rights>
<dc:source>{e(CONFIG['site'])}</dc:source>
<meta property="dcterms:modified">{agora:%Y-%m-%dT%H:%M:%SZ}</meta>
<meta name="cover" content="capa-img"/>
</metadata>
<manifest>
{manifesto}
</manifest>
<spine toc="ncx">
{spine}
</spine>
</package>
"""

    with tempfile.TemporaryDirectory() as tmp:
        capa = Path(tmp) / "capa.jpg"
        gerar_capa(capa)
        destino = RAIZ / CONFIG["epub"]
        with zipfile.ZipFile(destino, "w") as z:
            z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
            z.writestr("META-INF/container.xml",
                       '<?xml version="1.0" encoding="utf-8"?>\n<container version="1.0" '
                       'xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles>'
                       '<rootfile full-path="OEBPS/livro.opf" media-type="application/oebps-package+xml"/>'
                       '</rootfiles></container>\n', compress_type=zipfile.ZIP_DEFLATED)
            z.writestr("OEBPS/livro.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
            z.writestr("OEBPS/toc.ncx", ncx, compress_type=zipfile.ZIP_DEFLATED)
            z.writestr("OEBPS/estilo.css", css, compress_type=zipfile.ZIP_DEFLATED)
            z.write(capa, "OEBPS/capa.jpg", compress_type=zipfile.ZIP_STORED)
            for nome, conteudo in paginas.items():
                z.writestr(f"OEBPS/{nome}", conteudo, compress_type=zipfile.ZIP_DEFLATED)
    kb = destino.stat().st_size // 1024
    print(f"{CONFIG['epub']}: {len(arquivos)} capítulos, {kb} KB")


if __name__ == "__main__":
    main()
