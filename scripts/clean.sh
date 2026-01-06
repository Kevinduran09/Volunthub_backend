#!/usr/bin/env bash
set -euo pipefail

# Ejecuta desde la raíz del repo
ROOT_DIR="$(pwd)"

echo "Cleaning Python caches and build artifacts in: $ROOT_DIR"

# Directorios típicos a borrar
DIR_PATTERNS=(
  "__pycache__"
  ".pytest_cache"
  ".mypy_cache"
  ".ruff_cache"
  ".hypothesis"
  ".coverage"
  "htmlcov"
  "dist"
  "build"
  "*.egg-info"
  ".eggs"
  ".tox"
  ".nox"
  ".cache"
  ".pytype"
  ".dmypy.json"
  ".pyre"
)

# Borra directorios por nombre
for name in "${DIR_PATTERNS[@]}"; do
  find "$ROOT_DIR" -type d -name "$name" -prune -exec rm -rf {} + 2>/dev/null || true
done

# Borra archivos comunes
FILE_PATTERNS=(
  ".coverage"
  "coverage.xml"
  "*.pyc"
  "*.pyo"
  "*.pyd"
  "*.log"
)

for
