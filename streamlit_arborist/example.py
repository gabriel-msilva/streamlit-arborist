import streamlit as st

from streamlit_arborist import tree_view

DATA = [
    {"id": "1", "name": "Unread"},
    {"id": "2", "name": "Threads"},
    {
        "id": "3",
        "name": "Chat Rooms",
        "children": [
            {"id": "c1", "name": "General"},
            {"id": "c2", "name": "Random"},
            {"id": "c3", "name": "Open Source Projects"},
        ],
    },
    {
        "id": "4",
        "name": "Direct Messages",
        "children": [
            {"id": "d1", "name": "Alice"},
            {"id": "d2", "name": "Bob"},
            {"id": "d3", "name": "Charlie"},
        ],
    },
]

st.markdown(
    """
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.5.2/css/all.min.css">
    """,
    unsafe_allow_html=True,
)

st.header("Streamlit Arborist")

with st.sidebar:
    search_term = st.text_input("Search term")
    value = tree_view(DATA, height=250, search_term=search_term)


st.markdown("Selected data:")
st.json(value)
