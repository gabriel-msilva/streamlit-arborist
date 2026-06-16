import json

import streamlit as st

from streamlit_arborist import tree_checkbox, tree_view

st.set_page_config(page_title="streamlit-arborist")


@st.cache_data
def get_data() -> list[dict]:
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


def extract_ids(data, include_internal_nodes=False) -> list:
    ids = []

    for item in data:
        if "children" in item:
            if include_internal_nodes:
                ids.append(item["id"])

            ids.extend(extract_ids(item["children"], include_internal_nodes))
        else:
            ids.append(item["id"])

    return ids


data = get_data()

with st.sidebar:
    st.header("Configuration")
    st.markdown(
        "See all options in the [documentation](https://streamlit-arborist.readthedocs.io/)."
    )

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

    select_internal_nodes = st.checkbox(
        "Select internal nodes",
        value=False,
        help="Click on the icon to toggle, click on the label to select,"
        " or double-click the label to select and toggle.",
    )

    selection = st.selectbox(
        "Selection",
        options=extract_ids(data, include_internal_nodes=select_internal_nodes),
        index=None,
        help="The node id to select and scroll when rendered.",
    )

    checked = st.multiselect(
        "Checked",
        options=extract_ids(data, include_internal_nodes=True),
        default=[],
        help="A list of node ids to check when rendered. Checking an internal node cascades down to its children.",
    )

    search_term = st.text_input(
        "Search term", help="Only show nodes that match this term"
    )

st.title("streamlit-arborist")

st.header("Tree View")


st.markdown(
    """
    - Click on a leaf node (file) to select it.
    - Click on an internal node (folder) to toggle its open/closed state.
    - Use arrow keys to navigate through the tree, then press space to select a node.
    - When `select_internal_node=True`, internal nodes can be selected.

    Explore some of the configurations in the sidebar.
    """
)

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
        select_internal_nodes={select_internal_nodes!r},
        search_term={search_term!r},
        height=300,
    )
    """
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("Interact with the tree view:")

    value = tree_view(
        data,
        icons=icons,
        open_by_default=open_by_default,
        selection=selection,
        select_internal_nodes=select_internal_nodes,
        search_term=search_term,
        height=300,
    )
    print("Tree view value:", value)

with col2:
    st.markdown("Returned value:")

    body = "None" if value is None else json.dumps(value, indent=2)
    st.code(body)

st.divider()

st.header("Tree Checkbox")

st.markdown(
    """
    Each row renders a checkbox.
    Checking an internal node cascades down to its children and a node whose children are only partially checked renders as *indeterminate*.

    Returns the list of fully-checked node IDs.
    """
)

st.code(
    f"""
    from streamlit_arborist import tree_checkbox

    tree_checkbox(
        data,
        icons={icons!r},
        open_by_default={open_by_default!r},
        checked={checked!r},
        search_term={search_term!r},
        height=300,
    )
    """
)

col3, col4 = st.columns(2)

with col3:
    st.markdown("Interact with the checkbox tree:")

    value = tree_checkbox(
        data,
        icons=icons,
        checked=checked,
        open_by_default=open_by_default,
        search_term=search_term,
        height=300,
    )
    print("Checkbox value:", value)

with col4:
    st.markdown("Returned value:")

    body = json.dumps(value, indent=2)
    st.code(body)
