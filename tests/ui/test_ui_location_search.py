from modules.ui.page_objects.main_page import MainPage
import pytest


@pytest.mark.ui
def test_choose_location_with_valid_zip():
    main_page = MainPage()
    main_page.open()
    main_page.click_deliver_to_btn()
    main_page.enter_zip_code_and_confirm("42223")
    assert (
        main_page.get_zip_code_text() == "42223"
    ), "Expected location_zip_code to be '42223'"
    assert main_page.get_success_message_text() == (
        "We will use your selected location to show all products available for the United States. Additional language and currency settings may not be available."
    )
    main_page.confirm_location()
    assert main_page.get_deliver_to_location() == "42223"


@pytest.mark.ui
def test_setting_location_with_invalid_zip():
    main_page = MainPage()
    main_page.open()
    main_page.click_deliver_to_btn()
    main_page.enter_zip_code_and_confirm("00000")
    assert main_page.get_error_message_text() == "Please enter a valid US zip code"
