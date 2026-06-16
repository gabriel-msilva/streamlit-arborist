import json
import re
from pathlib import Path
from typing import Union

import pytest
from e2e_utils import StreamlitRunner
from playwright.sync_api import FrameLocator, Locator, Page, expect

ROOT_DIRECTORY = Path(__file__).parents[1].absolute()
EXAMPLE_FILE = ROOT_DIRECTORY / "app" / "example.py"

COMPONENT_FRAME_SELECTOR = 'iframe[title="streamlit_arborist\\.streamlit_arborist"]'

NODE_STATES = {
    "isOpen": re.compile(r"\bisOpen\b"),
    "isClosed": re.compile(r"\bisClosed\b"),
}


@pytest.fixture(autouse=True, scope="session")
def streamlit_app():
    with StreamlitRunner(EXAMPLE_FILE) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)

    # Wait for app to load
    page.get_by_role("img", name="Running...").is_hidden()


def tree_view_frame(page: Page) -> FrameLocator:
    """The first streamlit-arborist iframe on the page (the tree_view widget)."""
    return page.frame_locator(COMPONENT_FRAME_SELECTOR).first


def tree_checkbox_frame(page: Page) -> FrameLocator:
    """The second streamlit-arborist iframe on the page (the tree_checkbox widget)."""
    return page.frame_locator(COMPONENT_FRAME_SELECTOR).nth(1)


def tree_checkbox_input(page: Page, node_id: str) -> Locator:
    """Locate the underlying <input type=checkbox> for a tree_checkbox node by id."""
    return tree_checkbox_frame(page).locator(f'input[data-node-id="{node_id}"]')


def checkbox_chevron(page: Page, node_id: str) -> Locator:
    """Locate the chevron span for an internal tree_checkbox node by id."""
    return tree_checkbox_frame(page).locator(f'[data-chevron-id="{node_id}"]')


def toggle_checked(page: Page, node_id: str):
    """Toggle a node id in the sidebar's "Checked" st.multiselect."""
    multiselect = page.get_by_label("Checked")
    multiselect.click()
    page.get_by_role("option", name=node_id, exact=True).click()
    page.keyboard.press("Escape")


def assert_tree_view_value_equals(expected: Union[dict, None], page: Page):
    """Read the JSON code block following 'Returned value (tree_view):' in the demo."""
    json_block = page.locator("pre code").nth(1)
    expected_text = "None" if expected is None else json.dumps(expected, indent=2)
    expect(json_block).to_have_text(expected_text)


def assert_checkbox_value_equals(expected: list, page: Page):
    """Read the JSON code block following 'Returned value (tree_checkbox):' in the demo."""
    json_block = page.locator("pre code").nth(3)
    expect(json_block).to_have_text(json.dumps(expected, indent=2))
