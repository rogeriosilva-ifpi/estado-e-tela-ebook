# Estado & Tela

**Aplicações web reativas com React, do DOM manipulado à mão até uma
aplicação completa, autenticada e testada, construída com agentes de IA
sem perder o controle do código.**

Manual de campo em produção · lote 1 (capa, introdução e capítulos 1 a 3)
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

## Medições do lote 1

| Roteiro | Saída | Pré-requisito |
|---|---|---|
| `medicoes/cap01.py` | `c1-ala.txt` | `bash medicoes/vendor.sh /tmp/v` (React local) |
| `medicoes/cap02_cookie.py` | `c2-cookie-chromium.txt` | API em :3000 e `npm run dev` |
| `medicoes/cap03.py` | `c3-renderometro.txt` | `npm run dev` na tag `cap03` |

`cap02_cookie.py` aceita `firefox` ou `webkit` como argumento
(`playwright install firefox webkit`).

## Licença

Conteúdo (texto, figuras, estrutura): CC BY-SA 4.0. Código e roteiros:
MIT. Fontes Inter e JetBrains Mono: SIL Open Font License 1.1.
