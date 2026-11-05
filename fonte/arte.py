"""Cenas do Estado & Tela.

Mesmo mundo e mesmo traço do Crachá & Porta (arte_base.py): um hospital
à noite, formas geométricas planas sobre painel grafite, pessoas sem
rosto, nenhuma letra. A metáfora-mestra é o monitor de beira-leito.
"""
from arte_base import (RED, AMB, BG, BLUE, DGREY, DOOR, FLOOR, GR, GR2, GREY,
                       LINE, OR, OR2, PAPER, SKIN, WALL, cadeado, cracha, cruz,
                       luz, painel, pessoa, porta, svg)


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


def bandeja(x, y, w, h, cor, itens=2):
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{DGREY}"/>',
         f'<rect x="{x+3}" y="{y+3}" width="{w-6}" height="{h-6}" rx="2" fill="{DOOR}"/>']
    passo = (w - 6) / itens
    for i in range(itens):
        cx = x + 3 + passo * i + passo / 2
        s.append(f'<rect x="{cx-passo*0.32}" y="{y+h/2-4}" width="{passo*0.64}" height="8" rx="3" fill="{cor}" opacity=".85"/>')
    return "".join(s)


def abertura_04():
    """Bandejas modulares, as mesmas peças em combinações diferentes."""
    c = [painel(glow_x=230, glow_y=70)]
    c.append(cruz(24, 20))
    # carrinho com três prateleiras de bandejas encaixadas
    c.append(f'<rect x="150" y="40" width="6" height="112" fill="{GREY}"/>')
    c.append(f'<rect x="300" y="40" width="6" height="112" fill="{GREY}"/>')
    for i, (y, combo) in enumerate(((46, (GR2, OR2)), (82, (BLUE, GR2, AMB)), (118, (OR2,)))):
        c.append(f'<rect x="150" y="{y+28}" width="156" height="4" rx="1" fill="{GREY}"/>')
        larg = 150 / len(combo)
        for k, cor in enumerate(combo):
            c.append(bandeja(153 + k * larg, y, larg - 4, 28, cor, 1 if len(combo) == 3 else 2))
    for wx in (160, 296):
        c.append(f'<circle cx="{wx}" cy="153" r="7" fill="{LINE}"/><circle cx="{wx}" cy="153" r="2.5" fill="{GREY}"/>')
    # bandejas soltas sobre a bancada, esperando para encaixar
    c.append(f'<rect x="326" y="118" width="64" height="6" rx="2" fill="{GREY}"/>')
    c.append(f'<rect x="334" y="124" width="6" height="36" fill="{DGREY}"/><rect x="376" y="124" width="6" height="36" fill="{DGREY}"/>')
    c.append(bandeja(330, 94, 56, 22, BLUE, 2))
    c.append(pessoa(96, 160, GR, 0.95, jaleco=True))
    c.append(bandeja(108, 100, 40, 20, AMB, 1))
    return svg("".join(c), rotulo="Carrinho com bandejas modulares encaixadas em combinações diferentes")


def abertura_05():
    """A prescrição desce; a campainha do leito sobe."""
    c = [painel(glow_x=120, glow_y=50)]
    c.append(cruz(24, 20))
    # mezanino com o médico
    c.append(f'<rect x="0" y="86" width="190" height="6" fill="{LINE}"/>')
    c.append(pessoa(88, 86, GREY, 0.8))
    c.append(prancheta(104, 40, rot=-6))
    # escada/rampa da prescrição descendo
    c.append(f'<path d="M190 92 L300 150" stroke="{LINE}" stroke-width="3"/>')
    for i, (px, py) in enumerate(((206, 92), (238, 110), (270, 128))):
        c.append(f'<g opacity="{.35 + i*.3}">{prancheta(px, py, rot=28, cor=GR2)}</g>')
    # enfermeira e leito embaixo
    c.append(pessoa(318, 160, GR, 0.9, jaleco=True))
    c.append(leito(220, 70))
    # fio da campainha subindo até a luz do posto
    c.append(f'<path d="M226 128 C 210 100, 175 120, 150 70 L150 40" fill="none" stroke="{AMB}" stroke-width="2" stroke-dasharray="4 3"/>')
    c.append(luz(150, 34, AMB, 4))
    return svg("".join(c), rotulo="A prescrição desce do médico para a enfermagem; o fio da campainha do leito sobe até a luz do posto")


def carimbo(cx, cy, cor=GR2, r=16):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{cor}" stroke-width="3"/>'
            f'<path d="M{cx-7} {cy} l5 5 l9 -10" fill="none" stroke="{cor}" stroke-width="3" stroke-linecap="round"/>')


def abertura_06():
    """Prancheta de admissão com campos e um carimbo verde; um carimbo
    repetido, riscado, ao lado."""
    c = [painel(glow_x=210, glow_y=60)]
    c.append(cruz(24, 20))
    # balcão de admissão
    c.append(f'<rect x="60" y="120" width="290" height="40" rx="3" fill="{DGREY}"/>')
    c.append(f'<rect x="54" y="114" width="302" height="8" rx="2" fill="{GREY}"/>')
    # ficha grande
    c.append(f'<g transform="rotate(-4 200 70)">'
             f'<rect x="146" y="22" width="108" height="92" rx="5" fill="{PAPER}"/>'
             f'<rect x="184" y="16" width="32" height="10" rx="3" fill="{GREY}"/>')
    for i, w in enumerate((70, 52, 64)):
        y = 42 + i * 18
        c.append(f'<rect x="158" y="{y}" width="{w}" height="3" rx="1" fill="{GREY}"/>'
                 f'<rect x="158" y="{y+6}" width="84" height="7" rx="2" fill="none" stroke="{GREY}" stroke-width="1"/>')
    c.append(carimbo(232, 96, GR, 11))
    c.append('</g>')
    # ficha duplicada, riscada
    c.append(f'<g transform="rotate(8 300 80)" opacity=".75">'
             f'<rect x="270" y="46" width="66" height="62" rx="4" fill="{SKIN}"/>'
             f'<rect x="280" y="60" width="44" height="3" rx="1" fill="{GREY}"/>'
             f'<rect x="280" y="72" width="34" height="3" rx="1" fill="{GREY}"/>'
             f'<path d="M274 52 L332 104 M332 52 L274 104" stroke="{RED}" stroke-width="3" stroke-linecap="round"/>'
             f'</g>')
    c.append(pessoa(96, 160, GR, 0.95, jaleco=True))
    return svg("".join(c), rotulo="Ficha de admissão carimbada sobre o balcão; ao lado, uma ficha duplicada riscada")


def tubo(x, y):
    return (f'<rect x="{x}" y="{y}" width="10" height="30" rx="5" fill="{PAPER}" opacity=".9"/>'
            f'<rect x="{x}" y="{y}" width="10" height="9" rx="3" fill="{OR2}"/>')


def abertura_07():
    """Tubos de exame indo ao laboratório; um resultado antigo barrado."""
    c = [painel(glow_x=300, glow_y=60)]
    c.append(cruz(24, 20))
    # porta do laboratório à direita
    c.append(f'<rect x="300" y="44" width="80" height="116" rx="3" fill="{LINE}"/>')
    c.append(f'<rect x="306" y="50" width="68" height="110" fill="{DOOR}"/>')
    c.append(f'<rect x="314" y="58" width="52" height="34" rx="2" fill="{WALL}"/>')
    c.append(luz(340, 34, GR2, 3.5))
    # esteira de tubos saindo do laboratório
    c.append(f'<rect x="120" y="128" width="180" height="6" rx="2" fill="{GREY}"/>')
    for i, x in enumerate((150, 196)):
        c.append(f'<g opacity="{.55 + i * .4}">{tubo(x, 96)}</g>')
    # resultado antigo, barrado por uma faixa de luz
    c.append(f'<rect x="232" y="84" width="4" height="48" fill="{RED}" opacity=".85"/>')
    c.append(f'<rect x="226" y="80" width="16" height="4" rx="2" fill="{RED}"/>')
    c.append(f'<g opacity=".6">{tubo(252, 96)}</g>')
    c.append(f'<rect x="248" y="88" width="18" height="18" rx="9" fill="none" stroke="{RED}" stroke-width="2"/>')
    # enfermeira recebendo o tubo novo
    c.append(pessoa(88, 160, GR, 0.95, jaleco=True))
    c.append(f'<rect x="100" y="104" width="34" height="6" rx="3" fill="{GR}" transform="rotate(-10 100 107)"/>')
    return svg("".join(c), rotulo="Tubos de exame saindo do laboratório; um resultado antigo é barrado por uma faixa de luz")


def abertura_08():
    """Planta da ala vista de cima: setores com porta para o corredor
    comum; uma porta corta-fogo fechada contém o setor em alarme."""
    c = [painel(glow_x=330, glow_y=70, piso=False)]
    c.append(cruz(16, 14, 12))
    # corredor comum
    c.append(f'<rect x="24" y="124" width="352" height="30" rx="3" fill="{WALL}"/>')
    for x in range(40, 370, 28):
        c.append(f'<rect x="{x}" y="138" width="14" height="2" rx="1" fill="{LINE}"/>')
    setores = [(30, 104, GR2), (142, 104, GR2), (262, 108, RED)]
    for x, w, cor in setores:
        c.append(f'<rect x="{x}" y="34" width="{w}" height="84" rx="4" fill="{DOOR}" stroke="{LINE}" stroke-width="3"/>')
        # porta para o corredor
        c.append(f'<rect x="{x+w/2-11}" y="114" width="22" height="8" fill="{WALL}"/>')
        c.append(luz(x + w - 12, 44, cor, 3.5))
        # leitos e quadros vistos de cima
        for k in range(2):
            lx = x + 12 + k * (w / 2 - 4)
            c.append(f'<rect x="{lx}" y="56" width="{w/2-22}" height="18" rx="3" fill="{DGREY}"/>')
            c.append(f'<rect x="{lx+3}" y="59" width="10" height="12" rx="3" fill="{SKIN}" opacity=".8"/>')
        c.append(quadro(x + 12, 86, w - 24, 20, 2, DGREY))
    # alarme no terceiro setor, contido
    c.append(f'<circle cx="316" cy="76" r="44" fill="{RED}" opacity=".14"/>')
    c.append(f'<circle cx="316" cy="76" r="22" fill="{RED}" opacity=".12"/>')
    # porta corta-fogo fechada entre o segundo e o terceiro setor
    c.append(f'<rect x="250" y="30" width="8" height="94" rx="2" fill="{AMB}"/>')
    for y in range(34, 120, 12):
        c.append(f'<rect x="250" y="{y}" width="8" height="5" fill="{RED}"/>')
    # quem passa pelo corredor segue
    c.append(f'<circle cx="104" cy="139" r="6" fill="{SKIN}"/>')
    c.append(f'<rect x="112" y="135" width="16" height="8" rx="4" fill="{GR}"/>')
    return svg("".join(c), rotulo="Planta de uma ala vista de cima; uma porta corta-fogo fechada contém o setor em alarme")


def cadeira(x, base, cor=BLUE):
    """Pessoa em cadeira de rodas, de perfil."""
    return (f'<circle cx="{x}" cy="{base-12}" r="12" fill="none" stroke="{GREY}" stroke-width="3"/>'
            f'<circle cx="{x+20}" cy="{base-4}" r="4" fill="{GREY}"/>'
            f'<rect x="{x-6}" y="{base-26}" width="30" height="5" rx="2" fill="{GREY}"/>'
            f'<rect x="{x-8}" y="{base-50}" width="5" height="28" rx="2" fill="{GREY}"/>'
            f'<rect x="{x-4}" y="{base-54}" width="18" height="30" rx="7" fill="{cor}"/>'
            f'<rect x="{x+8}" y="{base-28}" width="16" height="6" rx="3" fill="{DGREY}"/>'
            f'<rect x="{x+20}" y="{base-28}" width="6" height="20" rx="2" fill="{DGREY}"/>'
            f'<circle cx="{x+5}" cy="{base-63}" r="8" fill="{SKIN}"/>')


def abertura_09():
    """Corredor com faixas coloridas no piso levando às portas, e
    uma rampa ao lado da escada: o caminho serve a todos."""
    c = [painel(glow_x=210, glow_y=60)]
    c.append(cruz(18, 16, 12))
    # portas ao fundo, cada uma com a luz da sua faixa
    for x, cor in ((150, GR2), (196, BLUE), (242, OR2)):
        c.append(f'<rect x="{x}" y="70" width="34" height="90" rx="2" fill="{DOOR}" stroke="{LINE}" stroke-width="2"/>')
        c.append(f'<rect x="{x}" y="64" width="34" height="5" rx="2" fill="{cor}"/>')
    # faixas no piso, do primeiro plano até cada porta
    for x0, x1, cor in ((60, 167, GR2), (120, 213, BLUE), (180, 259, OR2)):
        c.append(f'<polygon points="{x0},200 {x0+14},200 {x1+3},160 {x1-3},160" fill="{cor}" opacity=".85"/>')
    # escada e rampa à direita
    for k in range(4):
        c.append(f'<rect x="{300+k*10}" y="{160-(k+1)*10}" width="{70-k*10}" height="10" fill="{DGREY}"/>')
    c.append(f'<polygon points="296,200 400,200 400,128" fill="{LINE}"/>')
    c.append(f'<line x1="300" y1="186" x2="400" y2="116" stroke="{AMB}" stroke-width="3"/>')
    c.append(f'<g transform="rotate(-34 350 166)">{cadeira(342, 184)}</g>')
    c.append(pessoa(70, 176, GR, 0.9, jaleco=True))
    return svg("".join(c), rotulo="Corredor com faixas coloridas no piso levando a portas, e uma rampa ao lado da escada")


def abertura_10():
    """Maleta de instrumentos aberta: cada peça no seu encaixe de
    espuma; uma peça fora, ao lado do encaixe vazio com a forma dela."""
    c = [painel(glow_x=120, glow_y=50)]
    c.append(cruz(362, 16, 12))
    # tampa
    c.append(f'<polygon points="70,30 330,30 342,62 58,62" fill="{DOOR}" stroke="{LINE}" stroke-width="2"/>')
    c.append(f'<rect x="186" y="36" width="28" height="6" rx="3" fill="{AMB}"/>')
    # base com espuma
    c.append(f'<rect x="56" y="64" width="288" height="96" rx="6" fill="{DGREY}" stroke="{LINE}" stroke-width="2"/>')
    c.append(f'<rect x="64" y="72" width="272" height="80" rx="4" fill="{WALL}"/>')
    # encaixes e peças (termômetro, tesoura, seringa, estetoscópio)
    c.append(f'<rect x="76" y="82" width="14" height="60" rx="7" fill="{BG}"/>')
    c.append(f'<rect x="79" y="86" width="8" height="46" rx="4" fill="{PAPER}"/>')
    c.append(f'<circle cx="83" cy="134" r="5" fill="{RED}"/>')
    for cx in (110, 124):
        c.append(f'<circle cx="{cx}" cy="128" r="8" fill="{BG}"/>')
        c.append(f'<circle cx="{cx}" cy="128" r="5" fill="none" stroke="{BLUE}" stroke-width="2.5"/>')
    c.append(f'<line x1="112" y1="120" x2="126" y2="84" stroke="{GREY}" stroke-width="3"/>')
    c.append(f'<line x1="122" y1="120" x2="108" y2="84" stroke="{GREY}" stroke-width="3"/>')
    c.append(f'<rect x="150" y="96" width="70" height="16" rx="4" fill="{BG}"/>')
    c.append(f'<rect x="156" y="99" width="44" height="10" rx="2" fill="{PAPER}" opacity=".9"/>')
    c.append(f'<rect x="200" y="102" width="16" height="4" fill="{GREY}"/>')
    c.append(f'<rect x="150" y="104" width="8" height="2" fill="{GREY}"/>')
    # encaixe vazio do estetoscópio: a forma espera a peça
    c.append(f'<path d="M244 86 q0 34 22 34 q22 0 22 -34" fill="none" stroke="{BG}" stroke-width="9" stroke-linecap="round"/>')
    c.append(f'<circle cx="300" cy="128" r="12" fill="{BG}"/>')
    c.append(f'<line x1="266" y1="120" x2="290" y2="126" stroke="{BG}" stroke-width="7" stroke-linecap="round"/>')
    # a peça, fora, com a mesma forma
    c.append(f'<g transform="translate(-140 50) scale(.6)">'
             f'<path d="M244 86 q0 34 22 34 q22 0 22 -34" fill="none" stroke="{GR2}" stroke-width="4" stroke-linecap="round"/>'
             f'<line x1="266" y1="120" x2="290" y2="126" stroke="{GR2}" stroke-width="3"/>'
             f'<circle cx="300" cy="128" r="9" fill="{GR2}"/></g>')
    return svg("".join(c), rotulo="Maleta de instrumentos aberta, cada peça no seu encaixe; um estetoscópio fora, ao lado do encaixe vazio com a sua forma")


def ondas(x, y, cor, n=3, abre=1):
    """Arcos de som saindo de um alto-falante, para a direita (abre=1)."""
    out = []
    for k in range(n):
        r = 8 + k * 7
        out.append(f'<path d="M{x} {y-r} A{r} {r} 0 0 {1 if abre > 0 else 0} {x} {y+r}" '
                   f'fill="none" stroke="{cor}" stroke-width="2" opacity="{0.9 - k*0.25:.2f}"/>')
    return "".join(out)


def abertura_11():
    """Corredor com alto-falantes no teto, um canal por cor; em cada sala,
    só quem escuta aquele canal acende."""
    c = [painel(glow_x=200, glow_y=40)]
    c.append(cruz(18, 16, 12))
    # teto com três alto-falantes, cada um num canal
    canais = [(90, GR2), (200, BLUE), (310, OR2)]
    for x, cor in canais:
        c.append(f'<rect x="{x-9}" y="26" width="18" height="12" rx="3" fill="{DGREY}"/>')
        c.append(f'<circle cx="{x}" cy="32" r="4" fill="{cor}"/>')
        c.append(f'<g transform="rotate(90 {x} 40)">{ondas(x, 40, cor)}</g>')
    # salas embaixo, com uma pessoa e um receptor de canal cada
    salas = [(40, GR2, True), (110, BLUE, False), (180, BLUE, True),
             (250, GR2, False), (320, OR2, True)]
    for x, cor, ouvindo in salas:
        c.append(f'<rect x="{x}" y="96" width="56" height="64" rx="3" fill="{DOOR}" stroke="{LINE}" stroke-width="2"/>')
        c.append(pessoa(x + 28, FLOOR, GR if ouvindo else DGREY, 0.62, jaleco=ouvindo))
        c.append(f'<rect x="{x+40}" y="104" width="10" height="7" rx="2" fill="{cor if ouvindo else DGREY}"/>')
        if ouvindo:
            c.append(luz(x + 45, 100, cor, 3))
    return svg("".join(c), rotulo="Corredor com alto-falantes de três cores no teto; em cada sala só acende quem escuta o canal da sua cor")


def abertura_12():
    """Porta do centro cirúrgico com a luz de cirurgia acesa e, ao lado, o
    quadro das três fases da lista de verificação: duas marcadas, uma por vir."""
    c = [painel(glow_x=110, glow_y=60)]
    c.append(cruz(362, 16, 12))
    # porta dupla do centro cirúrgico
    c.append(f'<rect x="40" y="52" width="130" height="108" rx="3" fill="{DOOR}" stroke="{LINE}" stroke-width="3"/>')
    c.append(f'<line x1="105" y1="52" x2="105" y2="160" stroke="{LINE}" stroke-width="3"/>')
    for x in (62, 120):
        c.append(f'<rect x="{x}" y="72" width="26" height="20" rx="3" fill="{BG}" opacity=".7"/>')
    c.append(f'<rect x="80" y="34" width="50" height="12" rx="4" fill="{RED}"/>')
    c.append(f'<circle cx="105" cy="40" r="16" fill="{RED}" opacity=".18"/>')
    # quadro com as três fases
    c.append(f'<rect x="210" y="40" width="160" height="110" rx="6" fill="{WALL}" stroke="{LINE}" stroke-width="2"/>')
    for k, (feita, cor) in enumerate(((True, GR2), (True, GR2), (False, AMB))):
        y = 58 + k * 30
        c.append(f'<rect x="224" y="{y}" width="18" height="18" rx="4" fill="{BG}" stroke="{cor}" stroke-width="2"/>')
        if feita:
            c.append(f'<path d="M228 {y+9} l4 4 l7 -9" fill="none" stroke="{cor}" stroke-width="2.5"/>')
        for j, w in enumerate((90, 60)):
            c.append(f'<rect x="252" y="{y+3+j*8}" width="{w}" height="4" rx="2" fill="{DGREY if feita else LINE}"/>')
        if k < 2:
            c.append(f'<line x1="233" y1="{y+19}" x2="233" y2="{y+29}" stroke="{GR2}" stroke-width="2"/>')
    # seta de volta, cortada: com a luz acesa não se volta
    c.append(f'<path d="M360 138 q14 -40 0 -80" fill="none" stroke="{DGREY}" stroke-width="2" stroke-dasharray="3 4"/>')
    c.append(f'<line x1="352" y1="92" x2="368" y2="104" stroke="{RED}" stroke-width="3"/>')
    c.append(pessoa(190, FLOOR, GR, 0.8, jaleco=True))
    return svg("".join(c), rotulo="Porta do centro cirúrgico com a luz acesa e um quadro de três fases, duas marcadas; uma seta de volta aparece cortada")


def abertura_13():
    """Corredor com placas de endereço sobre as portas e, na parede, o mapa
    'você está aqui' com um alfinete: o endereço leva qualquer um ao leito."""
    c = [painel(glow_x=300, glow_y=50)]
    c.append(cruz(18, 16, 12))
    # mapa da ala na parede
    c.append(f'<rect x="28" y="40" width="120" height="86" rx="6" fill="{WALL}" stroke="{LINE}" stroke-width="2"/>')
    for k in range(3):
        for j in range(2):
            c.append(f'<rect x="{38+k*36}" y="{50+j*36}" width="30" height="28" rx="3" fill="{DGREY}"/>')
    c.append(f'<rect x="38" y="80" width="102" height="4" rx="2" fill="{LINE}"/>')
    c.append(f'<circle cx="118" cy="98" r="7" fill="{OR}"/>')
    c.append(f'<circle cx="118" cy="98" r="3" fill="{PAPER}"/>')
    c.append(f'<path d="M118 105 L118 114" stroke="{OR}" stroke-width="2.5"/>')
    # portas com placas numeradas por barras (sem texto)
    for k, x in enumerate((176, 246, 316)):
        c.append(f'<rect x="{x}" y="70" width="52" height="90" rx="2" fill="{DOOR}" stroke="{LINE}" stroke-width="2"/>')
        c.append(f'<rect x="{x+6}" y="52" width="40" height="13" rx="3" fill="{BLUE if k != 2 else OR2}"/>')
        for n in range(k + 1):
            c.append(f'<rect x="{x+12+n*7}" y="55" width="4" height="7" rx="1" fill="{BG}"/>')
    c.append(luz(342, 90, OR2, 4))
    c.append(pessoa(286, FLOOR, GR, 0.85, jaleco=True))
    c.append(f'<path d="M298 128 q20 -10 30 -36" fill="none" stroke="{OR2}" stroke-width="2" stroke-dasharray="3 4"/>')
    return svg("".join(c), rotulo="Corredor com placas de endereço sobre as portas e um mapa com alfinete; uma pessoa segue a placa até a terceira porta")


def abertura_14():
    """Arquivo central com pastas à esquerda; à direita, a prancheta na beira
    do leito com um relógio: a cópia vale por um tempo."""
    c = [painel(glow_x=120, glow_y=50)]
    c.append(cruz(362, 16, 12))
    # estante do arquivo central
    c.append(f'<rect x="30" y="40" width="130" height="120" rx="4" fill="{DOOR}" stroke="{LINE}" stroke-width="2"/>')
    for j in range(3):
        y = 50 + j * 36
        c.append(f'<rect x="36" y="{y+28}" width="118" height="4" fill="{LINE}"/>')
        for k in range(8):
            cor = (AMB, BLUE, GR2, PAPER)[(k + j) % 4]
            c.append(f'<rect x="{40+k*14}" y="{y+2}" width="10" height="26" rx="1" fill="{cor}" opacity=".75"/>')
    # seta de ida e de volta entre arquivo e prancheta
    c.append(f'<path d="M168 86 L232 86" stroke="{GREY}" stroke-width="2"/>'
             f'<path d="M226 81 L233 86 L226 91" fill="none" stroke="{GREY}" stroke-width="2"/>')
    c.append(f'<path d="M232 108 L168 108" stroke="{OR2}" stroke-width="2" stroke-dasharray="4 4"/>'
             f'<path d="M174 103 L167 108 L174 113" fill="none" stroke="{OR2}" stroke-width="2"/>')
    # prancheta com relógio
    c.append(f'<g transform="translate(262 52) scale(2.6)">{prancheta(0, 0, rot=-6)}</g>')
    c.append(f'<circle cx="338" cy="58" r="16" fill="{WALL}" stroke="{AMB}" stroke-width="2.5"/>')
    c.append(f'<path d="M338 58 L338 47 M338 58 L346 62" stroke="{AMB}" stroke-width="2.5" stroke-linecap="round"/>')
    c.append(leito(244, 120))
    return svg("".join(c), rotulo="Arquivo central com pastas e, ao lado, uma prancheta com relógio; setas de ida e volta entre os dois")


def abertura_15():
    """Porta de ala com leitor de crachá; a recepcionista aproxima o crachá.
    Atrás do vidro, a porta real, trancada com cadeado: esconder não é
    proibir."""
    c = [painel(glow_x=280, glow_y=60)]
    c.append(cruz(24, 18, 12))
    # porta da frente, com leitor e luz vermelha
    c.append(porta(70, FLOOR, 62, 112, cor_luz=RED, fechadura="leitor"))
    c.append(pessoa(170, FLOOR, BLUE, s=1.0))
    c.append(cracha(150, 92, w=16, h=22, rot=-14, brilho=True, faixa=BLUE))
    # parede de vidro e, atrás, a porta real trancada
    c.append(f'<rect x="214" y="30" width="170" height="130" rx="3" fill="{DOOR}" stroke="{LINE}" stroke-width="3"/>')
    c.append(porta(268, 152, 60, 100, cor_luz=GR2))
    c.append(cadeado(282, 104, s=1.0, cor=GR2))
    c.append(f'<rect x="214" y="30" width="170" height="130" rx="3" fill="{BLUE}" opacity=".10"/>')
    for x0 in (230, 250, 330):
        c.append(f'<line x1="{x0}" y1="150" x2="{x0+40}" y2="40" stroke="{PAPER}" stroke-width="2" opacity=".14"/>')
    c.append(f'<rect x="214" y="92" width="170" height="3" fill="{LINE}"/>')
    return svg("".join(c), rotulo="Porta de ala com leitor de crachá e uma pessoa aproximando o crachá; atrás de uma parede de vidro, outra porta trancada com cadeado")


def abertura_16():
    """Sala de simulação: o manequim no leito, o monitor ligado nele, a
    lista de verificação com marcas verdes e o cronômetro correndo."""
    c = [painel(glow_x=210, glow_y=50)]
    c.append(cruz(24, 16, 12))
    c.append(monitor(34, 34, w=112, h=74, acesa=0))
    c.append(leito(150, 130))
    # cabeça do manequim no travesseiro, com o alvo de teste
    cx, cy, r = 166, 121, 8
    c.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{AMB}"/>')
    c.append(f'<path d="M{cx} {cy-r} A{r} {r} 0 0 1 {cx+r} {cy} L{cx} {cy} Z" fill="{BG}"/>')
    c.append(f'<path d="M{cx} {cy+r} A{r} {r} 0 0 1 {cx-r} {cy} L{cx} {cy} Z" fill="{BG}"/>')
    c.append(f'<path d="M146 70 C 158 92, 160 104, 164 114" fill="none" stroke="{GREY}" stroke-width="1.4"/>')
    # lista de verificação com três marcas
    c.append(f'<rect x="300" y="34" width="70" height="92" rx="6" fill="{PAPER}"/>')
    c.append(f'<rect x="324" y="28" width="22" height="10" rx="3" fill="{GREY}"/>')
    for k in range(3):
        y = 52 + k * 24
        c.append(f'<path d="M310 {y} l5 5 l9 -10" fill="none" stroke="{GR}" stroke-width="3" stroke-linecap="round"/>')
        c.append(f'<rect x="330" y="{y-3}" width="{30 - 6*k}" height="4" rx="2" fill="{GREY}"/>')
    # cronômetro
    c.append(f'<rect x="241" y="40" width="10" height="7" rx="2" fill="{GREY}"/>')
    c.append(f'<circle cx="246" cy="70" r="22" fill="{WALL}" stroke="{OR2}" stroke-width="3"/>')
    c.append(f'<path d="M246 70 L246 54 M246 70 L256 76" stroke="{OR2}" stroke-width="3" stroke-linecap="round"/>')
    return svg("".join(c), rotulo="Sala de simulação com manequim no leito, monitor ligado, lista de verificação com marcas verdes e um cronômetro")
