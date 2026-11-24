import functools
from collections.abc import Callable

import streamlit.components.v2
from streamlit.elements.lib.utils import Key
from streamlit.string_util import validate_icon_or_emoji

from streamlit_arborist._version import get_version_dict

__version__ = get_version_dict()["version"]


@functools.cache
def _get_component():
    # Streamlit finds the assets with the manifest in `streamlit_arborist/pyproject.toml`
    # only while its runtime is running, so registering at import time would fail.
    return streamlit.components.v2.component(
        "streamlit-arborist.streamlit_arborist",
        html='<div class="react-root"></div>',
        css="index-*.css",
        js="index-*.js",
    )


# See `TreeProps` type in the react-arborist package:
# https://github.com/brimdata/react-arborist/blob/v3.4.0/packages/react-arborist/src/types/tree-props.ts
def tree_view(
    data: list[dict],
    icons: dict[str, str] | None = None,
    # Sizes
    row_height: int = 24,
    width: int | str = "auto",
    height: int = 500,
    indent: int = 24,
    overscan_count: int = 1,
    padding_top: int | None = None,
    padding_bottom: int | None = None,
    padding: int | None = None,
    # Config
    children_accessor: str = "children",
    id_accessor: str = "id",
    open_by_default: bool = True,
    # Selection
    selection: str | None = None,
    select_internal_nodes: bool = False,
    initial_open_state: dict[str, bool] | None = None,
    # Search
    search_term: str | None = None,
    # Streamlit
    key: Key | None = None,
    on_change: Callable[..., None] | None = None,
) -> dict | None:
    """
    Display a tree view.

    Parameters
    ----------
    data : list of dict
        A list of dictionaries representing the tree data.
        Each dictionary must have an `id` key.
        Optional keys are `name` for display (otherwise uses `id`), and `children` for
        child nodes.

        Passing different `data` on a rerun updates the tree.
        Nodes keep their open/closed state as long as their ID does not change.

    icons : dict, optional
        A dict of keys ``"open"``, ``"closed"``, and ``"leaf"`` with string values
        representing the icons to use for open internal nodes, closed internal nodes,
        and leaf nodes, respectively.

        The following options are valid values:

        * A single-character emoji.
          For example, you can set ``icons={"open": "🔓", "closed": "🔒", "leaf": "🍀"}``.
          Emoji short codes are not supported.

        * An icon from the Material Symbols library (rounded style) in the format
          ``":material/icon_name:"`` where `icon_name` is the name of the icon in
          snake case.

    row_height : int, default 24
        Height of each row in pixels.

    width : int or str, default "auto"
        View width in pixels or a valid
        `CSS width <https://developer.mozilla.org/pt-BR/docs/Web/CSS/width>`_ string.

    height : int, default 500
        View height in pixels.

    indent : int, default 24
        Node indentation in pixels.

    overscan_count : int, default 1
        Number of additional rows rendered outside the visible viewport to ensure smooth
        scrolling and better performance.

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

    select_internal_nodes : bool, default False
        If False, clicking an internal node only toggles open/closed.
        If True, internal (non-leaf) nodes can be selected:

        - Single-click the icon to toggle open/closed
        - Single-click the label to select
        - Double-click the label to select and toggle

    initial_open_state : dict[str, bool], optional
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
        An optional callback invoked when a node is selected.
        No arguments are passed to it.

    Returns
    -------
    dict or None
        The data of the selected node.
        Returns `None` if no node is selected.

    Examples
    --------
    The data should be a list of dictionaries, where each dictionary represents a node
    in the tree.
    Each node should have the following keys:

    * ``id`` (required)
    * ``name``: string to display (optional), and
    * ``children``: list of nested nodes (optional)

    Nodes without ``children`` key are considered leafs.

    >>> data = [
    ...     {
    ...         "id": "1",
    ...         "name": "Parent 1",
    ...         "children": [
    ...             {"id": "1.1", "name": "Child 1"},
    ...             {"id": "1.2", "name": "Child 2"}
    ...         ]
    ...     },
    ...     {
    ...         "id": "2",
    ...         "name": "Parent 2",
    ...         "children": [
    ...             {"id": "2.1", "name": "Child 3"},
    ...             {"id": "2.2", "name": "Child 4"}
    ...         ]
    ...     }
    ... ]

    >>> from streamlit_arborist import tree_view
    >>> tree_view(data)
    """
    icons = _normalize_icons(icons or {})

    result = _get_component()(
        data={
            "widget": "view",
            "data": data,
            "icons": icons,
            # Sizes
            "row_height": row_height,
            "overscan_count": overscan_count,
            "width": width,
            "height": height,
            "indent": indent,
            "padding_top": padding_top,
            "padding_bottom": padding_bottom,
            "padding": padding,
            # Config
            "children_accessor": children_accessor,
            "id_accessor": id_accessor,
            "open_by_default": open_by_default,
            # Selection
            "selection": selection,
            "select_internal_nodes": select_internal_nodes,
            # Open State
            "initial_open_state": initial_open_state,
            # Search
            "search_term": search_term,
        },
        # Streamlit
        key=key,
        default={"selected": None},
        on_selected_change=on_change or _noop,
    )

    # The result is empty when there's no script run context.
    return result.get("selected")


def tree_checkbox(
    data: list[dict],
    icons: dict[str, str] | None = None,
    # Sizes
    row_height: int = 24,
    width: int | str = "auto",
    height: int = 500,
    indent: int = 24,
    overscan_count: int = 1,
    padding_top: int | None = None,
    padding_bottom: int | None = None,
    padding: int | None = None,
    # Config
    children_accessor: str = "children",
    id_accessor: str = "id",
    open_by_default: bool = True,
    # Selection
    checked: list[str] | None = None,
    initial_open_state: dict[str, bool] | None = None,
    # Search
    search_term: str | None = None,
    # Streamlit
    key: Key | None = None,
    on_change: Callable[..., None] | None = None,
) -> list[str]:
    """
    Display a tree view with checkboxes and cascading multi-selection.

    Checking a parent cascades the checked state to all children; unchecking does the inverse.
    A parent whose children are only partially checked renders as **indeterminate**
    and is *not* included in the returned list.

    Parameters
    ----------
    data : list of dict
        A list of dictionaries representing the tree data.
        Each dictionary must have an `id` key.
        Optional keys are `name` for display (otherwise uses `id`), and `children` for
        child nodes.

        Passing different `data` on a rerun updates the tree.
        Nodes keep their open/closed state as long as their ID does not change.

    icons : dict, optional
        A dict of keys ``"open"``, ``"closed"``, and ``"leaf"`` with string values
        representing the icons to use for open internal nodes, closed internal nodes,
        and leaf nodes, respectively.

        The following options are valid values:

        * A single-character emoji.
          For example, you can set ``icons={"open": "🔓", "closed": "🔒", "leaf": "🍀"}``.
          Emoji short codes are not supported.

        * An icon from the Material Symbols library (rounded style) in the format
          ``":material/icon_name:"`` where `icon_name` is the name of the icon in
          snake case.

    row_height : int, default 24
        Height of each row in pixels.

    width : int or str, default "auto"
        View width in pixels or a valid
        `CSS width <https://developer.mozilla.org/pt-BR/docs/Web/CSS/width>`_ string.

    height : int, default 500
        View height in pixels.

    indent : int, default 24
        Node indentation in pixels.

    overscan_count : int, default 1
        Number of additional rows rendered outside the visible viewport to ensure smooth
        scrolling and better performance.

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

    checked : list of str, optional
        Initial set of checked node IDs.
        Checking an internal node checks itself *and* all children.

        Passing a different list on subsequent re-runs does not overwrite frontend state.
        Passing different `data` resets the checked state to `checked`.

    initial_open_state : dict[str, bool], optional
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
        An optional callback invoked when a node is selected.
        No arguments are passed to it.

    Returns
    -------
    list of str
        IDs of every node that is **fully** checked, including internal nodes whose
        children are all checked.
        Indeterminate nodes are omitted.

    Examples
    --------
    >>> from streamlit_arborist import tree_checkbox
    >>> data = [
    ...     {
    ...         "id": "1",
    ...         "name": "Parent 1",
    ...         "children": [
    ...             {"id": "1.1", "name": "Child 1"},
    ...             {"id": "1.2", "name": "Child 2"},
    ...         ],
    ...     }
    ... ]
    >>> tree_checkbox(data)

    Including an internal node in the checked list also cascades down to its children:

    >>> tree_checkbox(data, checked=["1"])
    ['1', '1.1', '1.2']
    """
    icons = _normalize_icons(icons or {})
    checked = list(checked) if checked else []

    result = _get_component()(
        data={
            "widget": "checkbox",
            "data": data,
            "icons": icons,
            # Sizes
            "row_height": row_height,
            "overscan_count": overscan_count,
            "width": width,
            "height": height,
            "indent": indent,
            "padding_top": padding_top,
            "padding_bottom": padding_bottom,
            "padding": padding,
            # Config
            "children_accessor": children_accessor,
            "id_accessor": id_accessor,
            "open_by_default": open_by_default,
            # Selection
            "checked": checked,
            # Open State
            "initial_open_state": initial_open_state,
            # Search
            "search_term": search_term,
        },
        # Streamlit
        key=key,
        default={"checked": checked},
        on_checked_change=on_change or _noop,
    )

    return result.get("checked", checked)


def _noop() -> None:
    pass


def _normalize_icons(icons: dict) -> dict:
    result = {}

    for key in ("open", "closed", "leaf"):
        value = icons.get(key) or None  # `None` over empty string
        result[key] = validate_icon_or_emoji(value)

    return result
