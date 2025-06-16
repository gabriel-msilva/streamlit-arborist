import os
from functools import partial
from typing import Dict, List, Union

import streamlit.components.v1 as components
from streamlit.runtime.state import WidgetArgs, WidgetCallback, WidgetKwargs

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
    icons: Dict[str, str] = None,
    # Sizes
    row_height: int = 24,
    width: Union[int, str] = "100%",
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
    initial_open_state: Dict[str, bool] = None,
    # Search
    search_term: str = None,
    # Streamlit
    key: Union[str, int] = None,
    on_change: WidgetCallback = None,
    args: WidgetArgs = None,
    kwargs: WidgetKwargs = None,
) -> dict:
    """
    Create a tree view.

    Parameters
    ----------
    data : List[dict]
        A list of dictionaries representing the tree data.
        Each dictionary should have an `id` and `name` keys, and may have a `children`
        key containing a list of child nodes.

    icons : dict, optional
        A dict of keys ``"open"``, ``"closed"``, and ``"leaf"`` with string values
        representing the icons to use for open internal nodes, closed internal nodes,
        and leaf nodes, respectively.

    row_height : int, default 24

    overscan_count : int, default 1
        Number of additional rows rendered outside the visible viewport to ensure smooth
        scrolling and better performance.

    width : int or str, default 300
        View width in pixels or as a CSS width string (e.g. ``"auto"``).
        https://developer.mozilla.org/pt-BR/docs/Web/CSS/width

    height : int, default 500
        View height in pixels.

    indent : int, optional
        Node indendation in pixels, by default 24

    padding_top : int, optional
        Space between the tree and its top border, in pixels.

    padding_bottom : int, optional
        Space between the tree and its bottom border, in pixels.

    padding : int, optional
        Space between the tree and its top/bottom borders, in pixels.
        Overrides both `padding_top` and `padding_bottom`.

    children_accessor : str, default "children"
        The children key in the tree data.

    id_accessor : str, default "id"
        The ID key in the tree data.

    open_by_default : bool, default True
        Whether all nodes should be open when rendered.

    selection : str or int, optional
        The node `id` to select and scroll when rendered.

    initial_open_state : Dict[str, bool], optional
        A dict of node ID keys and bool values indicating whether the node is open
        (`True`) or closed (`False`) when rendered.

    search_term : str, optional
        Only show nodes that match `search_term`.
        If a child matches, all its parents also match.
        Internal nodes are opened when filtering.

    key : str, optional
        An optional string or integer to use as the unique key for the widget.
        If this is omitted, a key will be generated for the widget based on its content.
        Multiple widgets of the same type may not share the same key.

    on_change : callable, optional
        An optional callback invoked when the widget's value changes. No arguments are passed to it.

    args : tuple, optional
        A tuple of arguments to pass to the `on_change` callback.

    kwargs : dict, optional
        An optional dict of kwargs to pass to the `on_change` callback.

    Returns
    -------
    dict
        A dictionary representing the selected node, or an empty dictionary if no node
        is selected.
    """
    icons = icons or {}
    icons = {
        "open": icons.get("icons", "📂"),
        "closed": icons.get("closed", "📁"),
        "leaf": icons.get("leaf", "📄"),
    }

    args = args or ()
    kwargs = kwargs or {}
    on_change = partial(on_change, *args, **kwargs) if on_change else None

    component_value = _component_func(
        data=data,
        icons=icons,
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
        # Open State
        initial_open_state=initial_open_state,
        # Search
        search_term=search_term,
        # Streamlit
        key=key,
        on_change=on_change,
        default={},
    )

    return component_value
