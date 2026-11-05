# Estado & Tela

**Aplicações web reativas com React, do DOM manipulado à mão até uma
aplicação completa, autenticada e testada, construída com agentes de IA
sem perder o controle do código.**

Manual de campo em produção · lotes 1 a 5 (capa, introdução e capítulos 1 a 12)
· organizado por Prof. Rogério Silva e Claude Opus 5.5 · 2026 · TEC.1052
Programação para Internet II · ADS · IFPI

## Os três repositórios

| Repositório | O que tem |
|---|---|
| `estado-e-tela-ebook` | este livro, os roteiros de medição e as saídas |
| `estado-e-tela-web` | o Mini-Prontuário em React, uma tag por capítulo |
| `estado-e-tela-api` | a API (fork da tag `cap16` do Crachá & Porta Express) |

## Montar o livro

O build lê o código direto do repositório da tela, na tag de cada
capítulo. Clone os três lado a lado com os nomes `ebook`, `web` e `api`
(ou aponte `ESTADO_WEB` e `ESTADO_API` para outro lugar).

```bash
pip install playwright pypdf && playwright install chromium
cd fonte && python3 build.py && cd ..          # index.html
python3 fonte/pdf.py "$PWD/index.html" "$PWD/Estado-e-Tela.pdf"
python3 fonte/medir.py Estado-e-Tela.pdf --json # páginas × orçamento
python3 fonte/build.py                          # de novo: sumário com páginas
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

`medicoes/tela.py` cria um `git worktree` de cada tag (tela e API), sobe os
servidores e encerra tudo no fim. `cap06-so-disabled.patch` é a variante do
capítulo 6 sem a trava do ref, medida mas não guardada em tag.

As saídas de teste e de lint (`c8-testes-*`, `c8-fronteiras-*`, `c9-tokens-revert`,
`c10-testes-*`, `c10-lint-botoes`) são o terminal real do `npx vitest run`,
`npx depcruise src` e `npx oxlint` na tag indicada, sem cores ANSI.

`cap02_cookie.py` aceita `firefox` ou `webkit` como argumento
(`playwright install firefox webkit`).

## Licença

Conteúdo (texto, figuras, estrutura): CC BY-SA 4.0. Código e roteiros:
MIT. Fontes Inter e JetBrains Mono: SIL Open Font License 1.1.
