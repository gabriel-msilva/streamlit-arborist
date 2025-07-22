#!/bin/bash
set -euo pipefail

pre-commit install
playwright install
(cd streamlit_arborist/frontend && npm clean-install)
