# Agent instructions

Read [CONTRIBUTING.md](./CONTRIBUTING.md) first.

## Project layout

```text
.
├── streamlit_arborist/
│   ├── __init__.py      # Python API
│   └── frontend/src/    # React components
├── app/                 # Demo app, also used by the end-to-end tests
├── e2e/                 # End-to-end tests
└── docs/                # Sphinx documentation and release notes
```

## Changing a component parameter

- Update the signature and docstring in [`__init__.py`](./streamlit_arborist/__init__.py),
  the `_component_func()` call,
  and `args["snake_case_name"]` in `TreeView.tsx` or `TreeCheckbox.tsx`.
- Keep parameters shared by both components in sync.
- Add an end-to-end test, and an example to [usage.rst](./docs/usage.rst) if useful.
- Add every user-facing change, including fixes, to [releases.rst](./docs/releases.rst).

## Code

- Use blank lines to separate logical blocks of code.
- The docs build uses `--nitpicky`, so broken references in docstrings fail it.

## Testing

- Prefer the [headless test run](./CONTRIBUTING.md#testing) to `mise run tests`.
- Run `mise run frontend-build` after frontend changes, or the tests use stale assets.
- [conftest.py](./e2e/conftest.py) finds elements in [example.py](./app/example.py) by position.
  Changing the demo app's layout can break tests.
- Test other scenarios with a small app,
  like [test_tree_view_data.py](./e2e/test_tree_view_data.py).
- Wait with `expect()` or `wait_for_render()`, never with `wait_for_timeout()` or `time.sleep()`.

## Writing documentation

In Markdown and reStructuredText, put each sentence on its own line and wrap at 100 characters:

```md
<!-- wrong -->

First sentence. Second sentence.

<!-- right -->

First sentence.
Second sentence.
```

## Commits

Split unrelated changes into separate commits, each with a single prefix.
