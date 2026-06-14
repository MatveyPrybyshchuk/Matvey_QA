import allure
from playwright.sync_api import Page


def make_screenshot(page: Page, screenshot_name):
    image = page.screenshot()
    allure.attach(
        image, f"{screenshot_name}", attachment_type=allure.attachment_type.PNG
    )
