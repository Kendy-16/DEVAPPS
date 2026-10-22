#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
export UV_LINK_MODE=copy
if ! command -v uv >/dev/null 2>&1; then
  echo "No se encuentra uv. Instala desde https://docs.astral.sh/uv/" >&2
  exit 1
fi
uv sync --python 3.13
uv run reflex run
