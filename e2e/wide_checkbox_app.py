import streamlit as st

from streamlit_arborist import tree_checkbox

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

value = st.sidebar.slider("Test", 0, 10)
replace_data = st.sidebar.checkbox("Replace data")

data = [{"id": "data", "children": [{"id": "child"}]}]
if replace_data:
    data[0]["name"] = "Updated data"
    data[0]["children"].append({"id": "new"})

selected = tree_checkbox(data, key="test_tree")

st.code(str(selected))
st.caption(f"Test value: {value}")
