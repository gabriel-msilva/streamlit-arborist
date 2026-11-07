# Contributing to streamlit-arborist

Thanks for your interest in contributing!
Bug reports and feature ideas are welcome in the
[issue tracker](https://github.com/gabriel-msilva/streamlit-arborist/issues).

This repository is based on the
[streamlit/component-template](https://github.com/streamlit/component-template) template.
See the Streamlit documentation on
[custom components](https://docs.streamlit.io/develop/concepts/custom-components) for background.

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

The project has two parts:

- A Python package in [streamlit_arborist/](./streamlit_arborist/) that exposes the components.
- A React frontend in [streamlit_arborist/frontend/](./streamlit_arborist/frontend/) that renders
  the trees.

## Setup

Development tools and commands are managed with [mise](https://mise.jdx.dev/installing-mise.html).
After installing it, run from the repository root:

```sh
mise install
mise run setup
```

List all available commands with `mise tasks`.

> [!NOTE]
> `uv` picks the Python version from [.python-version](./.python-version), which is the oldest
> supported version.

## Running the example app

Start the Streamlit backend and the frontend development server in parallel:

```sh
mise run backend ::: frontend
```

Open the app running at <http://localhost:8501>.
Changes to the frontend reload automatically.

The `backend` and `tests` tasks set `STREAMLIT_ARBORIST_DEV=true`, which makes the component load
from the frontend development server at <http://localhost:3001> instead of the built assets.

## Testing

End-to-end tests in [e2e/](./e2e/) use `pytest` and Playwright.
With the frontend development server running (`mise run frontend`), run:

```sh
mise run tests
```

The tests open a browser window.
Extra arguments are passed to pytest, for example `mise run tests -- -k checkbox`.

To test the built frontend headlessly in Firefox and Chromium, as CI does:

```sh
mise run build
uv run pytest --browser firefox --browser chromium
```

## Linting

`pre-commit` hooks format and lint the code on every commit.
To run them manually on all files:

```sh
mise run lint
```

## Documentation

The documentation in [docs/](./docs/) is written with [Sphinx](https://www.sphinx-doc.org/en/).
Build it at `docs/_build/html/`:

```sh
mise run docs
```

Remove the built pages with `mise run docs-clean`.

## Building

Build the frontend at `streamlit_arborist/frontend/build/` and the Python package at `dist/`:

```sh
mise run build
```

The frontend is rebuilt only when its sources change.

## Updating tool versions

Change the versions in [.tool-versions](./.tool-versions) and run `mise install`.
The same file is read by `mise`, the GitHub Actions workflow, and Read the Docs.
`mise` doesn't lock tools declared in `.tool-versions`, so there is no `mise.lock` to update.

## Continuous integration

The [GitHub Actions workflow](./.github/workflows/test-build-release.yaml) runs the `pre-commit`
hooks, the end-to-end tests on every supported Python version, and the documentation build on each
pull request and push to `main`.
Pull requests also build the package.

## Commit messages

Start commit messages with a prefix describing the type of change, followed by a short summary in
the imperative mood, for example `FIX: Re-render tree_view when data changes`.

| Prefix     | Use for                                          |
| ---------- | ------------------------------------------------ |
| `FEAT`     | New features                                     |
| `FIX`      | Bug fixes                                        |
| `REFACTOR` | Code changes that don't change behavior          |
| `TST`      | Tests                                            |
| `DOCS`     | Documentation                                    |
| `BLD`      | Build system, dependencies and development tools |
| `CI`       | GitHub Actions workflows                         |
| `AI`       | Instructions and skills for AI coding agents     |

## Releasing

The package version comes from the Git tag.
Pushing a tag makes CI build the package and publish it to PyPI.

1. Add the changes to [docs/releases.rst](./docs/releases.rst) under `Version X.Y.Z (unreleased)`.
2. To publish a release candidate, tag the branch's latest commit with `X.Y.ZrcN` and push the tag.
3. When the release is ready, replace `(unreleased)` with the release date, and update the version
   pinned in [app/requirements.txt](./app/requirements.txt) for the demo app.
4. After merging to `main`, create a
   [GitHub release](https://github.com/gabriel-msilva/streamlit-arborist/releases/new)
   with a new `X.Y.Z` tag on `main`, using the version as the title.
   Write the notes in Markdown as a **Full Changelog** link comparing with the previous version,
   followed by a `## Changes` section with the version's entries from `docs/releases.rst`.
