import re
from pathlib import Path

import pytest
from e2e_utils import StreamlitRunner
from playwright.sync_api import Page

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
