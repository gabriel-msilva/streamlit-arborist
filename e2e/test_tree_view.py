import json
import re
from pathlib import Path
from typing import Union

import pytest
from e2e_utils import StreamlitRunner
from playwright.sync_api import Page, expect

ROOT_DIRECTORY = Path(__file__).parents[1].absolute()
EXAMPLE_FILE = ROOT_DIRECTORY / "app" / "example.py"

COMPONENT_FRAME_SELECTOR = 'iframe[title="streamlit_arborist\\.streamlit_arborist"]'
COLORS = {
    "background": "rgba(0, 0, 0, 0)",
    "hover": "rgba(151, 166, 195, 0.15)",
    "selected": "rgba(151, 166, 195, 0.25)",
}

NODE_STATES = {
    "isOpen": re.compile(r"\bisOpen\b"),
    "isClosed": re.compile(r"\bisClosed\b"),
}


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(EXAMPLE_FILE) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)

    # Wait for app to load
    page.get_by_role("img", name="Running...").is_hidden()


def assert_component_value_equals(expected: Union[str, None], page: Page):
    # Streamlit renders Markdown code blocks as <pre><code> elements
    json_block = page.locator("pre code").nth(1)

    page.wait_for_timeout(500)

    if expected is None:
        assert json_block.text_content() == "None"
    else:
        assert json.loads(json_block.text_content()) == expected


def test_should_return_default_value(page: Page):
    assert_component_value_equals(None, page)


@pytest.mark.parametrize(
    "level, index, expected",
    [(1, 0, {"id": "1", "name": "Unread"}), (2, 1, {"id": "c2", "name": "Random"})],
)
def test_should_return_selected_value(
    page: Page, level: int, index: int, expected: dict
):
    frame = page.frame_locator(COMPONENT_FRAME_SELECTOR)

    node = frame.get_by_role("treeitem", level=level).nth(index)
    node.click()

    assert_component_value_equals(expected, page)


def test_should_toggle_internal_node_on_click(page: Page):
    frame = page.frame_locator(COMPONENT_FRAME_SELECTOR)

    internal_node = frame.get_by_role("treeitem", level=1).nth(2)
    inner_div = internal_node.locator("div")

    expect(inner_div).to_have_class(NODE_STATES["isOpen"])

    internal_node.click()

    expect(inner_div).to_have_class(NODE_STATES["isClosed"])
    assert_component_value_equals(None, page)


def test_should_select_node_on_click(page: Page):
    frame = page.frame_locator(COMPONENT_FRAME_SELECTOR)

    general = frame.get_by_role("treeitem", level=2).nth(0)
    inner_div = general.locator("div")

    expect(general).to_have_attribute("aria-selected", "false")
    expect(inner_div).to_have_css("background-color", COLORS["background"])

    general.click()

    expect(general).to_have_attribute("aria-selected", "true")
    expect(inner_div).to_have_css("background-color", COLORS["selected"])


def test_should_select_internal_node_on_label_and_toggle_on_icon(page: Page):
    frame = page.frame_locator(COMPONENT_FRAME_SELECTOR)

    checkbox = page.locator("label:has-text('Select internal nodes')")
    checkbox.click()

    expect(checkbox).to_be_checked()

    chat_rooms = frame.get_by_role("treeitem", level=1).nth(2)
    icon = chat_rooms.locator("span").nth(0)
    label = chat_rooms.locator("span", has_text="Chat Rooms")

    expect(chat_rooms).to_have_attribute("aria-selected", "false")
    expect(chat_rooms.locator("div")).to_have_class(NODE_STATES["isOpen"])

    icon.click()

    # Clicking the icon toggles open/closed but does not select the node
    expect(chat_rooms).to_have_attribute("aria-selected", "false")
    expect(chat_rooms.locator("div")).to_have_class(NODE_STATES["isClosed"])
    assert_component_value_equals(None, page)

    label.click()

    # Clicking the label selects the node but does not toggle open/closed
    expect(chat_rooms).to_have_attribute("aria-selected", "true")
    expect(chat_rooms.locator("div")).to_have_class(NODE_STATES["isClosed"])
    assert_component_value_equals(
        {
            "id": "3",
            "name": "Chat Rooms",
            "children": [
                {"id": "c1", "name": "General"},
                {"id": "c2", "name": "Random"},
                {"id": "c3", "name": "Open Source Projects"},
            ],
        },
        page,
    )


def test_should_select_and_toggle_internal_node_on_double_click(page: Page):
    frame = page.frame_locator(COMPONENT_FRAME_SELECTOR)

    checkbox = page.locator("label:has-text('Select internal nodes')")
    checkbox.click()

    expect(checkbox).to_be_checked()

    direct_messages = frame.get_by_role("treeitem", level=1).nth(3)

    expect(direct_messages).to_have_attribute("aria-selected", "false")
    expect(direct_messages.locator("div")).to_have_class(NODE_STATES["isOpen"])

    label = direct_messages.locator("span", has_text="Direct Messages")

    label.dblclick()

    # Double-clicking the label selects and toggles the node
    expect(direct_messages).to_have_attribute("aria-selected", "true")
    expect(direct_messages.locator("div")).to_have_class(NODE_STATES["isClosed"])
    assert_component_value_equals(
        {
            "id": "4",
            "name": "Direct Messages",
            "children": [
                {"id": "d1", "name": "Alice"},
                {"id": "d2", "name": "Bob"},
                {"id": "d3", "name": "Charlie"},
            ],
        },
        page,
    )


def test_should_hover_node(page: Page):
    frame = page.frame_locator(COMPONENT_FRAME_SELECTOR)

    unread = frame.get_by_role("treeitem", level=1)
    inner_div = unread.nth(0).locator("div")

    expect(inner_div).to_have_css("background-color", COLORS["background"])

    inner_div.hover()

    expect(inner_div).to_have_css("background-color", COLORS["hover"])

    page.mouse.move(0, 0)

    expect(inner_div).to_have_css("background-color", COLORS["background"])


def test_should_nodes_be_closed(page: Page):
    frame = page.frame_locator(COMPONENT_FRAME_SELECTOR)
    tree_items = frame.get_by_role("treeitem", level=1)

    chat_rooms = tree_items.nth(2).locator("div")
    direct_messages = tree_items.nth(3).locator("div")

    expect(chat_rooms).to_have_class(NODE_STATES["isOpen"])
    expect(direct_messages).to_have_class(NODE_STATES["isOpen"])

    checkbox = page.locator("label:has-text('Open by default')")

    expect(checkbox).to_be_checked()
    checkbox.click()
    expect(checkbox).not_to_be_checked()

    expect(chat_rooms).to_have_class(NODE_STATES["isClosed"])
    expect(direct_messages).to_have_class(NODE_STATES["isClosed"])


def test_should_search_nodes(page: Page):
    frame = page.frame_locator(COMPONENT_FRAME_SELECTOR)
    search_term = page.get_by_label("Search term")

    search_term.fill("general")
    search_term.press("Enter")

    page.wait_for_timeout(500)

    expect(frame.get_by_role("treeitem", level=1)).to_have_text("📂Chat Rooms")
    expect(frame.get_by_role("treeitem", level=2)).to_have_text("📄General")

    search_term.fill("read")
    search_term.press("Enter")

    page.wait_for_timeout(500)

    tree_items = frame.get_by_role("treeitem", level=1)

    expect(tree_items).to_have_count(2)
    expect(tree_items.nth(0)).to_have_text("📄Unread")
    expect(tree_items.nth(1)).to_have_text("📄Threads")


def test_should_change_emoji_icons(page: Page):
    frame = page.frame_locator(COMPONENT_FRAME_SELECTOR)
    level_1 = frame.get_by_role("treeitem", level=1)

    leaf_icon = level_1.nth(0).locator("span")
    expect(leaf_icon).to_have_text("📄")

    open_icon = level_1.nth(2).locator("span")
    expect(open_icon).to_have_text("📂")

    closed_icon = level_1.nth(3).locator("span")
    closed_icon.click()
    expect(closed_icon).to_have_text("📁")

    leaf_input = page.get_by_label("Leaf", exact=True)
    leaf_input.fill("🍀")
    leaf_input.press("Enter")

    page.wait_for_timeout(500)

    expect(leaf_icon).to_have_text("🍀")

    open_input = page.get_by_label("Open", exact=True)
    open_input.fill("🔓")
    open_input.press("Enter")

    page.wait_for_timeout(500)

    expect(open_icon).to_have_text("🔓")

    closed_input = page.get_by_label("Closed", exact=True)
    closed_input.fill("🔒")
    closed_input.press("Enter")

    page.wait_for_timeout(500)

    closed_icon.click()
    expect(closed_icon).to_have_text("🔒")


def test_should_use_material_symbols_icon(page: Page):
    frame = page.frame_locator(COMPONENT_FRAME_SELECTOR)
    level_1 = frame.get_by_role("treeitem", level=1)

    leaf_input = page.get_by_label("Leaf", exact=True)
    leaf_input.fill(":material/docs:")
    leaf_input.press("Enter")

    page.wait_for_timeout(500)

    leaf_icon = level_1.nth(0).locator("span")
    expect(leaf_icon).to_have_class(re.compile(r"material-symbols-rounded"))
    expect(leaf_icon).to_have_text("docs")


def test_should_not_have_icon(page: Page):
    frame = page.frame_locator(COMPONENT_FRAME_SELECTOR)
    level_1 = frame.get_by_role("treeitem", level=1)

    leaf_input = page.get_by_label("Leaf", exact=True)
    leaf_input.fill("")
    leaf_input.press("Enter")

    page.wait_for_timeout(500)

    leaf_icon = level_1.nth(0).locator("span")
    expect(leaf_icon).to_have_text("")


def test_should_select_node_by_id(page: Page):
    frame = page.frame_locator(COMPONENT_FRAME_SELECTOR)

    unread = frame.get_by_role("treeitem", level=1, name="Unread")
    inner_div = unread.locator("div")

    expect(unread).to_have_attribute("aria-selected", "false")
    expect(inner_div).to_have_css("background-color", COLORS["background"])

    selectbox = page.get_by_role("combobox", name="Selection")
    selectbox.click()

    page.get_by_role("option").get_by_text("1", exact=True).click()

    expect(unread).to_have_attribute("aria-selected", "true")
    expect(inner_div).to_have_css("background-color", COLORS["selected"])
