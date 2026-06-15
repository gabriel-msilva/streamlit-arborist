import json

from conftest import COMPONENT_FRAME_SELECTOR, NODE_STATES
from playwright.sync_api import Page, expect


def assert_checkbox_value_equals(expected: list, page: Page):
    # <pre><code> blocks on the page, in order:
    #   nth(0) tree_view source-code example
    #   nth(1) tree_view return value
    #   nth(2) tree_checkbox source-code example
    #   nth(3) tree_checkbox return value  <-- target
    json_block = page.locator("pre code").nth(3)
    page.wait_for_timeout(500)

    content = json_block.text_content()
    assert content and json.loads(content) == expected


def assert_tree_view_value_equals(expected, page: Page):
    json_block = page.locator("pre code").nth(1)
    page.wait_for_timeout(500)

    content = json_block.text_content()
    if expected is None:
        assert content == "None"
    else:
        assert content and json.loads(content) == expected


def tree_checkbox_frame(page: Page):
    return page.frame_locator(COMPONENT_FRAME_SELECTOR).nth(1)


def tree_checkbox_input(page: Page, node_id: str):
    return tree_checkbox_frame(page).locator(f'input[data-node-id="{node_id}"]')


def checkbox_chevron(page: Page, node_id: str):
    return tree_checkbox_frame(page).locator(f'[data-chevron-id="{node_id}"]')


def test_should_return_default_value(page: Page):
    assert_checkbox_value_equals([], page)


def seed_checked(page: Page, node_id: str):
    multiselect = page.get_by_label("Checked")

    multiselect.click()

    page.get_by_role("option", name=node_id, exact=True).click()
    page.keyboard.press("Escape")

    page.wait_for_timeout(500)


def test_that_seed_leaf_returns_only_that_leaf(page: Page):
    seed_checked(page, "c1")

    assert_checkbox_value_equals(["c1"], page)
    expect(tree_checkbox_input(page, "c1")).to_be_checked()


def test_that_seed_parent_cascades_to_subtree(page: Page):
    seed_checked(page, "3")

    assert_checkbox_value_equals(["3", "c1", "c2", "c3"], page)
    for node_id in ("3", "c1", "c2", "c3"):
        expect(tree_checkbox_input(page, node_id)).to_be_checked()


def test_that_check_parent_cascades_down(page: Page):
    parent_checkbox = tree_checkbox_input(page, "3")

    expect(parent_checkbox).not_to_be_checked()

    parent_checkbox.click()

    expected = ["3", "c1", "c2", "c3"]
    for node_id in expected:
        expect(tree_checkbox_input(page, node_id)).to_be_checked()

    assert_checkbox_value_equals(expected, page)


def test_that_uncheck_leaf_makes_parent_indeterminate(page: Page):
    parent_checkbox = tree_checkbox_input(page, "3")
    parent_checkbox.click()  # check the parent; cascades down

    for node_id in ("3", "c1", "c2", "c3"):
        expect(tree_checkbox_input(page, node_id)).to_be_checked()

    # Uncheck one leaf
    tree_checkbox_input(page, "c1").click()

    expect(tree_checkbox_input(page, "3")).not_to_be_checked()
    expect(tree_checkbox_input(page, "3")).to_have_js_property("indeterminate", True)

    expect(tree_checkbox_input(page, "c1")).not_to_be_checked()

    expect(tree_checkbox_input(page, "c2")).to_be_checked()
    expect(tree_checkbox_input(page, "c3")).to_be_checked()

    assert_checkbox_value_equals(["c2", "c3"], page)


def test_that_uncheck_all_leaves_makes_parent_unchecked(page: Page):
    tree_checkbox_input(page, "3").click()  # cascade-down

    for leaf in ("c1", "c2", "c3"):
        tree_checkbox_input(page, leaf).click()

    parent_checkbox = tree_checkbox_input(page, "3")

    expect(parent_checkbox).not_to_be_checked()
    expect(parent_checkbox).to_have_js_property("indeterminate", False)
    assert_checkbox_value_equals([], page)


def test_that_leaf_row_click_toggles_check(page: Page):
    # Click anywhere on a leaf row toggles its check.
    leaf_row = tree_checkbox_frame(page).get_by_role("treeitem", name="Unread")
    leaf_checkbox = tree_checkbox_input(page, "1")

    expect(leaf_checkbox).not_to_be_checked()

    leaf_row.click()

    expect(leaf_checkbox).to_be_checked()
    assert_checkbox_value_equals(["1"], page)

    leaf_row.click()

    expect(leaf_checkbox).not_to_be_checked()
    assert_checkbox_value_equals([], page)


def test_that_internal_row_click_toggles_check_with_cascade(page: Page):
    internal_row = tree_checkbox_frame(page).get_by_role("treeitem", name="Chat Rooms")
    inner_div = internal_row.locator("div").first

    expect(tree_checkbox_input(page, "3")).not_to_be_checked()
    # Open state unchanged because the chevron is the only open/close affordance.
    expect(inner_div).to_have_class(NODE_STATES["isOpen"])

    internal_row.click()

    for node_id in ("3", "c1", "c2", "c3"):
        expect(tree_checkbox_input(page, node_id)).to_be_checked()
    expect(inner_div).to_have_class(NODE_STATES["isOpen"])
    assert_checkbox_value_equals(["3", "c1", "c2", "c3"], page)


def test_that_space_key_toggles_focused_row(page: Page):
    # Keyboard accessibility: clicking a row both checks AND focuses it; Space
    # then toggles the focused row's check.
    leaf_row = tree_checkbox_frame(page).get_by_role("treeitem", name="Unread")
    leaf_checkbox = tree_checkbox_input(page, "1")

    leaf_row.click()

    expect(leaf_checkbox).to_be_checked()
    expect(leaf_row).to_have_attribute("aria-selected", "true")

    tree_checkbox_frame(page).get_by_role("tree").press(" ")

    expect(leaf_checkbox).not_to_be_checked()
    assert_checkbox_value_equals([], page)


def test_that_internal_row_double_click_checks_and_toggles_open(page: Page):
    internal_row = tree_checkbox_frame(page).get_by_role(
        "treeitem", name="Direct Messages"
    )
    inner_div = internal_row.locator("div").first

    expect(tree_checkbox_input(page, "4")).not_to_be_checked()
    expect(inner_div).to_have_class(NODE_STATES["isOpen"])

    internal_row.dblclick()

    expect(tree_checkbox_input(page, "4")).to_be_checked()
    expect(inner_div).to_have_class(NODE_STATES["isClosed"])

    # Children are no longer in the DOM (collapsed), so assert via the
    # Python-side return value instead of locating their checkboxes.
    assert_checkbox_value_equals(["4", "d1", "d2", "d3"], page)


def test_that_leaf_row_double_click_only_toggles_check(page: Page):
    # Leaves have no open/close to toggle, so dblclick is equivalent to a
    # single click: the check ends up toggled once, not zero times.
    leaf_row = tree_checkbox_frame(page).get_by_role("treeitem", name="Threads")
    leaf_checkbox = tree_checkbox_input(page, "2")

    expect(leaf_checkbox).not_to_be_checked()

    leaf_row.dblclick()

    expect(leaf_checkbox).to_be_checked()
    assert_checkbox_value_equals(["2"], page)


def test_that_chevron_click_only_toggles_open(page: Page):
    chevron = checkbox_chevron(page, "3")
    internal_row = tree_checkbox_frame(page).get_by_role("treeitem", name="Chat Rooms")
    inner_div = internal_row.locator("div").first

    expect(inner_div).to_have_class(NODE_STATES["isOpen"])
    expect(chevron).to_have_attribute("data-open", "true")

    chevron.click()

    expect(inner_div).to_have_class(NODE_STATES["isClosed"])
    expect(chevron).to_have_attribute("data-open", "false")
    expect(tree_checkbox_input(page, "3")).not_to_be_checked()
    assert_checkbox_value_equals([], page)

    chevron.click()

    expect(inner_div).to_have_class(NODE_STATES["isOpen"])
    expect(chevron).to_have_attribute("data-open", "true")


def test_that_components_are_independent(page: Page):
    assert_tree_view_value_equals(None, page)
    assert_checkbox_value_equals([], page)

    tree_checkbox_input(page, "c2").click()

    assert_tree_view_value_equals(None, page)
    assert_checkbox_value_equals(["c2"], page)
