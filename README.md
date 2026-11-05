# Estado & Tela

**Aplicações web reativas com React, do DOM manipulado à mão até uma
aplicação completa, autenticada e testada, construída com agentes de IA
sem perder o controle do código.**

20 capítulos · 244 páginas · 22 figuras · 21 ilustrações

Manual de campo · organizado por Prof. Rogério Silva e Claude Opus 5.5 ·
2026 · TEC.1052 Programação para Internet II · ADS · IFPI

Parte da [biblioteca de ebooks abertos do Prof. Rogério Silva](https://rogeriosilva-ifpi.github.io/).

## Como ler

- **Site**: https://rogeriosilva-ifpi.github.io/estado-e-tela-ebook/
- **PDF**: [Estado-e-Tela.pdf](Estado-e-Tela.pdf) (108 × 192 mm, para celular)
- **EPUB**: [Estado-e-Tela.epub](Estado-e-Tela.epub) (EPUB 3, validado com EPUBCheck)

## Os quatro repositórios

| Repositório | O que tem |
|---|---|
| `estado-e-tela-ebook` | este livro, os roteiros de medição e as saídas |
| `estado-e-tela-web` | o Mini-Prontuário em React, uma tag por capítulo |
| `estado-e-tela-api` | a API (fork da tag `cap16` do Crachá & Porta Express) |
| `estado-e-tela-next` | o laboratório Next.js dos capítulos 17 e 18 |

## Montar o livro

O build lê o código direto dos repositórios, na tag de cada capítulo.
Clone os quatro lado a lado com os nomes `ebook`, `web`, `api` e `next`
(ou aponte `ESTADO_WEB`, `ESTADO_API` e `ESTADO_NEXT` para outro lugar).

```bash
pip install playwright pypdf && playwright install chromium
cd fonte && python3 build.py && cd ..          # index.html
python3 fonte/pdf.py "$PWD/index.html" "$PWD/Estado-e-Tela.pdf"
python3 fonte/medir.py Estado-e-Tela.pdf --json # páginas × orçamento
python3 fonte/build.py                          # de novo: sumário com páginas
pip install beautifulsoup4 html5lib pillow
python3 epub.py                                 # Estado-e-Tela.epub (EPUB 3)
```

O build falha se uma linha de código impressa passar de 46 caracteres,
se uma tabela estiver fora de `.tbl-wrap` ou se um placeholder não tiver
fonte.

## Procedência

- **Dado**: fato externo, com fonte no fim de cada capítulo.
- **Medido**: saída real, guardada em `saidas/`, produzida pelos roteiros
  de `medicoes/`. Nenhuma saída foi escrita à mão; trechos cortados são
  marcados com `…`.
- **Código**: sai do git (`{{BLOCO:tag:caminho}}`), nunca de cópia.

## Medições

| Roteiro | Saída | Pré-requisito |
|---|---|---|
| `medicoes/cap01.py` | `c1-ala.txt` | `bash medicoes/vendor.sh /tmp/v` (React local) |
| `medicoes/cap02_cookie.py` | `c2-cookie-chromium.txt` | API em :3000 e `npm run dev` |
| `medicoes/cap03.py` | `c3-renderometro.txt` | `npm run dev` na tag `cap03` |
| `medicoes/cap04.py` | `c4-renderometro.txt` | nenhum: sobe a tela de cada tag sozinho |
| `medicoes/cap05.py` | `c5-mutacao.txt` | nenhum |
| `medicoes/cap06.py` | `c6-envio-duplo.txt` | nenhum: sobe API e tela de cada tag (porta 5173 livre) |
| `medicoes/cap07.py` | `c7-corrida.txt` | nenhum: idem |
| `medicoes/cap08.py` | `c8-busca.txt` | nenhum: sobe API e tela; um cenário sem API |
| `medicoes/vigia_a11y.py TAG…` | `c9-vigia.txt` | `cd medicoes && npm install` (axe-core) |
| `medicoes/cap09.py` | `c9-comparacao.txt` | idem; faz `npm ci` em cada tag (precisa de rede para o registro npm) |
| `medicoes/cap10.py` | `c10-teclado.txt` | nenhum |
| `medicoes/cap11.py` | `c11-renders.txt` | nenhum; aplica `cap11-contexto-unico.patch` na variante |
| `medicoes/cap12.py` | `c12-voltar.txt` | nenhum: sobe a API `cap12` (porta 5173 livre) |
| `medicoes/cap13.py` | `c13-rotas.txt` | nenhum; aplica `cap13-sem-flushsync.patch` na variante; faz build das tags |
| `medicoes/cap14.py` | `c14-remoto.txt` | nenhum: sobe a API `cap14` |
| `medicoes/cap15.py` | `c15-sessao.txt` | nenhum: sobe as APIs `cap14` e `cap15` (porta 5173 livre) |
| `medicoes/porta_dos_fundos.py TELA API` | `c15-porta-*.txt` | nenhum; sai com código 1 se achar porta dos fundos |
| `medicoes/cap16.py e2e` | `c16-e2e.txt` | `PW_CHROMIUM` se o Chromium instalado não for o do `@playwright/test` |
| `medicoes/cap16.py compilador` | `c16-compilador.txt` | nenhum; aplica `cap16-paineis.patch` nas duas tags |
| `medicoes/cap16.py piramide` | `c16-piramide.txt` | nenhum |
| `medicoes/raio_x.py TAG…` | `c16-bundle.txt` | nenhum: build de cada tag num worktree |
| `medicoes/cap17.py chegada` | `c17-chegada.txt` | portas 3000, 4173 e 5174 livres; `npm install` em `next` |
| `medicoes/cap17.py hidratacao` | `c17-hidratacao.txt` | idem; o Next roda com `TZ=UTC` |
| `medicoes/cap17.py fronteira` | `c17-fronteira.txt` | nenhum: só o build com `cap17-cliente-importa-api.patch` |
| `medicoes/cap18.py` | `c18-mapa.txt` | portas 3000 e 5174 livres |
| `medicoes/cap19.py` | `c19-passos`, `-depuracao`, `-plantao`, `-a11y`, `-gate` | portas 3000 e 5173 livres; sobe a API `cap19` com `TZ` escolhido (meio-dia e 23h na API) |
| `medicoes/porta_dos_fundos.py cap19 cap19` | `c19-porta.txt` | nenhum |
| `medicoes/cookie_navegadores.py` | `c00-cookie-navegadores.txt` | `xvfb-run -a`; WebKitGTK (`webkit2gtk-4.1`, `WebKitWebDriver`) e `pip install selenium` |

`medicoes/tela.py` cria um `git worktree` de cada tag (tela e API), sobe os
servidores e encerra tudo no fim. `cap06-so-disabled.patch` é a variante do
capítulo 6 sem a trava do ref, medida mas não guardada em tag.

As saídas de teste e de lint (`c8-testes-*`, `c8-fronteiras-*`, `c9-tokens-revert`,
`c10-testes-*`, `c10-lint-botoes`, `c15-testes-*`, `c16-mock-antes`, `c16-testes-*`) são o terminal real do `npx vitest run`,
`npx depcruise src` e `npx oxlint` na tag indicada, sem cores ANSI.

`cap02_cookie.py` aceita `firefox` ou `webkit` como argumento
(`playwright install firefox webkit`). A conferência do cookie
`__Host-sessao` fora do Chromium foi feita com `cookie_navegadores.py`:
o WebKitGTK recusa o cookie `Secure` em `http://localhost` e aceita em
`https://localhost` (`npm run dev:https` na tela). O Firefox não foi
testado: o ambiente de produção do livro não conseguiu baixá-lo.

`c19-passo08.txt` é a saída real de `npx vitest run src/app/atendimentos.test.tsx`
na tag `cap19-passo08` (os dois vermelhos de propósito).

## Páginas

| Parte | Capítulos | Páginas |
|---|---|---|
| Frente | capa, sumário, introdução | 6 |
| I · A mudança de paradigma | 1 a 3 | 34 |
| II · Os fundamentos | 4 a 7 | 50 |
| III · Arquitetura | 8 a 12 | 57 |
| IV · A aplicação completa | 13 a 16 | 50 |
| V · Renderização moderna | 17 e 18 | 20 |
| VI · Entrega e referência | 19 e 20 | 27 |
| **Total** | | **244** (orçamento 244, teto 250) |

## Licença

Conteúdo (texto, figuras, estrutura): CC BY-SA 4.0. Código e roteiros:
MIT. Fontes Inter e JetBrains Mono: SIL Open Font License 1.1.
