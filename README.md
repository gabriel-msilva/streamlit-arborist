# streamlit-arborist

[![CI - Test, Build and Release](https://github.com/gabriel-msilva/streamlit-arborist/actions/workflows/test-build-release.yaml/badge.svg)](https://github.com/gabriel-msilva/streamlit-arborist/actions/workflows/test-build-release.yaml)
![PyPI - Version](https://img.shields.io/pypi/v/streamlit-arborist)
![PyPI - License](https://img.shields.io/pypi/l/streamlit-arborist)

_streamlit-arborist_ is a [Streamlit](https://streamlit.io) component based on
[react-arborist](https://github.com/brimdata/react-arborist) for visualizing
hierarchical data structures as interactive tree views.

## Installation

```sh
pip install streamlit-arborist
```

## Basic usage

```python
from streamlit_arborist import tree_view

data = [
   {
      "id": "1",
      "name": "Parent 1",
      "children": [
         {"id": "1.1", "name": "Child 1"},
         {"id": "1.2", "name": "Child 2"}
      ]
   },
   {
      "id": "2",
      "name": "Parent 2",
      "children": [
         {"id": "2.1", "name": "Child 3"},
         {"id": "2.2", "name": "Child 4"}
      ]
   }
]

tree_view(data)
```

```sh
streamlit run app.py
```

## Development

This repository is based on
[streamlit/component-template](https://github.com/streamlit/component-template) template.
Find details about
[custom components](https://docs.streamlit.io/develop/concepts/custom-components)
in Streamlit documentation.

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

While developing the frontend, set `_RELEASE = False` in [`__init__.py`](./streamlit_arborist/__init__.py).

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

### Documentation

The documentation files are located in [docs/](./docs/) directory and written with
[Sphinx](https://www.sphinx-doc.org/en/).

```sh
make docs
```
