from modules.ui.page_objects.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class MainPage(BasePage):
    URL = "https://www.amazon.com/"

    def __init__(self) -> None:
        super().__init__()
        self.start_here_btn = (
            By.CSS_SELECTOR,
            "div[class='nav-signin-tooltip-footer'] a[class='nav-a']",
        )
        self.search_field = (By.ID, "twotabsearchtextbox")
        self.search_btn = (By.ID, "nav-search-submit-button")
        self.search_section_title_result = (
            By.CSS_SELECTOR,
            ".a-color-state.a-text-bold",
        )
        self.message = (By.CSS_SELECTOR, "div[class='a-row']")
        self.deliver_btn = (By.ID, "nav-global-location-popover-link")
        self.modal = (By.CLASS_NAME, "a-popover-wrapper")
        self.zip_code_field = (By.ID, "GLUXZipUpdateInput")
        self.apply_btn = (
            By.CSS_SELECTOR,
            "input[aria-labelledby='GLUXZipUpdate-announce']",
        )
        self.location_result = (
            By.ID,
            "GLUXHiddenSuccessSelectedAddressPlaceholder",
        )
        self.success_message_text = (By.ID, "GLUXHiddenSuccessSubTextAisEgress")
        self.error_message = (By.CSS_SELECTOR, "a-alert-inline-error div")
        self.continue_btn = (By.XPATH, "(//input[@id='GLUXConfirmClose'])[2]")
        self.deliver_location = (By.ID, "glow-ingress-line2")

    def open(self):
        self.driver.get(MainPage.URL)

    def click_start_here_btn(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.start_here_btn)
        ).click()

    def enter_product_name(self, product_name: str):
        self.driver.find_element(*self.search_field).click()
        self.driver.find_element(*self.search_field).send_keys(product_name)
        self.driver.find_element(*self.search_btn).click()

    def get_message_text(self):
        return self.driver.find_element(*self.message).text

    # 15
    def get_search_section_title_text(self):
        search_section_title_result = (
            WebDriverWait(self.driver, 10)
            .until(EC.visibility_of_element_located(self.search_section_title_result))
            .text
        )
        return search_section_title_result.strip('""')

    # 30
    def click_deliver_to_btn(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.deliver_btn)
        ).click()

    # 30
    def enter_zip_code_and_confirm(self, zip):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.modal)
        )
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.zip_code_field)
        ).click()
        self.driver.find_element(*self.zip_code_field).send_keys(zip)
        self.driver.find_element(*self.apply_btn).click()

    def get_zip_code_text(self):
        return self.driver.find_element(*self.location_result).get_attribute(
            "textContent"
        )

    def get_success_message_text(self):
        return self.driver.find_element(*self.success_message_text).get_attribute(
            "textContent"
        )

    def get_error_message_text(self):
        return self.driver.find_element(*self.error_message).text

    # 30
    def confirm_location(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.continue_btn)
        ).click()

    def get_deliver_to_location(self):
        time.sleep(5)
        result = self.driver.find_element(*self.deliver_location).get_attribute(
            "textContent"
        )
        return result.rstrip().split()[-1][0:5]


# pytest -s -m ui
