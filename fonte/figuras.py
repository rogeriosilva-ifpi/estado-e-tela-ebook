"""Gera as figuras técnicas desenhadas por código (fig_*.svg).

As cores vêm das classes do head.html (f-*, s-*), nunca de hexadecimal,
para acompanhar o tema claro e escuro.
"""
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def t(x, y, txt, tam=11, cls="f-soft", peso=None, mono=False, anc=None):
    a = f' text-anchor="{anc}"' if anc else ""
    p = f' font-weight="{peso}"' if peso else ""
    m = " mono" if mono else ""
    return f'<text x="{x}" y="{y}" font-size="{tam}"{p}{a} class="{cls}{m}">{txt}</text>'


def r(x, y, w, h, cls, rx=6, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"{extra}/>'


def seta(x1, y1, x2, y2, cls="s-mut"):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-width="1.6" class="{cls}"/>'
            f'<path d="M{x2-4} {y2-6} L{x2} {y2} L{x2+4} {y2-6}" fill="none" stroke-width="1.6" class="{cls}"/>')


def fig_proxy():
    s = []
    s.append(r(0, 0, 400, 50, "f-alt"))
    s.append(t(14, 20, "NAVEGADOR", 9.5, "f-mut", 800))
    s.append(t(14, 39, "http://localhost:5173", 13, "f-ink", 700, mono=True))
    s.append(seta(200, 50, 200, 76))
    s.append(r(0, 76, 400, 132, "f-accs s-accl", extra=' stroke-width="1.2"'))
    s.append(t(14, 96, "VITE · SERVIDOR DE DESENVOLVIMENTO · :5173", 9.5, "f-acc", 800))
    s.append(r(14, 108, 178, 86, "f-card s-bord", extra=' stroke-width="1"'))
    s.append(t(26, 128, "/src/main.tsx …", 11, "f-ink", 700, mono=True))
    s.append(t(26, 148, "transforma TSX em JS", 10.5))
    s.append(t(26, 164, "e devolve o módulo;", 10.5))
    s.append(t(26, 180, "salvou, a tela troca", 10.5))
    s.append(r(208, 108, 178, 86, "f-card s-bord", extra=' stroke-width="1"'))
    s.append(t(220, 128, "/api/…  /health", 11, "f-ink", 700, mono=True))
    s.append(t(220, 148, "não responde: repassa", 10.5))
    s.append(t(220, 164, "para a API e devolve", 10.5))
    s.append(t(220, 180, "a resposta como é", 10.5))
    s.append(seta(297, 194, 297, 234))
    s.append(r(0, 234, 400, 56, "f-infos s-infol", extra=' stroke-width="1.2"'))
    s.append(t(14, 254, "API EXPRESS DO CRACHÁ &amp; PORTA · :3000", 9.5, "f-info", 800))
    s.append(t(14, 274, "sessão, permissões, pacientes", 11.5, "f-ink", 700))
    s.append(t(0, 314, "Para o navegador existe uma origem só. O cookie", 11, "f-soft"))
    s.append(t(0, 331, "de sessão vai junto e não há CORS no caminho.", 11, "f-soft"))
    return f'<svg viewBox="0 0 400 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="O proxy do Vite: tela e API na mesma origem">{"".join(s)}</svg>'


def linha_dom(x, y, rotulo_key, nome, nota, estado=None):
    """Uma <li> desenhada: key, nome e o campo de anotação."""
    s = []
    cls = {"erro": "f-bads s-badl", "ok": "f-goods s-goodl", "sai": "f-alt s-bord"}.get(estado, "f-card s-bord")
    s.append(r(x, y, 186, 30, cls, 5, ' stroke-width="1"'))
    s.append(t(x + 8, y + 19, rotulo_key, 9.5, "f-acc", 700, mono=True))
    s.append(t(x + 44, y + 19, nome, 10.5, "f-ink" if estado != "sai" else "f-mut", 700))
    s.append(r(x + 118, y + 7, 62, 16, "f-bg s-bord", 3, ' stroke-width="1"'))
    if nota:
        s.append(t(x + 123, y + 19, nota, 9.5, "f-bad" if estado == "erro" else "f-ink", 600, mono=True))
    return "".join(s)


def fig_chaves():
    s = []
    # painel A
    s.append(t(0, 14, "KEY = ÍNDICE", 9.5, "f-bad", 800))
    s.append(t(0, 34, "antes", 10, "f-mut", 700))
    s.append(t(206, 34, "depois da alta de Maria", 10, "f-mut", 700))
    a = [("0", "Maria", ""), ("1", "João", "ver febre"), ("2", "Ana Clara", "")]
    d = [("0", "João", "", "erro"), ("1", "Ana Clara", "ver febre", "erro"), ("2", "Pedro", "", None)]
    for i, (k, n, nota) in enumerate(a):
        s.append(linha_dom(0, 42 + i * 36, k, n, nota))
    for i, (k, n, nota, e) in enumerate(d):
        s.append(linha_dom(206 + 0, 42 + i * 36, k, n, nota, e))
    s.append(t(0, 166, "A nota fica presa à posição 1. Quem está lá agora é", 10.5, "f-soft"))
    s.append(t(0, 182, "Ana Clara, e João perdeu o que você escreveu.", 10.5, "f-soft"))
    s.append(f'<line x1="0" y1="198" x2="400" y2="198" stroke-dasharray="2 4" stroke-width="1" class="s-bord"/>')
    # painel B
    y0 = 218
    s.append(t(0, y0, "KEY = ID DO PACIENTE", 9.5, "f-good", 800))
    s.append(t(0, y0 + 20, "antes", 10, "f-mut", 700))
    s.append(t(206, y0 + 20, "depois da alta de Maria", 10, "f-mut", 700))
    a = [("p1", "Maria", ""), ("p2", "João", "ver febre"), ("p3", "Ana Clara", "")]
    d = [("p1", "Maria", "", "sai"), ("p2", "João", "ver febre", "ok"), ("p3", "Ana Clara", "", None)]
    for i, (k, n, nota) in enumerate(a):
        s.append(linha_dom(0, y0 + 28 + i * 36, k, n, nota))
    for i, (k, n, nota, e) in enumerate(d):
        s.append(linha_dom(206, y0 + 28 + i * 36, k, n, nota, e))
    s.append(f'<line x1="212" y1="{y0+43}" x2="318" y2="{y0+43}" stroke-width="1.6" class="s-mut"/>')
    s.append(t(0, y0 + 152, "Cada nota acompanha o seu paciente. Só a linha de", 10.5, "f-soft"))
    s.append(t(0, y0 + 168, "Maria sai do DOM; as outras nem são tocadas.", 10.5, "f-soft"))
    return f'<svg viewBox="0 0 400 {y0+176}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Key por índice versus key por id na alta de um paciente">{"".join(s)}</svg>'


PAPEL = {"coordena": ("f-accs s-accl", "f-acc"),
         "moldura": ("f-infos s-infol", "f-info"),
         "apresenta": ("f-goods s-goodl", "f-good")}


def fig_arvore():
    s = []
    nos = [  # (nível, nome, papel, o que sabe)
        (0, "Ala", "coordena", "busca, pacientes, derivados"),
        (1, "Painel · Resumo", "moldura", "só o título"),
        (2, "ResumoAla", "apresenta", "recebe pacientes"),
        (1, "Painel · Pacientes", "moldura", "só o título"),
        (2, "BarraBusca", "apresenta", "valor e onMudar"),
        (2, "ListaPacientes", "apresenta", "pacientes e onAlta"),
        (3, "CartaoPaciente ×6", "apresenta", "um paciente"),
        (4, "SeloRisco", "apresenta", "um risco"),
    ]
    y = 6
    pos = []
    for nivel, nome, papel, sabe in nos:
        x = nivel * 22
        cls, txt = PAPEL[papel]
        w = 196 - nivel * 22 + 22 * 0
        s.append(r(x, y, 200 - nivel * 22, 28, cls, 6, ' stroke-width="1.1"'))
        s.append(t(x + 10, y + 18, nome, 11, "f-ink", 700, mono=True))
        s.append(t(212, y + 12, papel.upper(), 8.5, txt, 800))
        s.append(t(212, y + 24, sabe, 10, "f-soft"))
        pos.append((nivel, x, y))
        y += 36
    # conectores da árvore
    for i, (nivel, x, yy) in enumerate(pos):
        if nivel == 0:
            continue
        pai = max(j for j in range(i) if pos[j][0] == nivel - 1)
        px = pos[pai][1] + 10
        s.append(f'<path d="M{px} {pos[pai][2]+28} V{yy+14} H{x}" fill="none" stroke-width="1.2" class="s-mut"/>')
    s.append(t(0, y + 14, "Quem coordena guarda estado. Quem apresenta recebe", 10.5, "f-soft"))
    s.append(t(0, y + 30, "props. A moldura não sabe o que carrega.", 10.5, "f-soft"))
    h = y + 38
    return f'<svg viewBox="0 0 400 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Árvore de componentes da Ala com o papel de cada um">{"".join(s)}</svg>'


def fig_fluxo():
    s = []
    s.append(r(0, 0, 400, 64, "f-accs s-accl", 8, ' stroke-width="1.2"'))
    s.append(t(14, 20, "ALA · COORDENA", 9.5, "f-acc", 800))
    s.append(t(14, 39, "estado: pacientes, selecionadoId", 11, "f-ink", 700, mono=True))
    s.append(t(14, 55, "derivado: visiveis, selecionado", 11, "f-soft", mono=True))
    # setas de props descendo
    s.append(seta(90, 64, 90, 104, "s-good"))
    s.append(seta(310, 64, 310, 104, "s-good"))
    s.append(t(98, 88, "props", 10, "f-good", 700))
    s.append(t(318, 88, "props", 10, "f-good", 700))
    s.append(r(0, 104, 196, 50, "f-goods s-goodl", 8, ' stroke-width="1.1"'))
    s.append(t(12, 124, "ListaPacientes", 11, "f-ink", 700, mono=True))
    s.append(t(12, 142, "→ CartaoPaciente ×6", 10.5, "f-soft", mono=True))
    s.append(r(212, 104, 188, 50, "f-goods s-goodl", 8, ' stroke-width="1.1"'))
    s.append(t(224, 124, "PainelDetalhe", 11, "f-ink", 700, mono=True))
    s.append(t(224, 142, "paciente={selecionado}", 10, "f-soft", mono=True))
    # evento subindo (tracejado) do cartão até Ala
    s.append(f'<path d="M40 104 V76" fill="none" stroke-width="1.6" stroke-dasharray="4 3" class="s-acc"/>')
    s.append(f'<path d="M36 82 L40 76 L44 82" fill="none" stroke-width="1.6" class="s-acc"/>')
    s.append(t(0, 172, "Dados descem como props. Eventos sobem como", 10.5, "f-soft"))
    s.append(t(0, 188, "chamadas: onSelecionar(id), onPrioridade(id).", 10.5, "f-soft"))
    s.append(f'<line x1="0" y1="204" x2="400" y2="204" stroke-dasharray="2 4" stroke-width="1" class="s-bord"/>')
    # Object.is
    s.append(t(0, 226, "O QUE O REACT COMPARA NO set", 9.5, "f-mut", 800))
    s.append(r(0, 236, 400, 46, "f-bads s-badl", 6, ' stroke-width="1"'))
    s.append(t(12, 254, "p.prioridade = …; setPacientes(pacientes)", 10.5, "f-ink", 700, mono=True))
    s.append(t(12, 272, "mesmo array → Object.is igual → sem render", 10.5, "f-bad", 700))
    s.append(r(0, 290, 400, 46, "f-goods s-goodl", 6, ' stroke-width="1"'))
    s.append(t(12, 308, "setPacientes(pacientes.map(…))", 10.5, "f-ink", 700, mono=True))
    s.append(t(12, 326, "array novo → diferente → render", 10.5, "f-good", 700))
    return f'<svg viewBox="0 0 400 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Fluxo de dados de mão única e a comparação que o React faz no set">{"".join(s)}</svg>'


def fig_envio():
    s = []
    # máquina de estados do envio, em escada vertical
    estados = [
        (0, "ocioso", "f-alt s-bord", "f-ink", "formulário editável"),
        (1, "enviando", "f-warns s-warnl", "f-warn", "botão travado · Enviando…"),
    ]
    s.append(r(130, 0, 140, 34, "f-alt s-bord", 17, ' stroke-width="1.1"'))
    s.append(t(200, 22, "ocioso", 12, "f-ink", 800, anc="middle"))
    s.append(seta(200, 34, 200, 62))
    s.append(t(210, 52, "Admitir", 10, "f-mut", 700))
    s.append(r(130, 62, 140, 34, "f-warns s-warnl", 17, ' stroke-width="1.1"'))
    s.append(t(200, 84, "enviando", 12, "f-warn", 800, anc="middle"))
    # três saídas
    for x, nome, cls, txt, sub in ((0, "inválido", "f-bads s-badl", "f-bad", "400 ou Zod"),
                                    (140, "erro", "f-bads s-badl", "f-bad", "401 · 403 · 409 · 5xx"),
                                    (280, "ok", "f-goods s-goodl", "f-good", "201")):
        s.append(f'<path d="M200 96 L{x+60} 140" fill="none" stroke-width="1.4" class="s-mut"/>')
        s.append(r(x, 140, 120, 34, cls, 17, ' stroke-width="1.1"'))
        s.append(t(x + 60, 162, nome, 12, txt, 800, anc="middle"))
        s.append(t(x + 60, 192, sub, 10, "f-mut", 600, anc="middle", mono=True))
    s.append(t(0, 222, "Inválido e erro voltam ao formulário com o que foi digitado.", 10.5, "f-soft"))
    s.append(t(0, 238, "Enviando vem de pendente; os outros, do tipo Resultado.", 10.5, "f-soft"))
    return f'<svg viewBox="0 0 400 246" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Estados de um envio de formulário">{"".join(s)}</svg>'


def fig_barreiras():
    s = []
    linhas = [
        ("CLIQUE", "f-alt s-bord", "f-ink", "dois cliques no mesmo instante", None),
        ("disabled={pendente}", "f-warns s-warnl", "f-warn", "só depois do próximo render", "aviso visual · passa"),
        ("useRef no onSubmit", "f-goods s-goodl", "f-good", "no instante do clique", "trava a mesma aba"),
        ("409 no servidor", "f-goods s-goodl", "f-good", "CNS já existe", "trava qualquer aba"),
    ]
    y = 0
    for i, (titulo, cls, txt, sub, veredito) in enumerate(linhas):
        s.append(r(0, y, 400, 46, cls, 8, ' stroke-width="1.1"'))
        s.append(t(14, y + 20, titulo, 11.5, "f-ink", 700, mono=True))
        s.append(t(14, y + 37, sub, 10.5, "f-soft"))
        if veredito:
            s.append(t(386, y + 28, veredito, 10.5, txt, 800, anc="end"))
        if i < len(linhas) - 1:
            s.append(seta(200, y + 46, 200, y + 62))
        y += 62
    s.append(t(0, y + 8, "Medido no Chromium com a API real: só disabled deixa", 10.5, "f-soft"))
    s.append(t(0, y + 24, "dois prontuários; o ref segura a aba; o 409 segura o resto.", 10.5, "f-soft"))
    return f'<svg viewBox="0 0 400 {y+32}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="As barreiras contra o envio duplo">{"".join(s)}</svg>'


def fig_efeito():
    s = []
    s.append(t(0, 14, "ESTA LÓGICA PRECISA DE UM EFEITO?", 9.5, "f-mut", 800))
    perguntas = [
        ("Dá para calcular com props e estado?", "calcule no render", "f-goods s-goodl", "f-good"),
        ("Acontece por causa de um clique ou envio?", "ponha no handler", "f-goods s-goodl", "f-good"),
        ("Mantém algo fora do React em dia?", "isso é um efeito", "f-accs s-accl", "f-acc"),
    ]
    y = 26
    for i, (p, r_, cls, txt) in enumerate(perguntas):
        s.append(r(0, y, 248, 40, "f-card s-bord", 6, ' stroke-width="1"'))
        s.append(t(12, y + 25, p, 10.5, "f-ink", 700))
        s.append(f'<line x1="248" y1="{y+20}" x2="262" y2="{y+20}" stroke-width="1.6" class="s-mut"/>'
                 f'<path d="M256 {y+16} L262 {y+20} L256 {y+24}" fill="none" stroke-width="1.6" class="s-mut"/>')
        s.append(r(266, y, 134, 40, cls, 6, ' stroke-width="1.1"'))
        s.append(t(333, y + 25, r_, 10.5, txt, 800, anc="middle"))
        if i < 2:
            s.append(t(14, y + 56, "não", 9.5, "f-mut", 700))
            s.append(f'<line x1="8" y1="{y+40}" x2="8" y2="{y+62}" stroke-width="1.4" class="s-mut"/>')
        y += 62
    y += 6
    s.append(f'<line x1="0" y1="{y}" x2="400" y2="{y}" stroke-dasharray="2 4" stroke-width="1" class="s-bord"/>')
    y += 22
    s.append(t(0, y, "O CICLO DE UM EFEITO COM LIMPEZA", 9.5, "f-mut", 800))
    passos = [("termo = \"ma\"", "setup: pede ?q=ma", "f-infos s-infol"),
              ("termo = \"mar\"", "limpeza: abort(ma) · setup: pede ?q=mar", "f-infos s-infol"),
              ("sai da tela", "limpeza: abort(mar)", "f-alt s-bord")]
    y += 10
    for a, b, cls in passos:
        s.append(r(0, y, 400, 34, cls, 6, ' stroke-width="1"'))
        s.append(t(12, y + 22, a.replace('\\"', '"'), 11, "f-ink", 700, mono=True))
        s.append(t(140, y + 22, b, 10.5, "f-soft", mono=True))
        y += 42
    s.append(t(0, y + 8, "StrictMode roda setup, limpeza e setup na montagem, em dev,", 10.5, "f-soft"))
    s.append(t(0, y + 24, "para provar que a limpeza desfaz o setup.", 10.5, "f-soft"))
    return f'<svg viewBox="0 0 400 {y+32}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Quando usar um efeito e o ciclo de setup e limpeza">{"".join(s)}</svg>'


if __name__ == "__main__":
    for nome, f in (("proxy", fig_proxy), ("chaves", fig_chaves),
                    ("arvore", fig_arvore), ("fluxo", fig_fluxo),
                    ("envio", fig_envio), ("barreiras", fig_barreiras),
                    ("efeito", fig_efeito)):
        (AQUI / f"fig_{nome}.svg").write_text(f() + "\n", encoding="utf-8")
        print("fig_" + nome)
