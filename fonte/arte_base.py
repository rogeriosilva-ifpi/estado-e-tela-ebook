"""Biblioteca de ilustração do Crachá & Porta.

Cenas editoriais geométricas, sempre no mesmo mundo (um hospital à
noite), sempre sobre painel escuro, sem texto. Cada cena é uma função
que devolve um <svg> 400x200 (aberturas) ou livre (capa).
"""
BG, BG2, WALL, LINE, DOOR = "#15171C", "#1B1E23", "#1F2228", "#2E3238", "#262A31"
OR, OR2, AMB = "#C2410C", "#FF8A4C", "#F0A868"
GR, GR2, BLUE = "#2F6B4F", "#7FCBA2", "#9DBDE8"
PAPER, SKIN, GREY, DGREY, RED = "#F2EFE9", "#E8E3DA", "#8A8F99", "#3A3F47", "#E5735F"
FLOOR = 160


_n = [0]


def svg(corpo, w=400, h=200, rotulo="", recorte=True):
    _n[0] += 1
    cid = f"arte{_n[0]}"
    clip = (f'<defs><clipPath id="{cid}"><rect width="{w}" height="{h}" rx="12"/></clipPath></defs>'
            f'<g clip-path="url(#{cid})">{corpo}</g>') if recorte else corpo
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-label="{rotulo}">{clip}</svg>')


def painel(glow_x=300, glow_y=40, piso=True):
    s = [f'<rect width="400" height="200" rx="12" fill="{BG}"/>',
         f'<circle cx="{glow_x}" cy="{glow_y}" r="120" fill="{OR}" opacity=".13"/>',
         f'<circle cx="{glow_x}" cy="{glow_y}" r="60" fill="{OR}" opacity=".10"/>']
    if piso:
        s.append(f'<rect x="0" y="{FLOOR}" width="400" height="{200-FLOOR}" fill="{BG2}"/>')
        s.append(f'<rect x="0" y="{FLOOR}" width="400" height="1.5" fill="{LINE}"/>')
    return "".join(s)


def cruz(x, y, s=14):
    """Placa do hospital: cruz verde."""
    t = s / 3
    return (f'<rect x="{x}" y="{y}" width="{s+8}" height="{s+8}" rx="4" fill="{GR}"/>'
            f'<rect x="{x+4+t}" y="{y+4}" width="{t}" height="{s}" fill="{PAPER}"/>'
            f'<rect x="{x+4}" y="{y+4+t}" width="{s}" height="{t}" fill="{PAPER}"/>')


def luz(x, y, cor, r=3.5):
    if cor is None:
        return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{DGREY}"/>'
    return (f'<circle cx="{x}" cy="{y}" r="{r*4}" fill="{cor}" opacity=".18"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{cor}"/>')


def porta(x, base, w, h, cor_luz=None, aberta=0.0, fechadura="redonda"):
    y = base - h
    s = [f'<rect x="{x-3}" y="{y-3}" width="{w+6}" height="{h+3}" rx="3" fill="{LINE}"/>']
    if aberta:
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{AMB}" opacity=".35"/>')
        s.append(f'<polygon points="{x},{y} {x+w*aberta},{y+6} {x+w*aberta},{base-2} {x},{base}" fill="{DOOR}"/>')
    else:
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{DOOR}"/>')
        s.append(f'<rect x="{x+5}" y="{y+6}" width="{w-10}" height="{h*0.38}" rx="2" fill="{WALL}"/>')
        hx, hy = x + w - 8, y + h * 0.55
        if fechadura == "redonda":
            s.append(f'<circle cx="{hx}" cy="{hy}" r="2.6" fill="{AMB}"/>')
        elif fechadura == "leitor":
            s.append(f'<rect x="{x+w+5}" y="{hy-9}" width="7" height="12" rx="1.5" fill="{DGREY}"/>'
                     f'<rect x="{x+w+6.5}" y="{hy-6}" width="4" height="2" fill="{cor_luz or GREY}"/>')
            s.append(f'<circle cx="{hx}" cy="{hy}" r="2.4" fill="{GREY}"/>')
    s.append(luz(x + w / 2, y - 10, cor_luz))
    return "".join(s)


def pessoa(x, base, cor, s=1.0, jaleco=False):
    """Figura sem rosto: cabeça, tronco, pernas."""
    h_corpo, w_corpo = 40 * s, 22 * s
    top = base - 22 * s - h_corpo
    out = [f'<rect x="{x-w_corpo/2+3*s}" y="{base-22*s}" width="{6*s}" height="{22*s}" rx="{2*s}" fill="{DGREY}"/>',
           f'<rect x="{x+w_corpo/2-9*s}" y="{base-22*s}" width="{6*s}" height="{22*s}" rx="{2*s}" fill="{DGREY}"/>',
           f'<rect x="{x-w_corpo/2}" y="{top}" width="{w_corpo}" height="{h_corpo}" rx="{8*s}" fill="{cor}"/>']
    if jaleco:
        out.append(f'<rect x="{x-1*s}" y="{top+4*s}" width="{2*s}" height="{h_corpo-8*s}" fill="{BG}" opacity=".35"/>')
    out.append(f'<circle cx="{x}" cy="{top-9*s}" r="{8.5*s}" fill="{SKIN}"/>')
    return "".join(out)


def cracha(cx, cy, w=30, h=42, rot=0, brilho=True, faixa=OR):
    x, y = cx - w / 2, cy - h / 2
    g = [f'<g transform="rotate({rot} {cx} {cy})">']
    if brilho:
        g.append(f'<circle cx="{cx}" cy="{cy}" r="{h*0.95}" fill="{OR2}" opacity=".16"/>')
    g += [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{PAPER}"/>',
          f'<rect x="{cx-5}" y="{y-5}" width="10" height="7" rx="2" fill="{GREY}"/>',
          f'<rect x="{x}" y="{y+5}" width="{w}" height="{h*0.18}" fill="{faixa}"/>',
          f'<circle cx="{cx}" cy="{y+h*0.52}" r="{w*0.2}" fill="{DGREY}"/>',
          f'<rect x="{x+5}" y="{y+h*0.76}" width="{w-10}" height="2.4" rx="1" fill="{GREY}"/>',
          f'<rect x="{x+5}" y="{y+h*0.85}" width="{(w-10)*0.6}" height="2.4" rx="1" fill="{GREY}"/>',
          f'<circle cx="{x+w-6}" cy="{y+h-7}" r="3.6" fill="{AMB}"/>',
          '</g>']
    return "".join(g)


def balcao(x, w, h=40):
    return (f'<rect x="{x}" y="{FLOOR-h}" width="{w}" height="{h}" rx="3" fill="{DGREY}"/>'
            f'<rect x="{x-4}" y="{FLOOR-h-5}" width="{w+8}" height="6" rx="2" fill="{GREY}"/>')


def perspectiva(vx=420, vy=110):
    linhas = []
    for x0 in (-40, 60, 160, 260):
        linhas.append(f'<line x1="{x0}" y1="200" x2="{vx}" y2="{vy}" stroke="{LINE}" stroke-width="1"/>')
    return "".join(linhas)


# ---------------------------------------------------------------- cenas

def chave(x, y, s=1.0, cor=AMB, rot=0):
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<circle cx="{x}" cy="{y}" r="{9*s}" fill="none" stroke="{cor}" stroke-width="{4*s}"/>'
            f'<rect x="{x+8*s}" y="{y-2*s}" width="{34*s}" height="{4*s}" rx="1" fill="{cor}"/>'
            f'<rect x="{x+30*s}" y="{y+2*s}" width="{4*s}" height="{7*s}" fill="{cor}"/>'
            f'<rect x="{x+37*s}" y="{y+2*s}" width="{4*s}" height="{5*s}" fill="{cor}"/></g>')


def cadeado(x, y, s=1.0, cor=GR2):
    return (f'<path d="M{x+6*s} {y} v{-10*s} a{10*s} {10*s} 0 0 1 {20*s} 0 v{10*s}" fill="none" stroke="{GREY}" stroke-width="{4*s}"/>'
            f'<rect x="{x}" y="{y}" width="{32*s}" height="{26*s}" rx="{4*s}" fill="{cor}"/>'
            f'<circle cx="{x+16*s}" cy="{y+11*s}" r="{3.5*s}" fill="{BG}"/>'
            f'<rect x="{x+14.5*s}" y="{y+12*s}" width="{3*s}" height="{8*s}" fill="{BG}"/>')


def envelope(x, y, w=110, h=70, lacre=True):
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{PAPER}"/>',
         f'<polygon points="{x},{y} {x+w/2},{y+h*0.55} {x+w},{y}" fill="{SKIN}" stroke="{GREY}" stroke-width="1"/>']
    if lacre:
        cx, cy = x + w / 2, y + h * 0.55
        s.append(f'<circle cx="{cx}" cy="{cy}" r="17" fill="{OR}"/>')
        s.append(f'<circle cx="{cx}" cy="{cy}" r="11" fill="none" stroke="{OR2}" stroke-width="2.5"/>')
        s.append(f'<rect x="{cx-2}" y="{cy-7}" width="4" height="14" fill="{OR2}"/>')
        s.append(f'<rect x="{cx-7}" y="{cy-2}" width="14" height="4" fill="{OR2}"/>')
    return "".join(s)


def abertura_02():
    """Mesa de lacres: envelope com selo, chave, cadeado e carimbo sob a luminária."""
    c = [painel(glow_x=200, glow_y=70)]
    c.append(cruz(24, 20))
    # luminária e cone de luz
    c.append(f'<rect x="196" y="0" width="8" height="28" fill="{GREY}"/>')
    c.append(f'<polygon points="176,28 224,28 214,14 186,14" fill="{DGREY}"/>')
    c.append(f'<polygon points="180,30 220,30 330,{FLOOR-28} 70,{FLOOR-28}" fill="{AMB}" opacity=".08"/>')
    # mesa
    c.append(f'<rect x="40" y="{FLOOR-28}" width="320" height="10" rx="3" fill="{GREY}"/>')
    c.append(f'<rect x="56" y="{FLOOR-18}" width="10" height="18" fill="{DGREY}"/>')
    c.append(f'<rect x="334" y="{FLOOR-18}" width="10" height="18" fill="{DGREY}"/>')
    # objetos sobre a mesa
    c.append(envelope(150, FLOOR - 28 - 66, 100, 62))
    c.append(chave(84, FLOOR - 40, 1.0, AMB, rot=-12))
    c.append(cadeado(282, FLOOR - 28 - 28, 0.95))
    # carimbo de lacre ao lado
    c.append(f'<rect x="262" y="{FLOOR-28-50}" width="7" height="30" rx="3" fill="{GREY}" transform="rotate(18 265 {FLOOR-60})"/>')
    c.append(f'<circle cx="270" cy="{FLOOR-36}" r="7" fill="{OR}"/>')
    # pó de hash: pontos laranja caindo de um funil
    for i, (dx, dy) in enumerate(((0, 0), (6, 9), (-5, 16), (3, 24), (-2, 33))):
        c.append(f'<circle cx="{118+dx}" cy="{40+dy}" r="{2.2-i*0.25}" fill="{OR2}" opacity="{0.9-i*0.12}"/>')
    c.append(f'<polygon points="104,22 132,22 121,36 115,36" fill="{DGREY}"/>')
    return svg("".join(c), rotulo="Mesa iluminada com envelope lacrado, chave, cadeado e carimbo")


def abertura_01():
    """Recepção entrega o crachá; ao fundo, três portas."""
    c = [painel(glow_x=150, glow_y=70)]
    c.append(cruz(24, 20))
    c.append(f'<rect x="56" y="24" width="64" height="5" rx="2" fill="{LINE}"/>')
    c.append(f'<rect x="56" y="34" width="40" height="5" rx="2" fill="{LINE}"/>')
    # portas em perspectiva
    c.append(porta(250, 160, 44, 96, GR2))
    c.append(porta(312, 152, 36, 80, AMB, fechadura="leitor"))
    c.append(porta(362, 146, 28, 66, None))
    # recepção
    c.append(pessoa(78, 150, GR, 1.0, jaleco=True))
    c.append(balcao(30, 130, 42))
    c.append(pessoa(196, 160, GREY, 1.05))
    c.append(cracha(158, 104, 26, 36, rot=-10))
    return svg("".join(c), rotulo="Recepção de hospital entregando um crachá; ao fundo, três portas")


def abertura_03():
    """Tubo pneumático com três estações de inspeção levando um crachá."""
    c = [painel(glow_x=210, glow_y=90)]
    c.append(cruz(24, 20))
    y = 96
    # tubo
    c.append(f'<rect x="-10" y="{y-14}" width="420" height="28" rx="14" fill="{WALL}" stroke="{LINE}" stroke-width="2"/>')
    c.append(f'<rect x="-10" y="{y-9}" width="420" height="4" fill="{PAPER}" opacity=".06"/>')
    # dutos verticais nas pontas
    c.append(f'<rect x="20" y="{y+14}" width="16" height="{FLOOR-y-14}" fill="{WALL}" stroke="{LINE}" stroke-width="2"/>')
    c.append(f'<rect x="364" y="0" width="16" height="{y-14}" fill="{WALL}" stroke="{LINE}" stroke-width="2"/>')
    # estações (borda, rota, domínio)
    for x, cor in ((110, BLUE), (220, OR2), (320, GR2)):
        c.append(f'<rect x="{x-16}" y="{y-24}" width="32" height="48" rx="7" fill="{DOOR}" stroke="{LINE}" stroke-width="2"/>')
        c.append(f'<rect x="{x-16}" y="{y-3}" width="32" height="6" fill="{cor}" opacity=".5"/>')
        c.append(luz(x, y - 34, cor, 3.2))
        c.append(f'<rect x="{x-2}" y="{y+24}" width="4" height="{FLOOR-y-24}" fill="{LINE}"/>')
    # cápsula entre as estações 1 e 2
    cx = 165
    c.append(f'<rect x="{cx-26}" y="{y-11}" width="52" height="22" rx="11" fill="{PAPER}" opacity=".16" stroke="{PAPER}" stroke-opacity=".5" stroke-width="1.2"/>')
    c.append(cracha(cx, y, 16, 20, rot=90, brilho=False))
    for i, dx in enumerate((36, 48, 60)):
        c.append(f'<rect x="{cx-dx-10}" y="{y-4+i*4-4}" width="{14-i*3}" height="2" rx="1" fill="{AMB}" opacity="{.7-i*.2}"/>')
    # piso: pessoa observando
    c.append(pessoa(70, 192, GR, 0.7, jaleco=True))
    return svg("".join(c), rotulo="Tubo pneumático de hospital levando um crachá por três estações de inspeção")


def capa():
    """Crachá grande inclinado diante de uma porta com fechadura."""
    c = []
    # porta ao fundo
    c.append(f'<rect x="196" y="10" width="150" height="230" rx="4" fill="none" stroke="{LINE}" stroke-width="3"/>')
    c.append(f'<rect x="206" y="20" width="130" height="80" rx="3" fill="{WALL}"/>')
    c.append(f'<circle cx="320" cy="150" r="9" fill="none" stroke="{AMB}" stroke-width="3"/>')
    c.append(f'<rect x="317" y="156" width="6" height="14" rx="2" fill="{AMB}"/>')
    c.append(luz(271, 0, GR2, 4))
    # cordão
    c.append(f'<path d="M150 -10 L196 92 M240 -10 L204 92" stroke="{OR}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    c.append(cracha(200, 150, 92, 128, rot=-8))
    return svg("".join(c), w=400, h=250, rotulo="Um crachá diante de uma porta com fechadura")


def ampulheta(x, y, s=1.0):
    return (f'<rect x="{x-16*s}" y="{y-36*s}" width="{32*s}" height="{5*s}" rx="2" fill="{GREY}"/>'
            f'<rect x="{x-16*s}" y="{y+31*s}" width="{32*s}" height="{5*s}" rx="2" fill="{GREY}"/>'
            f'<polygon points="{x-12*s},{y-31*s} {x+12*s},{y-31*s} {x+2*s},{y} {x+12*s},{y+31*s} {x-12*s},{y+31*s} {x-2*s},{y}" fill="{PAPER}" opacity=".18" stroke="{GREY}" stroke-width="1.5"/>'
            f'<polygon points="{x-6*s},{y-16*s} {x+6*s},{y-16*s} {x},{y-4*s}" fill="{AMB}"/>'
            f'<polygon points="{x-11*s},{y+30*s} {x+11*s},{y+30*s} {x},{y+18*s}" fill="{AMB}"/>'
            f'<rect x="{x-0.8*s}" y="{y}" width="{1.6*s}" height="{18*s}" fill="{AMB}" opacity=".8"/>')


def abertura_04():
    """Moedor transforma uma chave de papel em pó, ao lado de uma ampulheta."""
    c = [painel(glow_x=170, glow_y=80)]
    c.append(cruz(24, 20))
    # bancada
    c.append(f'<rect x="60" y="{FLOOR-24}" width="280" height="10" rx="3" fill="{GREY}"/>')
    c.append(f'<rect x="76" y="{FLOOR-14}" width="10" height="14" fill="{DGREY}"/>')
    c.append(f'<rect x="314" y="{FLOOR-14}" width="10" height="14" fill="{DGREY}"/>')
    # moedor: funil, corpo, manivela
    c.append(f'<polygon points="118,30 186,30 166,62 138,62" fill="{DGREY}" stroke="{LINE}" stroke-width="2"/>')
    c.append(f'<rect x="126" y="62" width="52" height="40" rx="6" fill="{DOOR}" stroke="{LINE}" stroke-width="2"/>')
    c.append(f'<rect x="178" y="74" width="26" height="6" rx="3" fill="{GREY}"/>')
    c.append(f'<rect x="200" y="58" width="6" height="30" rx="3" fill="{GREY}"/>')
    c.append(f'<circle cx="203" cy="58" r="6" fill="{AMB}"/>')
    # chave de papel entrando no funil
    c.append(f'<g transform="rotate(-35 152 26)"><rect x="132" y="20" width="44" height="12" rx="2" fill="{PAPER}"/>'
             f'<circle cx="132" cy="26" r="10" fill="{PAPER}"/><circle cx="132" cy="26" r="4" fill="{BG}"/>'
             f'<rect x="164" y="30" width="5" height="7" fill="{PAPER}"/></g>')
    # pó caindo num pote lacrado
    for i, (dx, dy) in enumerate(((0, 0), (5, 8), (-4, 14), (3, 20))):
        c.append(f'<circle cx="{152+dx}" cy="{106+dy}" r="{2.2-i*0.3}" fill="{OR2}" opacity="{0.9-i*0.15}"/>')
    c.append(f'<rect x="132" y="{FLOOR-60}" width="40" height="36" rx="6" fill="{PAPER}" opacity=".2" stroke="{PAPER}" stroke-opacity=".5" stroke-width="1.5"/>')
    c.append(f'<rect x="132" y="{FLOOR-46}" width="40" height="22" rx="4" fill="{OR}" opacity=".85"/>')
    c.append(f'<rect x="128" y="{FLOOR-66}" width="48" height="8" rx="3" fill="{GREY}"/>')
    # ampulheta
    c.append(ampulheta(270, FLOOR - 64, 1.1))
    return svg("".join(c), rotulo="Moedor transformando uma chave de papel em pó, ao lado de uma ampulheta")


def pulseira(cx, cy, cor=OR, rot=0):
    return (f'<g transform="rotate({rot} {cx} {cy})">'
            f'<rect x="{cx-30}" y="{cy-6}" width="60" height="12" rx="6" fill="{cor}"/>'
            f'<rect x="{cx-8}" y="{cy-9}" width="16" height="18" rx="3" fill="{PAPER}"/>'
            f'<rect x="{cx-4}" y="{cy-4}" width="8" height="2" fill="{GREY}"/>'
            f'<rect x="{cx-4}" y="{cy+1}" width="5" height="2" fill="{GREY}"/></g>')


def abertura_05():
    """Guichê entrega uma pulseira numerada; atrás, escaninhos acesos."""
    c = [painel(glow_x=230, glow_y=60)]
    c.append(cruz(24, 20))
    # parede do guichê com janela
    c.append(f'<rect x="150" y="18" width="230" height="{FLOOR-18}" fill="{WALL}"/>')
    c.append(f'<rect x="170" y="38" width="190" height="92" rx="6" fill="{BG}" stroke="{LINE}" stroke-width="3"/>')
    # escaninhos ao fundo: grade com alguns acesos
    acesos = {(0, 1), (1, 3), (2, 0), (2, 4), (1, 1)}
    for lin in range(3):
        for col in range(6):
            x, y = 182 + col * 29, 48 + lin * 24
            on = (lin, col) in acesos
            c.append(f'<rect x="{x}" y="{y}" width="24" height="18" rx="2" fill="{AMB if on else DOOR}" opacity="{0.85 if on else 1}"/>')
    # balcão do guichê
    c.append(f'<rect x="160" y="130" width="210" height="8" rx="2" fill="{GREY}"/>')
    # pulseira passando pela janela
    c.append(f'<circle cx="160" cy="132" r="30" fill="{OR2}" opacity=".14"/>')
    c.append(pulseira(160, 132, OR, rot=-12))
    # visitante
    c.append(pessoa(96, 192, GREY, 0.95))
    return svg("".join(c), rotulo="Guichê entregando uma pulseira numerada; ao fundo, escaninhos acesos")


def lupa(x, y, r=26, rot=35):
    return (f'<g transform="rotate({rot} {x} {y})">'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{BLUE}" opacity=".12"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{GREY}" stroke-width="5"/>'
            f'<path d="M{x-r*0.55} {y-r*0.25} a{r*0.6} {r*0.6} 0 0 1 {r*0.45} {-r*0.4}" fill="none" stroke="{PAPER}" stroke-width="2.5" opacity=".6"/>'
            f'<rect x="{x-4}" y="{y+r+2}" width="8" height="{r*1.3}" rx="3" fill="{GREY}"/></g>')


def selo(cx, cy, r=13):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r+3}" fill="{OR}" opacity=".35"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{OR}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*0.62}" fill="none" stroke="{OR2}" stroke-width="2"/>'
            f'<rect x="{cx-1.5}" y="{cy-r*0.45}" width="3" height="{r*0.9}" fill="{OR2}"/>'
            f'<rect x="{cx-r*0.45}" y="{cy-1.5}" width="{r*0.9}" height="3" fill="{OR2}"/>')


def abertura_06():
    """Crachá lacrado numa vitrine: a lupa lê tudo, o selo impede a falsificação,
    a ampulheta conta o prazo que ninguém interrompe."""
    c = [painel(glow_x=190, glow_y=80)]
    c.append(cruz(24, 20))
    # vitrine (caixa de vidro) sobre pedestal
    c.append(f'<rect x="120" y="{FLOOR-22}" width="140" height="22" rx="3" fill="{DGREY}"/>')
    c.append(f'<rect x="112" y="{FLOOR-28}" width="156" height="8" rx="2" fill="{GREY}"/>')
    c.append(f'<rect x="126" y="34" width="128" height="{FLOOR-62}" rx="6" fill="{PAPER}" opacity=".05" stroke="{PAPER}" stroke-opacity=".35" stroke-width="1.5"/>')
    c.append(f'<rect x="132" y="40" width="5" height="{FLOOR-74}" fill="{PAPER}" opacity=".08"/>')
    # crachá com três faixas (cabeçalho, conteúdo, assinatura)
    c.append(f'<circle cx="190" cy="86" r="52" fill="{OR2}" opacity=".10"/>')
    c.append(cracha(190, 86, 58, 80, rot=0, brilho=False, faixa=BLUE))
    c.append(f'<rect x="161" y="{86+40-14}" width="58" height="4" fill="{AMB}" opacity=".7"/>')
    c.append(selo(212, 118, 11))
    # lupa lendo o crachá por fora do vidro
    c.append(lupa(92, 70, 24, rot=-35))
    c.append(f'<line x1="112" y1="74" x2="168" y2="80" stroke="{AMB}" stroke-width="1" stroke-dasharray="3 3" opacity=".6"/>')
    # ampulheta
    c.append(ampulheta(318, FLOOR - 52, 0.95))
    return svg("".join(c), rotulo="Crachá lacrado numa vitrine, lido por uma lupa, ao lado de uma ampulheta")


def abertura_07():
    """Quadro de chaves: pares de chave pequena e grande; um gancho revogado."""
    c = [painel(glow_x=210, glow_y=70)]
    c.append(cruz(24, 20))
    # quadro
    c.append(f'<rect x="86" y="22" width="230" height="122" rx="8" fill="{WALL}" stroke="{LINE}" stroke-width="3"/>')
    estados = ["ok", "ok", "revogada", "ok"]
    for i, est in enumerate(estados):
        x = 112 + i * 54
        c.append(f'<rect x="{x-12}" y="34" width="24" height="7" rx="2" fill="{DOOR}"/>')
        cor = RED if est == "revogada" else GR2
        c.append(luz(x, 52, cor, 2.6))
        c.append(f'<circle cx="{x}" cy="66" r="3" fill="{GREY}"/>')
        if est == "revogada":
            # gancho vazio com uma chave partida caída
            c.append(f'<line x1="{x}" y1="66" x2="{x}" y2="74" stroke="{GREY}" stroke-width="2"/>')
            c.append(f'<g opacity=".55">{chave(x-14, 126, 0.55, GREY, rot=8)}</g>')
            continue
        # chave pequena (access) e grande (refresh) no mesmo gancho
        c.append(f'<line x1="{x}" y1="66" x2="{x}" y2="74" stroke="{GREY}" stroke-width="2"/>')
        c.append(chave(x, 82, 0.55, AMB, rot=90))
        c.append(chave(x + 9, 80, 0.8, PAPER if i != 1 else OR2, rot=90))
    # ampulheta pequena ao lado do quadro
    c.append(ampulheta(352, FLOOR - 40, 0.7))
    c.append(pessoa(52, 192, GR, 0.8, jaleco=True))
    return svg("".join(c), rotulo="Quadro de chaves com pares de chaves pequena e grande e um gancho revogado")


def celular(x, y, s=1.0, digitos=True):
    o = [f'<rect x="{x}" y="{y}" width="{22*s}" height="{38*s}" rx="{4*s}" fill="{DGREY}" stroke="{GREY}" stroke-width="1.5"/>',
         f'<rect x="{x+3*s}" y="{y+5*s}" width="{16*s}" height="{26*s}" rx="{2*s}" fill="{BG}"/>']
    if digitos:
        for i in range(3):
            o.append(f'<circle cx="{x+6.5*s+i*4.5*s}" cy="{y+14*s}" r="{1.5*s}" fill="{GR2}"/>')
            o.append(f'<circle cx="{x+6.5*s+i*4.5*s}" cy="{y+20*s}" r="{1.5*s}" fill="{GR2}"/>')
        o.append(f'<rect x="{x+5*s}" y="{y+25*s}" width="{12*s}" height="{2*s}" rx="1" fill="{AMB}"/>')
    return "".join(o)


def abertura_08():
    """Porta com leitor de crachá e teclado; o celular dá o segundo fator;
    pela janela, outro prédio emite crachás por um feixe de luz."""
    c = [painel(glow_x=250, glow_y=60)]
    c.append(cruz(24, 20))
    # janela com o outro prédio (provedor de identidade)
    c.append(f'<rect x="62" y="52" width="96" height="74" rx="4" fill="{BG}" stroke="{LINE}" stroke-width="3"/>')
    c.append(f'<rect x="80" y="70" width="30" height="56" fill="{DOOR}"/>')
    c.append(f'<rect x="114" y="82" width="26" height="44" fill="{DOOR}"/>')
    for (wx, wy) in ((85, 76), (97, 76), (85, 90), (119, 88), (129, 100)):
        c.append(f'<rect x="{wx}" y="{wy}" width="6" height="6" fill="{BLUE}" opacity=".8"/>')
    c.append(f'<polygon points="110,74 250,96 250,104 110,84" fill="{BLUE}" opacity=".10"/>')
    # porta com duas fechaduras
    c.append(porta(240, FLOOR, 56, 112, GR2))
    c.append(f'<rect x="304" y="78" width="12" height="18" rx="2" fill="{DGREY}"/>')
    c.append(f'<rect x="306" y="82" width="8" height="3" fill="{GR2}"/>')
    c.append(f'<rect x="302" y="102" width="16" height="20" rx="2" fill="{DGREY}"/>')
    for i in range(3):
        for j in range(3):
            c.append(f'<rect x="{304.5+j*4.3}" y="{105+i*5}" width="3" height="3" fill="{GREY}"/>')
    # pessoa com crachá e celular
    c.append(pessoa(190, 192, GR, 0.9, jaleco=True))
    c.append(cracha(196, 152, 12, 16, rot=-6, brilho=False))
    c.append(f'<circle cx="166" cy="140" r="20" fill="{GR2}" opacity=".10"/>')
    c.append(celular(156, 122, 0.9))
    return svg("".join(c), rotulo="Porta com leitor de crachá e teclado; celular com código; outro prédio ao fundo")


def abertura_09():
    """Catraca com contador e ampulheta; guarita com livro de registro;
    uma fila de sombras do lado de fora."""
    c = [painel(glow_x=230, glow_y=70)]
    c.append(cruz(24, 20))
    # fila de sombras
    for i, x in enumerate((40, 70, 100, 130)):
        c.append(f'<g opacity="{0.35 + i*0.1}">{pessoa(x, 192, DGREY, 0.75)}</g>')
    # catraca
    c.append(f'<rect x="176" y="{FLOOR-62}" width="40" height="62" rx="5" fill="{DGREY}" stroke="{LINE}" stroke-width="2"/>')
    c.append(f'<rect x="184" y="{FLOOR-54}" width="24" height="14" rx="2" fill="{BG}"/>')
    c.append(f'<rect x="188" y="{FLOOR-50}" width="5" height="6" fill="{RED}"/><rect x="196" y="{FLOOR-50}" width="5" height="6" fill="{RED}" opacity=".4"/>')
    for ang in (200, 320, 80):
        c.append(f'<rect x="216" y="{FLOOR-34}" width="34" height="5" rx="2.5" fill="{GREY}" transform="rotate({ang} 214 {FLOOR-32})"/>')
    c.append(f'<circle cx="214" cy="{FLOOR-32}" r="6" fill="{AMB}"/>')
    c.append(luz(196, FLOOR - 76, RED, 3))
    # guarita com livro de registro
    c.append(f'<rect x="282" y="58" width="96" height="{FLOOR-58}" rx="4" fill="{WALL}" stroke="{LINE}" stroke-width="2"/>')
    c.append(f'<rect x="292" y="70" width="76" height="40" rx="3" fill="{BG}"/>')
    c.append(f'<rect x="300" y="118" width="58" height="34" rx="2" fill="{PAPER}"/>')
    c.append(f'<rect x="328" y="118" width="2" height="34" fill="{GREY}"/>')
    for i in range(5):
        c.append(f'<rect x="304" y="{124+i*5.5}" width="20" height="2" rx="1" fill="{GREY}"/>')
        c.append(f'<rect x="334" y="{124+i*5.5}" width="{18 - (i%2)*6}" height="2" rx="1" fill="{GREY}"/>')
    c.append(ampulheta(256, FLOOR - 40, 0.6))
    return svg("".join(c), rotulo="Catraca com contador vermelho, ampulheta e guarita com livro de registro; fila de sombras do lado de fora")


def abertura_10():
    """Corredor com quatro portas, quatro fechaduras: lista, crachá
    colorido, relógio e fio que liga a pessoa ao paciente."""
    c = [painel(glow_x=210, glow_y=60)]
    c.append(cruz(24, 20))
    xs = (60, 140, 220, 300)
    for x in xs:
        c.append(porta(x, FLOOR, 48, 96, None))
    # 1 ACL: prancheta com lista
    c.append(f'<rect x="{xs[0]+14}" y="80" width="20" height="26" rx="2" fill="{PAPER}"/>')
    for i in range(4):
        c.append(f'<rect x="{xs[0]+17}" y="{85+i*5}" width="14" height="2" fill="{GREY}"/>')
    # 2 RBAC: leitor com três cores de crachá
    for i, cor in enumerate((OR, GR2, BLUE)):
        c.append(f'<rect x="{xs[1]+10+i*10}" y="86" width="8" height="12" rx="1.5" fill="{cor}"/>')
    # 3 ABAC: relógio
    cx = xs[2] + 24
    c.append(f'<circle cx="{cx}" cy="92" r="12" fill="{PAPER}"/><circle cx="{cx}" cy="92" r="12" fill="none" stroke="{AMB}" stroke-width="2"/>')
    c.append(f'<line x1="{cx}" y1="92" x2="{cx}" y2="84" stroke="{BG}" stroke-width="2"/><line x1="{cx}" y1="92" x2="{cx+6}" y2="95" stroke="{BG}" stroke-width="2"/>')
    # 4 ReBAC: dois nós ligados
    c.append(f'<line x1="{xs[3]+12}" y1="96" x2="{xs[3]+36}" y2="84" stroke="{GR2}" stroke-width="2.5"/>')
    c.append(f'<circle cx="{xs[3]+12}" cy="96" r="6" fill="{GR2}"/><circle cx="{xs[3]+36}" cy="84" r="6" fill="{AMB}"/>')
    # luzes acima das portas, em degrau
    for i, x in enumerate(xs):
        c.append(luz(x + 24, 52, (GREY, AMB, OR2, GR2)[i], 3))
    c.append(f'<rect x="40" y="{FLOOR+12}" width="330" height="3" rx="1.5" fill="{OR}" opacity=".35"/>')
    return svg("".join(c), rotulo="Corredor com quatro portas e quatro tipos de fechadura: lista, crachá, relógio e relação")


def abertura_11():
    """Quadro na parede: a matriz papel × permissão, com marcas; um
    carimbo sobre a mesa."""
    c = [painel(glow_x=200, glow_y=60)]
    c.append(cruz(24, 20))
    x0, y0, cw, ch = 110, 30, 34, 16
    c.append(f'<rect x="{x0-46}" y="{y0-10}" width="{46+cw*3+20}" height="{ch*7+30}" rx="6" fill="{WALL}" stroke="{LINE}" stroke-width="3"/>')
    marcas = [(1, 1, 1), (1, 1, 1), (1, 1, 1), (1, 1, 0), (1, 1, 0), (0, 1, 0), (1, 0, 0)]
    for i, linha in enumerate(marcas):
        y = y0 + 10 + i * ch
        c.append(f'<rect x="{x0-38}" y="{y+3}" width="30" height="4" rx="2" fill="{GREY}"/>')
        for j, v in enumerate(linha):
            cx, cy = x0 + j * cw + cw / 2, y + 5
            if v:
                c.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="{GR2}"/>')
            else:
                c.append(f'<line x1="{cx-4}" y1="{cy-4}" x2="{cx+4}" y2="{cy+4}" stroke="{RED}" stroke-width="2.4"/><line x1="{cx+4}" y1="{cy-4}" x2="{cx-4}" y2="{cy+4}" stroke="{RED}" stroke-width="2.4"/>')
    for j, cor in enumerate((OR, GR, BLUE)):
        c.append(f'<rect x="{x0 + j*cw + 9}" y="{y0-2}" width="16" height="6" rx="2" fill="{cor}"/>')
    # mesa com carimbo
    c.append(f'<rect x="270" y="{FLOOR-30}" width="110" height="8" rx="3" fill="{GREY}"/>')
    c.append(f'<rect x="318" y="{FLOOR-62}" width="10" height="26" rx="3" fill="{DGREY}"/>')
    c.append(f'<rect x="308" y="{FLOOR-38}" width="30" height="8" rx="2" fill="{OR}"/>')
    c.append(pessoa(240, 192, GR, 0.85, jaleco=True))
    return svg("".join(c), rotulo="Quadro na parede com a matriz de papéis e permissões; carimbo sobre a mesa")


def abertura_12():
    """Arquivo de prontuários: gavetas numeradas; uma mão alcança a
    gaveta vizinha, e a luz dela acende em vermelho."""
    c = [painel(glow_x=220, glow_y=60)]
    c.append(cruz(24, 20))
    x0, y0, gw, gh = 120, 26, 52, 24
    for lin in range(4):
        for col in range(4):
            x, y = x0 + col * (gw + 6), y0 + lin * (gh + 6)
            alvo = (lin, col) == (1, 2)
            dona = (lin, col) == (1, 1)
            c.append(f'<rect x="{x}" y="{y}" width="{gw}" height="{gh}" rx="3" fill="{DOOR}" stroke="{LINE}" stroke-width="1.5"/>')
            c.append(f'<rect x="{x+gw/2-9}" y="{y+gh/2-3}" width="18" height="6" rx="2" fill="{PAPER if not alvo else RED}" opacity="{0.9 if alvo or dona else 0.35}"/>')
            if alvo:
                c.append(luz(x + gw - 8, y + 7, RED, 2.4))
            if dona:
                c.append(luz(x + gw - 8, y + 7, GR2, 2.4))
    # gaveta puxada (a do vizinho)
    gx, gy = x0 + 2 * (gw + 6), y0 + (gh + 6)
    c.append(f'<rect x="{gx-6}" y="{gy+4}" width="{gw+12}" height="{gh+6}" rx="3" fill="{WALL}" stroke="{RED}" stroke-width="2" opacity=".9"/>')
    c.append(f'<rect x="{gx+4}" y="{gy}" width="14" height="18" rx="1" fill="{PAPER}"/><rect x="{gx+20}" y="{gy-2}" width="14" height="18" rx="1" fill="{PAPER}" opacity=".8"/>')
    # pessoa à esquerda, braço estendido
    c.append(pessoa(70, 192, GREY, 0.9))
    c.append(f'<line x1="82" y1="140" x2="{gx-6}" y2="{gy+18}" stroke="{SKIN}" stroke-width="5" stroke-linecap="round" opacity=".85"/>')
    return svg("".join(c), rotulo="Arquivo de prontuários com gavetas numeradas; alguém abre a gaveta vizinha e a luz fica vermelha")


def abertura_13():
    """Cofre na parede com duas chaves penduradas; uma esteira traz
    caixas lacradas, e uma caixa sem lacre é separada."""
    c = [painel(glow_x=200, glow_y=60)]
    c.append(cruz(24, 20))
    # cofre
    c.append(f'<rect x="60" y="36" width="96" height="92" rx="8" fill="{DGREY}" stroke="{GREY}" stroke-width="3"/>')
    c.append(f'<circle cx="108" cy="82" r="20" fill="{WALL}" stroke="{AMB}" stroke-width="3"/>')
    for ang in range(0, 360, 60):
        c.append(f'<rect x="107" y="64" width="2" height="8" fill="{AMB}" transform="rotate({ang} 108 82)"/>')
    c.append(chave(170, 52, 0.6, AMB, rot=90))
    c.append(chave(186, 52, 0.6, GREY, rot=90))
    # esteira
    c.append(f'<rect x="200" y="{FLOOR-22}" width="190" height="8" rx="4" fill="{GREY}"/>')
    for x in range(208, 386, 22):
        c.append(f'<circle cx="{x}" cy="{FLOOR-18}" r="3" fill="{DGREY}"/>')
    for i, x in enumerate((214, 262, 310)):
        c.append(f'<rect x="{x}" y="{FLOOR-56}" width="36" height="34" rx="3" fill="{AMB}" opacity=".85"/>')
        c.append(f'<circle cx="{x+18}" cy="{FLOOR-39}" r="6" fill="{OR}"/><circle cx="{x+18}" cy="{FLOOR-39}" r="3" fill="{OR2}"/>')
    # caixa sem lacre, separada
    c.append(f'<rect x="352" y="{FLOOR-40}" width="30" height="28" rx="3" fill="{AMB}" opacity=".45" transform="rotate(12 367 {FLOOR-26})"/>')
    c.append(luz(367, FLOOR - 58, RED, 2.6))
    return svg("".join(c), rotulo="Cofre com duas chaves; esteira com caixas lacradas e uma caixa sem lacre separada")


def manequim(x, base, s=1.0):
    """Boneco de teste de impacto: corpo amarelo com alvos pretos e brancos."""
    out = [pessoa(x, base, AMB, s)]
    top = base - 22 * s - 40 * s
    for cx, cy, r in ((x, top - 9 * s, 4.2 * s), (x, top + 18 * s, 5 * s)):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BG}"/>')
        out.append(f'<path d="M{cx} {cy-r} A{r} {r} 0 0 1 {cx+r} {cy} L{cx} {cy} Z" fill="{PAPER}"/>')
        out.append(f'<path d="M{cx} {cy+r} A{r} {r} 0 0 1 {cx-r} {cy} L{cx} {cy} Z" fill="{PAPER}"/>')
    return "".join(out)


def abertura_14():
    """Um manequim de teste experimenta as portas, uma a uma; na
    parede, a prancheta de resultados marca cada tentativa."""
    c = [painel(glow_x=230, glow_y=60)]
    c.append(cruz(24, 20))
    xs = (130, 200, 270)
    for x, cor in zip(xs, (GR2, RED, AMB)):
        c.append(porta(x, FLOOR, 46, 96, cor, fechadura="leitor"))
    # manequim à direita, com a mão na maçaneta da última porta
    c.append(manequim(352, 192, 0.95))
    c.append(f'<line x1="342" y1="140" x2="{xs[2]+40}" y2="{FLOOR-42}" stroke="{AMB}" stroke-width="5" stroke-linecap="round"/>')
    # rastro das portas já tentadas, no chão
    for i, x in enumerate(xs[:2]):
        c.append(f'<rect x="{x+12}" y="{FLOOR+16}" width="22" height="3" rx="1.5" fill="{OR}" opacity="{0.25 + i*0.15}"/>')
    # prancheta de resultados na parede
    c.append(f'<rect x="40" y="62" width="40" height="54" rx="3" fill="{PAPER}"/>')
    c.append(f'<rect x="51" y="57" width="18" height="8" rx="2" fill="{GREY}"/>')
    for i, cor in enumerate((GR2, GR2, GR2, RED, GR2)):
        y = 72 + i * 8
        c.append(f'<rect x="45" y="{y}" width="20" height="2.6" rx="1" fill="{GREY}"/>')
        c.append(f'<circle cx="72" cy="{y+1.3}" r="2.6" fill="{cor}"/>')
    return svg("".join(c), rotulo="Manequim de teste de impacto tenta abrir uma porta; prancheta na parede marca o resultado de cada tentativa")


def robo(x, base, s=1.0, faixa=GR2):
    """Robô de entrega: caixa sobre rodas, antena e um crachá de uma cor."""
    w, h = 54 * s, 62 * s
    y = base - h - 10 * s
    out = [f'<rect x="{x-w/2}" y="{y}" width="{w}" height="{h}" rx="{10*s}" fill="{GREY}"/>',
           f'<rect x="{x-w/2+7*s}" y="{y+8*s}" width="{w-14*s}" height="{18*s}" rx="{5*s}" fill="{BG}"/>',
           f'<rect x="{x-12*s}" y="{y+15*s}" width="{24*s}" height="{3*s}" rx="1.5" fill="{BLUE}"/>',
           f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y-14*s}" stroke="{GREY}" stroke-width="{3*s}"/>',
           luz(x, y - 16 * s, BLUE, 2.6 * s)]
    for dx in (-w / 2 + 10 * s, w / 2 - 10 * s):
        out.append(f'<circle cx="{x+dx}" cy="{base-6*s}" r="{7*s}" fill="{DGREY}"/>')
    out.append(cracha(x, y + 44 * s, 18 * s, 24 * s, rot=0, brilho=False, faixa=faixa))
    return "".join(out)


def abertura_15():
    """Robô de entrega com crachá de uma cor só diante de um armário de
    escaninhos: só o escaninho daquela cor acende. Num escaninho
    trancado, um bilhete colado."""
    c = [painel(glow_x=250, glow_y=60)]
    c.append(cruz(24, 20))
    x0, y0, gw, gh = 170, 22, 46, 30
    cores = [[GREY, GR2, GREY, GREY], [GREY, GREY, GREY, RED], [GREY, GR2, GREY, GREY], [GREY, GREY, GREY, GREY]]
    c.append(f'<rect x="{x0-8}" y="{y0-8}" width="{4*(gw+6)+10}" height="{4*(gh+6)+10}" rx="6" fill="{WALL}" stroke="{LINE}" stroke-width="2"/>')
    for lin in range(4):
        for col in range(4):
            x, y = x0 + col * (gw + 6), y0 + lin * (gh + 6)
            cor = cores[lin][col]
            aceso = cor == GR2
            c.append(f'<rect x="{x}" y="{y}" width="{gw}" height="{gh}" rx="3" fill="{DOOR}" stroke="{GR2 if aceso else LINE}" stroke-width="{2 if aceso else 1.2}"/>')
            c.append(f'<rect x="{x+gw-11}" y="{y+gh/2-4}" width="5" height="8" rx="1" fill="{DGREY}"/>')
            c.append(luz(x + 8, y + 8, cor if cor != GREY else None, 2.2))
            if aceso:
                c.append(f'<rect x="{x+3}" y="{y+3}" width="{gw-6}" height="{gh-6}" rx="2" fill="{GR2}" opacity=".12"/>')
    # bilhete colado no escaninho trancado
    bx, by = x0 + 3 * (gw + 6) + 6, y0 + (gh + 6) + 4
    c.append(f'<rect x="{bx}" y="{by}" width="26" height="22" rx="1" fill="{PAPER}" transform="rotate(-8 {bx+13} {by+11})"/>')
    for i in range(3):
        c.append(f'<rect x="{bx+4}" y="{by+5+i*5}" width="{18 - i*4}" height="2" rx="1" fill="{GREY}" transform="rotate(-8 {bx+13} {by+11})"/>')
    c.append(f'<rect x="{bx+9}" y="{by-3}" width="10" height="5" fill="{AMB}" opacity=".7" transform="rotate(-8 {bx+13} {by+11})"/>')
    # robô e o feixe do crachá até o escaninho certo
    c.append(robo(100, 192, 1.0, faixa=GR2))
    c.append(f'<line x1="110" y1="{192-36}" x2="{x0+gw+6+4}" y2="{y0+2*(gh+6)+gh/2}" stroke="{GR2}" stroke-width="1.5" stroke-dasharray="4 4" opacity=".7"/>')
    return svg("".join(c), rotulo="Robô de entrega com crachá verde diante de um armário de escaninhos; só os verdes acendem; um bilhete colado num escaninho trancado")


def abertura_16():
    """Escada de quatro degraus junto à parede; uma fita métrica desce
    do alto e uma marca laranja indica o terceiro degrau."""
    c = [painel(glow_x=240, glow_y=50)]
    c.append(cruz(24, 20))
    x0, w, h = 120, 52, 30
    for i in range(4):
        x = x0 + i * w
        topo = FLOOR - (i + 1) * h
        cor = (DGREY, DGREY, OR, DGREY)[i]
        c.append(f'<rect x="{x}" y="{topo}" width="{(4 - i) * w}" height="{h}" fill="{cor if i == 2 else DOOR}" stroke="{LINE}" stroke-width="2"/>')
        c.append(f'<rect x="{x}" y="{topo}" width="{(4 - i) * w}" height="4" fill="{OR2 if i == 2 else GREY}" opacity="{1 if i == 2 else .5}"/>')
    # fita métrica vertical à direita
    fx = x0 + 4 * w + 18
    c.append(f'<rect x="{fx}" y="22" width="14" height="{FLOOR-22}" fill="{AMB}"/>')
    for k in range(0, int((FLOOR - 22) / 6)):
        y = FLOOR - k * 6
        c.append(f'<rect x="{fx}" y="{y}" width="{7 if k % 5 else 11}" height="1.4" fill="{BG}"/>')
    c.append(f'<rect x="{fx-6}" y="12" width="26" height="16" rx="4" fill="{GREY}"/>')
    # marca do terceiro degrau
    y3 = FLOOR - 3 * h
    c.append(f'<line x1="{x0 + 2*w}" y1="{y3}" x2="{fx + 20}" y2="{y3}" stroke="{OR2}" stroke-width="2" stroke-dasharray="5 4"/>')
    c.append(luz(fx + 26, y3, OR2, 3))
    # pessoa no segundo degrau, subindo
    c.append(pessoa(x0 + w + 26, FLOOR - 2 * h, GR, 0.8, jaleco=True))
    return svg("".join(c), rotulo="Escada de quatro degraus; uma fita métrica marca o terceiro degrau, e alguém sobe pelo segundo")
