#!/bin/bash
set -euo pipefail

(cd streamlit_arborist/frontend && npm run build)
python -m build
