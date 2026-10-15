from pathlib import Path

import pytest
from conftest import COMPONENT_FRAME_SELECTOR, wait_for_render
from e2e_utils import StreamlitRunner
from playwright.sync_api import FrameLocator, Locator, Page, expect

WIDE_APP_FILE = Path(__file__).with_name("wide_checkbox_app.py")


@pytest.fixture(scope="module")
def wide_checkbox_app():
    with StreamlitRunner(WIDE_APP_FILE) as runner:
        yield runner


@pytest.fixture(autouse=True)
def go_to_app(page: Page, wide_checkbox_app: StreamlitRunner):
    """Override the conftest fixture to open the wide-layout app instead of the demo."""
    page.goto(wide_checkbox_app.server_url)
    expect(component_frame(page).get_by_role("tree")).to_be_visible()


def component_frame(page: Page) -> FrameLocator:
    return page.frame_locator(COMPONENT_FRAME_SELECTOR)


def child_checkbox(page: Page) -> Locator:
    return component_frame(page).locator('input[data-node-id="child"]')


def assert_value_equals(expected: str, page: Page):
    expect(page.locator("pre code")).to_have_text(expected)


def test_checked_state_survives_sidebar_toggle(page: Page):
    child = child_checkbox(page)
    child.check()

    expect(child).to_be_checked()
    assert_value_equals("['child', 'data']", page)

    # In wide layout, toggling the sidebar resizes the iframe and Streamlit
    # resends the component args.
    sidebar = page.get_by_test_id("stSidebar")
    with wait_for_render(component_frame(page)):
        sidebar.hover()
        page.get_by_test_id("stSidebarCollapseButton").get_by_role("button").click()

    expect(sidebar).to_have_attribute("aria-expanded", "false")
    expect(child).to_be_checked()
    assert_value_equals("['child', 'data']", page)

    with wait_for_render(component_frame(page)):
        page.get_by_test_id("stExpandSidebarButton").click()

    expect(sidebar).to_have_attribute("aria-expanded", "true")
    expect(child).to_be_checked()
    assert_value_equals("['child', 'data']", page)


def test_checked_state_survives_rerun(page: Page):
    child = child_checkbox(page)
    child.check()

    assert_value_equals("['child', 'data']", page)

    page.get_by_role("slider", name="Test").press("ArrowRight")

    expect(page.get_by_text("Test value: 1", exact=True)).to_be_visible()
    expect(child).to_be_checked()
    assert_value_equals("['child', 'data']", page)


def test_changed_data_reseeds_checked_state(page: Page):
    child = child_checkbox(page)
    child.check()

    assert_value_equals("['child', 'data']", page)

    page.get_by_text("Replace data").click()

    expect(child).not_to_be_checked()
    assert_value_equals("[]", page)


def test_changed_data_rerenders_tree(page: Page):
    frame = component_frame(page)
    new_child = frame.locator('input[data-node-id="new"]')

    expect(new_child).to_have_count(0)

    page.get_by_text("Replace data").click()

    expect(frame.get_by_text("Updated data")).to_be_visible()
    expect(new_child).to_be_visible()

    new_child.check()

    assert_value_equals("['new']", page)
