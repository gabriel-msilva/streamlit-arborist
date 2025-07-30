import streamlit as st

from streamlit_arborist import tree_view

st.set_page_config("streamlit-arborist", initial_sidebar_state="expanded")


@st.cache_data
def get_data():
    return [
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


def extract_ids(data) -> list:
    ids = []

    for item in data:
        ids.append(item["id"])

        if "children" in item:
            ids.extend(extract_ids(item["children"]))

    return ids


data = get_data()

with st.sidebar:
    st.header("Instructions")
    st.markdown(
        """
    - Click on a node to select it.
    - Click on a node icon to open or close it.
    - Press Shift + Click to select multiple nodes.
    - Use arrow keys to navigate through the tree, then press space to select a node.
    """
    )
    st.header("Configuration")
    st.markdown("See all options in the [documentation]().")

    with st.expander("Icons", expanded=True):
        col1, col2, col3 = st.columns(3)
        icons = {
            "open": col1.text_input("Open", value="📂"),
            "closed": col2.text_input("Closed", value="📁"),
            "leaf": col3.text_input("Leaf", value="📄"),
        }

    open_by_default = st.checkbox(
        "Open by default",
        value=True,
        help="Whether to open nodes by default when rendered.",
    )

    selection = st.selectbox(
        "Selection",
        options=extract_ids(data),
        index=None,
        help="The node id to select and scroll when rendered.",
    )

    disable_multi_selection = st.checkbox(
        "Disable multi-selection",
        value=False,
        help="Whether to disable multi-selection of nodes.",
    )

    search_term = st.text_input("Search term")

st.title("streamlit-arborist")

st.header("Tree View")

with st.expander("Sample data"):
    st.json(data)

st.code(
    f"""
    from streamlit_arborist import tree_view

    tree_view(
        data,
        icons={icons!r},
        open_by_default={open_by_default!r},
        selection={selection!r},
        search_term={search_term!r},
        disable_multi_selection={disable_multi_selection!r},
        height=300,
    )
    """
)

col1, col2 = st.columns(2)

with col1:
    value = tree_view(
        data,
        icons=icons,
        open_by_default=open_by_default,
        selection=selection,
        search_term=search_term,
        disable_multi_selection=disable_multi_selection,
        height=300,
    )

with col2:
    st.markdown("Selected data:")
    st.json(value)
