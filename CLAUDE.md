# CLAUDE.md

Ebook "Estado & Tela" (pt-BR), quarto livro da série do Prof. Rogério
Silva. Fonte em HTML, saída em site (index.html) e PDF 108 × 192 mm.

## Build

- `cd fonte && python3 build.py` monta `index.html` a partir de
  `head.html` + `p1.html`…`pN.html`.
- `python3 fonte/pdf.py <abs index.html> <abs pdf>` renderiza no Chromium
  headless (não troque por WeasyPrint: as figuras usam CSS do documento).
- `python3 fonte/medir.py <pdf> --json` mede páginas por capítulo contra o
  orçamento aprovado (244 p, teto 250) e grava `saidas/paginas.json`,
  que o sumário usa no build seguinte.

## Regras que o build faz cumprir

- Código impresso vem do git: `{{BLOCO:tag:caminho|linhas=a-b}}` lê
  `../web` (ou `api@tag:` para `../api`). Linha > 46 caracteres = erro.
- `{{DIFF:tagA:tagB:caminho}}` imprime a diferença real entre tags.
- `{{SAIDA:arquivo|linhas=..|destaque=a;b}}` imprime `saidas/arquivo`.
- `{{FIG:nome}}` lê `fonte/fig_nome.svg`; `{{ARTE:função}}` chama
  `fonte/arte.py`. Toda tabela dentro de `<div class="tbl-wrap">`.

## Regras de conteúdo

- Dado (fonte externa), Modelo ilustrativo (conta nossa, premissas
  explícitas) e Medido (saída real em `saidas/`) nunca se misturam.
- Saída de terminal nunca é escrita à mão. Corte só com `…`.
- Figuras: SVG inline com classes de cor (`f-*`, `s-*`), sem hexadecimal,
  para funcionar nos dois temas. Aberturas: `arte.py`, painel grafite.
- Cada capítulo: problema, modelo mental + "Onde a analogia para", por
  dentro, prática, erro clássico e prova de revert, armadilha de IA,
  prompt de agente, exercícios em três níveis, fechamento com fontes.
- Prompts no texto: agente (Goal/Context/Constraints/Done when). Variante
  C-P-T-R-F-A, revisão e V.E.R.M. ficam em `web/prompts/capNN.md`.
