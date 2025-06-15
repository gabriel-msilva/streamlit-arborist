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

The development environment is managed with [pixi](https://pixi.sh/latest/).

### Setup

1. Install the `dev` environment defined in [pyproject.toml](./pyproject.toml):

   ```sh
   pixi install --frozen
   ```

2. Install `npm` packages in [streamlit_arborist/frontend](./streamlit_arborist/frontend/):

   ```sh
   pixi run npm
   ```

### Running

1. Run the [example.py](./streamlit_arborist/example.py) app file with Streamlit:

   ```sh
   pixi run backend
   ```

2. Start the component's frontend server:

   ```sh
   pixi run frontend
   ```

Open the app running at <http://localhost:8501>.
