#!/usr/bin/env bash
# Gera o bundle local de React 19.3.1 usado por cap01.py no lugar do esm.sh.
# uso: bash medicoes/vendor.sh <pasta de trabalho>   → <pasta>/vendor.js
set -euo pipefail
DEST="${1:?informe uma pasta de trabalho}"
mkdir -p "$DEST" && cd "$DEST"
npm init -y >/dev/null
npm i --no-audit --no-fund react@19.3.1 react-dom@19.3.1 esbuild >/dev/null
cat > entrada.js <<'JS'
import * as R from "react";
import { createRoot } from "react-dom/client";
export const React = R;
export { createRoot };
JS
npx esbuild entrada.js --bundle --format=esm \
  --define:process.env.NODE_ENV='"development"' --outfile=vendor.js
echo "$DEST/vendor.js"
