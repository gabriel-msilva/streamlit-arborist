.. _usage:

=====
Usage
=====

``tree_view()`` displays a tree data structure in Streamlit, pretty much like a file explorer.
It is mostly a wrapper around `react-arborist <https://github.com/brimdata/react-arborist>`_.
Note that not every feature from *react-arborist* is available in *streamlit-arborist*.

.. seealso:: See all available parameters in the :ref:`api`.

Data
----

The data should be a list of dictionaries, where each dictionary represents a node
in the tree.
Each node should have the following keys:

* ``id`` (required)
* ``name``: string to display (optional), and
* ``children``: list of nested nodes (optional)

.. code-block:: python

    from streamlit_arborist import tree_view

    data = [
        {
            "id": "1",
            "name": "Parent 1",
            "children": [
                {"id": "1.1", "name": "Child 1"},
                {"id": "1.2", "name": "Child 2"}
            ]
        },
        {
            "id": "2",
            "name": "Parent 2",
            "children": [
                {"id": "2.1", "name": "Child 3"},
                {"id": "2.2", "name": "Child 4"}
            ]
        }
    ]

    tree_view(data)

You may include additional keys in the node's data:

.. code-block:: python

    data = [
        {"id": "1", "name": "Node 1", "description": "This is node 1"},
        {"id": "2", "name": "Node 2", "description": "This is node 2"}
    ]

Change the default key names using ``children_accessor`` and ``id_accessor``.

.. code-block:: python

    data = [{"key": "A", "contents": [{"key": "A.1"}, {"key": "A.2"}]}]
    tree_view(data, children_accessor="contents", id_accessor="key")

Selection
---------

Select leaf nodes by clicking on them.
The component returns the selected nodes' data, including extra keys.

.. code-block:: python

    >>> selected = tree_view(data)
    >>> selected
    {"id": "1.1", "name": "Child 1"}

Programmatically select a node by passing its *id*:

.. code-block:: python

    tree_view(data, selection="1.1")

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

    tree_view(data, search_term="Child")


Combine it with `st.text_input() <https://docs.streamlit.io/develop/api-reference/widgets/st.text_input>`_
to allow users to search interactively:

.. code-block:: python

    import streamlit as st

    search_term = st.text_input("Search term")
    tree_view(data, search_term=search_term)
