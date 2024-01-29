from modules.ui.page_objects.main_page import MainPage
import pytest


@pytest.mark.ui
def test_product_search():
    main_page = MainPage()
    main_page.open()
    main_page.enter_product_name("atomic habits")
    assert main_page.get_search_section_title_text() == "atomic habits"


@pytest.mark.ui
def test_search_nonexist_product():
    main_page = MainPage()
    main_page.open()
    main_page.enter_product_name("jfsjdgsg")
    assert main_page.get_message_text().startswith(
        "No results for"
    ), "Expected message to start with 'No results for'"
