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
   pixi install --environment dev
   pixi shell --environment dev
   ```

2. Install `npm` package in [streamlit_arborist/frontend](./streamlit_arborist/frontend/):

   ```sh
   cd streamlit_arborist/frontend
   npm clean-install
   ```

### Running

1. Run the [example.py](./streamlit_arborist/example.py) app file with Streamlit:

   ```sh
   # http://localhost:8501
   streamlit run streamlit_arborist/example.py
   ```

2. Start the component's frontend server:

   ```sh
   # http://localhost:3001
   cd streamlit_arborist/frontend
   npm run start
   ```
