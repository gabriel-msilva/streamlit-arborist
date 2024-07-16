import os
from typing import List, Union

import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = False

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("streamlit_arborist"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "streamlit_arborist",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_arborist", path=build_dir)

# https://github.com/brimdata/react-arborist/blob/v3.4.0/packages/react-arborist/src/types/tree-props.ts


def tree_view(
    data: List[dict],
    # Sizes
    row_height: int = 24,
    width: Union[int, str] = 300,
    height: int = 500,
    indent: int = 24,
    overscan_count: int = 1,
    padding_top: int = None,
    padding_bottom: int = None,
    padding: int = None,
    # Config
    children_accessor: str = "children",
    id_accessor: str = "id",
    open_by_default: bool = True,
    selection_follows_focus: bool = False,
    disable_multi_selection: bool = False,
    # disable_edit: bool = False,
    disable_drag: bool = False,
    disable_drop: bool = False,
    # Selection
    selection: str = None,
    initial_open_state: dict = None,
    # Search
    search_term: str = None,
    # Node style
    leaf_icon: str = None,
    internal_icon: dict = None,
    # Streamlit
    key: str = None,
    on_change=None,
) -> str:
    internal_icon = internal_icon or {}
    icons = {
        "leaf": leaf_icon,
        "internal": {"open": internal_icon["open"], "closed": internal_icon["closed"]},
    }

    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(
        data=data,
        # Sizes
        row_height=row_height,
        overscan_count=overscan_count,
        width=width,
        height=height,
        indent=indent,
        padding_top=padding_top,
        padding_bottom=padding_bottom,
        padding=padding,
        # Config
        children_accessor=children_accessor,
        id_accessor=id_accessor,
        open_by_default=open_by_default,
        selection_follows_focus=selection_follows_focus,
        disable_multi_selection=disable_multi_selection,
        # disable_edit=disable_edit,
        disable_drag=disable_drag,
        disable_drop=disable_drop,
        # Selection
        selection=selection,
        initial_open_state=initial_open_state,
        # Search
        search_term=search_term,
        icons=icons,
        # Streamlit
        key=key,
        on_change=on_change,
        default={},
    )

    return component_value
