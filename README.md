# streamlit-arborist

Streamlit component for creating tree views.

## Installation instructions

```sh
pip install streamlit-arborist
```

## Usage instructions

```python
import streamlit as st

from streamlit_arborist import streamlit_arborist

value = streamlit_arborist()

st.write(value)
```

## Development

This repository is based on
[streamlit/component-template](https://github.com/streamlit/component-template) template.

The development environment requires
[uv](https://docs.astral.sh/uv/getting-started/installation/)
and [Node.js + npm](https://nodejs.org/en/download/current) installed.

### Setup

Install the `dev` Python environment defined in [pyproject.toml](./pyproject.toml)
and `npm` packages in [streamlit_arborist/frontend](./streamlit_arborist/frontend/):

```sh
make setup
```

### Running

1. Run the [example.py](./streamlit_arborist/example.py) app file with Streamlit:

   ```sh
   make backend
   ```

2. Start the component's frontend server:

   ```sh
   make frontend
   ```

Open the app running at <http://localhost:8501>.

### Build

Set `_RELEASE = True` in [`__init__.py`](./streamlit_arborist/__init__.py) and run:

```sh
make build
```
