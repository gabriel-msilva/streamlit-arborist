.. _usage:

=====
Usage
=====

.. currentmodule:: streamlit_arborist

*streamlit-arborist* is mostly a wrapper around `react-arborist <https://github.com/brimdata/react-arborist>`_.
Note that not every feature from *react-arborist* is available in *streamlit-arborist*.

It exposes two custom components:

- :py:func:`tree_view`: display a tree and let the user pick **one** node.
  Use when the user picks a single node, e.g. file pickers or navigation
- :py:func:`tree_checkbox`: display a tree with a checkbox per row for **multi-selection with cascading**.
  Use when the user picks a *set* of nodes, e.g. picking categories or selecting items for a downstream operation.

Both components share almost all parameters, including appearance and search options.

.. seealso::

    See all available parameters in the :ref:`api`.

Data
----

The data should be a list of dictionaries, where each dictionary represents a node in the tree.
Each node should have the following keys:

* ``id`` (required)
* ``name``: string to display (optional), and
* ``children``: list of nested nodes (optional)

.. code-block:: python

    from streamlit_arborist import tree_view

    data = [
        {
            "id": "1",
            "name": "Child 1",
        },
        {
            "id": "2",
            "name": "Parent 2",
            "children": [
                {"id": "2.1", "name": "Child 2.1"},
                {"id": "2.2", "name": "Child 2.2"}
            ]
        }
    ]

    tree_view(data)

You may include additional keys in the node's data:

.. code-block:: python

    data2 = [
        {"id": "1", "name": "Node 1", "description": "This is node 1"},
        {"id": "2", "name": "Node 2", "description": "This is node 2"}
    ]

    tree_view(data2)

Change the default key names using ``children_accessor`` and ``id_accessor``.

.. code-block:: python

    data3 = [{"key": "A", "contents": [{"key": "A.1"}, {"key": "A.2"}]}]
    tree_view(data3, children_accessor="contents", id_accessor="key")

Single selection (``tree_view``)
--------------------------------

:py:func:`tree_view` allows selecting leaf nodes by clicking on them.
The component returns the selected node's data, including extra keys.

.. code-block:: python

    >>> selected = tree_view(data)
    >>> selected
    {"id": "1.1", "name": "Child 1"}

Row interaction:

- Click a leaf node to select it.
- Click an internal node to toggle open/closed.
- Use arrow keys and space to interact via the keyboard.

Programmatically select a node by passing its *id*:

.. code-block:: python

    tree_view(data, selection="2.1")

Set ``select_internal_nodes=True`` to allow the selection of internal nodes.
The behavior of internal nodes changes:

- Click the icon to toggle open/closed
- Click the label to select
- Double-click the label to select and toggle

Selecting an internal node returns the node's data, including the ``children`` key.

.. code-block:: python

    >>> selected = tree_view(data, select_internal_nodes=True)
    >>> selected
    {
        "id": "2",
        "name": "Parent 2",
        "children": [
            {"id": "2.1", "name": "Child 2.1"},
            {"id": "2.2", "name": "Child 2.2"}
        ]
    }

Checkbox multi-selection (``tree_checkbox``)
--------------------------------------------

Use :py:func:`tree_checkbox` allow users to select multiple nodes with checkboxes.
The component returns a list of fully-checked node IDs.

Checking an internal node cascades down to its children, and a node whose children are only partially checked renders as *indeterminate*.

.. code-block:: python

    from streamlit_arborist import tree_checkbox

    tree_checkbox(data)

Row interaction:

- Click the chevron at the start of an internal row to open/close
  (does not change the check state).
- Click anywhere on a row (or its checkbox) to toggle the check.
  Internal nodes cascade to all children.
- Double-click an internal row to toggle the check *and* open/close in one gesture.
- Press space on a focused row to toggle the check via the keyboard.

Set the initial checked state with the ``checked`` argument:

.. code-block:: python

    >>> checked = tree_checkbox(data, checked=["1.1"])
    >>> checked
    ['1.1']

Including an internal node auto-checks its children, so the returned list may be a
superset of what you passed in:

.. code-block:: python

    >>> checked = tree_checkbox(data, checked=["1"])
    >>> checked
    ['1', '1.1', '1.2']

.. note::

    The ``checked`` argument is applied only on the initial render.
    Passing a different list on subsequent Streamlit reruns does not overwrite the user's interactive state.
    To reset the widget, pass a new ``key``.

Appearance
----------

Set icons for *open*/*closed* internal nodes and *leaf* nodes using the ``icons``
parameter.

.. code-block:: python

    tree_view(data, icons={"open": "📂", "closed": "📁", "leaf": "📄"})

Material Symbols icons are also supported.

.. code-block:: python

    tree_view(
        data,
        icons={
            "open": ":material/folder_open:",
            "closed": ":material/folder:",
            "leaf": ":material/docs:"
        }
    )

Customize sizes and padding:

.. code-block:: python

    tree_view(
        data,
        row_height=30,
        height=400,
        padding_top=10,
    )

Search
------

Add a search term to filter matching names:

.. code-block:: python

    tree_checkbox(data, search_term="Child")


Combine it with `st.text_input() <https://docs.streamlit.io/develop/api-reference/widgets/st.text_input>`_
to allow users to search interactively:

.. code-block:: python

    import streamlit as st

    search_term = st.text_input("Search term")
    tree_checkbox(data, search_term=search_term)
