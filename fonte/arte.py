"""Cenas do Estado & Tela.

Mesmo mundo e mesmo traço do Crachá & Porta (arte_base.py): um hospital
à noite, formas geométricas planas sobre painel grafite, pessoas sem
rosto, nenhuma letra. A metáfora-mestra é o monitor de beira-leito.
"""
from arte_base import (AMB, BG, BLUE, DGREY, DOOR, FLOOR, GR, GR2, GREY,
                       LINE, OR, OR2, PAPER, SKIN, WALL, cruz, luz, painel,
                       pessoa, svg)


def monitor(x, y, w=142, h=94, acesa=1, haste=True):
    """Monitor multiparamétrico. `acesa`: índice da faixa redesenhada."""
    s = []
    if haste:
        cx = x + w / 2
        s.append(f'<rect x="{cx-3}" y="{y+h}" width="6" height="{FLOOR-y-h}" fill="{LINE}"/>')
        s.append(f'<rect x="{cx-21}" y="{FLOOR-4}" width="42" height="5" rx="2" fill="{DGREY}"/>')
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{DOOR}" stroke="{DGREY}" stroke-width="2"/>')
    ix, iy, iw, ih = x + 8, y + 8, w - 16, h - 16
    s.append(f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="4" fill="#0E1013"/>')
    faixas = 3
    fh = ih / faixas
    cores = (GR2, OR2, BLUE)
    for i in range(faixas):
        fy = iy + i * fh
        meio = fy + fh / 2
        cor = cores[i]
        if i == acesa:
            s.append(f'<rect x="{ix}" y="{fy+2}" width="{iw}" height="{fh-4}" fill="{OR2}" opacity=".16"/>')
            s.append(f'<rect x="{ix}" y="{fy+2}" width="3" height="{fh-4}" fill="{OR2}"/>')
        pts = []
        passo = (iw - 8) / 12
        for k in range(13):
            px = ix + 4 + k * passo
            if i == 0:
                py = meio - (7 if k % 4 == 1 else -6 if k % 4 == 2 else 0)
            elif i == 1:
                py = meio + (4 if k % 2 else -4) - (k % 3)
            else:
                py = meio + (3 if k % 2 else -3)
            pts.append(f"{px:.1f},{py:.1f}")
        op = "1" if i != 2 else ".7"
        s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{cor}" stroke-width="{2 if i < 2 else 1.6}" opacity="{op}"/>')
    return "".join(s)


def leito(x, w=96):
    return (f'<rect x="{x}" y="134" width="{w}" height="16" rx="4" fill="{DGREY}"/>'
            f'<rect x="{x+4}" y="126" width="30" height="10" rx="4" fill="{SKIN}" opacity=".85"/>'
            f'<rect x="{x+34}" y="128" width="{w-38}" height="8" rx="3" fill="{GR}" opacity=".75"/>'
            f'<rect x="{x+4}" y="150" width="5" height="10" fill="{LINE}"/>'
            f'<rect x="{x+w-9}" y="150" width="5" height="10" fill="{LINE}"/>')


def prancheta(x, y, rot=-8, cor=OR):
    cx, cy = x + 9, y + 12
    return (f'<g transform="rotate({rot} {cx} {cy})">'
            f'<rect x="{x}" y="{y}" width="18" height="24" rx="3" fill="{PAPER}"/>'
            f'<rect x="{x+3}" y="{y+6}" width="12" height="2.4" rx="1" fill="{GREY}"/>'
            f'<rect x="{x+3}" y="{y+11}" width="8" height="2.4" rx="1" fill="{cor}"/>'
            f'<rect x="{x+3}" y="{y+16}" width="10" height="2.4" rx="1" fill="{GREY}"/></g>')


def quadro(x, y, w=40, h=30, linhas=3, cor=PAPER):
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{cor}" opacity=".9"/>']
    for i in range(linhas):
        lw = w - 10 - (i % 2) * 8
        s.append(f'<rect x="{x+5}" y="{y+6+i*7}" width="{lw}" height="2.4" rx="1" fill="{GREY}"/>')
    return "".join(s)


def capa():
    """Uma tela feita de blocos; só um está aceso."""
    c = [f'<rect x="60" y="14" width="280" height="190" rx="14" fill="{DOOR}" stroke="{DGREY}" stroke-width="3"/>',
         f'<rect x="74" y="28" width="252" height="162" rx="6" fill="#0E1013"/>']
    cols, rows, gap = 9, 6, 4
    bw = (252 - 16 - gap * (cols - 1)) / cols
    bh = (162 - 16 - gap * (rows - 1)) / rows
    for r in range(rows):
        for k in range(cols):
            bx = 82 + k * (bw + gap)
            by = 36 + r * (bh + gap)
            if (r, k) == (2, 5):
                c.append(f'<rect x="{bx-6}" y="{by-6}" width="{bw+12}" height="{bh+12}" rx="6" fill="{OR2}" opacity=".22"/>')
                c.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="3" fill="{OR2}"/>')
            else:
                tom = (GR2, BLUE, GREY)[(r + k) % 3]
                op = ".22" if (r * 7 + k * 3) % 5 else ".38"
                c.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="3" fill="{tom}" opacity="{op}"/>')
    c.append(f'<rect x="194" y="204" width="12" height="28" fill="{LINE}"/>')
    c.append(f'<rect x="160" y="230" width="80" height="8" rx="3" fill="{DGREY}"/>')
    return svg("".join(c), w=400, h=244,
               rotulo="Tela de monitor feita de blocos pequenos; um único bloco aceso em laranja")


def abertura_01():
    """Duas enfermarias: quadros à mão de um lado, um monitor do outro."""
    c = [painel(glow_x=300, glow_y=60)]
    c.append(cruz(24, 20))
    # parede divisória
    c.append(f'<rect x="196" y="0" width="8" height="{FLOOR}" fill="{LINE}"/>')
    # esquerda: quadros-brancos e alguém correndo entre eles
    for i, (qx, qy) in enumerate(((22, 58), (70, 44), (118, 62), (150, 100), (18, 100))):
        c.append(quadro(qx, qy, 38, 28, 3, PAPER if i != 3 else AMB))
    c.append(f'<g transform="rotate(-8 112 132)">{pessoa(112, 160, GR, 0.8, jaleco=True)}</g>')
    for i in range(3):
        c.append(f'<rect x="{80-i*12}" y="{118+i*6}" width="{16-i*4}" height="2" rx="1" fill="{AMB}" opacity="{.7-i*.2}"/>')
    # direita: um monitor e alguém parado, anotando
    c.append(monitor(234, 30, 120, 80, acesa=1))
    c.append(pessoa(368, 160, GR, 0.8, jaleco=True))
    c.append(prancheta(340, 108))
    return svg("".join(c), rotulo="Duas enfermarias: numa, alguém corre entre cinco quadros; na outra, um único monitor")


def abertura_02():
    """Carrinho de equipamentos sendo ligado; uma luz verde acende."""
    c = [painel(glow_x=250, glow_y=80)]
    c.append(cruz(24, 20))
    # tomada na parede
    c.append(f'<rect x="330" y="96" width="34" height="44" rx="5" fill="{DOOR}" stroke="{LINE}" stroke-width="2"/>')
    c.append(f'<circle cx="341" cy="118" r="3" fill="{BG}"/><circle cx="353" cy="118" r="3" fill="{BG}"/>')
    # carrinho
    c.append(f'<rect x="150" y="86" width="130" height="10" rx="3" fill="{GREY}"/>')
    c.append(f'<rect x="156" y="96" width="118" height="44" rx="4" fill="{DGREY}"/>')
    c.append(f'<rect x="164" y="104" width="46" height="12" rx="2" fill="{DOOR}"/>')
    c.append(f'<rect x="164" y="120" width="46" height="12" rx="2" fill="{DOOR}"/>')
    c.append(f'<rect x="150" y="140" width="130" height="6" rx="2" fill="{GREY}"/>')
    for wx in (160, 270):
        c.append(f'<circle cx="{wx}" cy="153" r="7" fill="{LINE}"/><circle cx="{wx}" cy="153" r="2.5" fill="{GREY}"/>')
    # equipamento sobre o carrinho: monitor pequeno apagado + caixa
    c.append(monitor(176, 26, 86, 58, acesa=-1, haste=False))
    c.append(f'<rect x="222" y="104" width="44" height="28" rx="3" fill="{DOOR}"/>')
    c.append(luz(254, 118, GR2, 3))
    # cabo até a tomada
    c.append(f'<path d="M266 128 C 300 160, 320 160, 341 132" fill="none" stroke="{GREY}" stroke-width="2.5"/>')
    c.append(f'<rect x="336" y="126" width="18" height="10" rx="2" fill="{PAPER}"/>')
    # pessoa conectando
    c.append(pessoa(96, 160, GR, 0.95, jaleco=True))
    return svg("".join(c), rotulo="Carrinho de equipamentos ligado à tomada; uma luz verde acende")


def abertura_03():
    """O monitor de beira-leito: só a faixa que mudou está acesa."""
    c = [painel(glow_x=250, glow_y=70)]
    c.append(cruz(24, 20))
    c.append(monitor(178, 28, 142, 94, acesa=1))
    c.append(leito(296))
    c.append(f'<path d="M312 128 C 300 120, 300 116, 316 112" fill="none" stroke="{GREY}" stroke-width="1.2"/>')
    c.append(pessoa(104, 150, GR, 1.0, jaleco=True))
    c.append(f'<rect x="114" y="96" width="30" height="6" rx="3" fill="{GR}" transform="rotate(-18 114 99)"/>')
    c.append(prancheta(140, 80))
    return svg("".join(c), rotulo="Monitor de beira-leito atualizando só uma faixa da tela, ao lado de um leito e de uma enfermeira")
