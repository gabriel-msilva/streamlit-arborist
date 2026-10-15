import streamlit as st

from streamlit_arborist import tree_view

replace_data = st.checkbox("Replace data")

data = [{"id": "data", "name": "Data", "children": [{"id": "child", "name": "Child"}]}]
if replace_data:
    data[0]["name"] = "Updated data"
    data[0]["children"].append({"id": "new", "name": "New child"})

tree_view(data, key="tree_view")
