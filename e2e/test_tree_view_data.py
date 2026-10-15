from pathlib import Path

import pytest
from conftest import COMPONENT_FRAME_SELECTOR, NODE_STATES
from e2e_utils import StreamlitRunner
from playwright.sync_api import FrameLocator, Page, expect

DATA_APP_FILE = Path(__file__).with_name("tree_view_data_app.py")


@pytest.fixture(scope="module")
def tree_view_data_app():
    with StreamlitRunner(DATA_APP_FILE) as runner:
        yield runner


@pytest.fixture(autouse=True)
def go_to_app(page: Page, tree_view_data_app: StreamlitRunner):
    """Override the conftest fixture to open the data-change app instead of the demo."""
    page.goto(tree_view_data_app.server_url)
    expect(component_frame(page).get_by_role("tree")).to_be_visible()


def component_frame(page: Page) -> FrameLocator:
    return page.frame_locator(COMPONENT_FRAME_SELECTOR)


def test_changed_data_rerenders_tree(page: Page):
    frame = component_frame(page)

    page.get_by_text("Replace data").click()

    expect(frame.get_by_text("Updated data")).to_be_visible()
    expect(frame.get_by_text("New child")).to_be_visible()


def test_changed_data_keeps_open_state(page: Page):
    frame = component_frame(page)
    parent = frame.get_by_role("treeitem", level=1).first
    inner_div = parent.locator("div")

    parent.click()

    expect(inner_div).to_have_class(NODE_STATES["isClosed"])

    page.get_by_text("Replace data").click()

    expect(frame.get_by_text("Updated data")).to_be_visible()
    expect(inner_div).to_have_class(NODE_STATES["isClosed"])
    expect(frame.get_by_text("New child")).to_have_count(0)
