.. _releases:

=============
Release Notes
=============

.. currentmodule:: streamlit_arborist

Version 0.4.0 (unreleased)
--------------------------

* Added :py:func:`tree_checkbox` component for checkbox-based multi-select with cascading
  parent/child semantics.

Version 0.3.0 (2026-02-11)
--------------------------

* Added support to select internal nodes in :py:func:`tree_view`.
  When ``select_internal_nodes=True``, the behavior of internal nodes changes:

  - Click the icon to toggle open/closed
  - Click the label to select
  - Double-click the label to select and toggle

Version 0.2.1 (2025-08-24)
--------------------------

* Added support to `Material Symbols <https://fonts.google.com/icons?icon.style=Rounded>`_
  (rounded style) icons.
