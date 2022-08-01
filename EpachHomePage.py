from selenium.webdriver.common.by import By


class EpackHomePage:
    def __init__(self, driver):
        self.driver = driver

    search_epack = (By.XPATH, '//input[@placeholder = "Enter Epack Number"]')
    search_button = (By.XPATH, '//button[@id = "btnSearch"]')

    test_instructions = (By.XPATH, '//p[contains(text(), "Please have testing completed by")]')

    def search_epack_input(self):
        return self.driver.find_element(*EpackHomePage.search_epack)

    def search_button_field(self):
        return self.driver.find_element(*EpackHomePage.search_button)

    def test_instructions_paragraph(self):
        return self.driver.find_element(*EpackHomePage.test_instructions)

