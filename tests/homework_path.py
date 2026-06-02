import pytest
from selenium import webdriver
import time
from selenium.webdriver.common.by import By


"""
Написать автотест который будет отображение информации по карточке 
(открыть страницу, загрузить карточки, проверить что карточки видны xpath и css)
"""


class TestTask_1:
    @pytest.fixture
    def driver(self) -> webdriver.Chrome:
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("http://localhost:3000/automation-lab/cards")
        yield driver
        print("\nClosing driver!\n")
        driver.quit()
        

    Locators = {
        'xpath': {
            'bnt_dnld_cards': (By.XPATH, "//button[@class = 'trigger-btn']"),
            'lst_of_cards': (By.XPATH, "//div[starts-with(@class, 'card card-')]")
            },    
        'css': {
            'bnt_dnld_cards': (By.XPATH, "//button[@class = 'trigger-btn']"),
            'lst_of_cards': (By.XPATH, "//div[starts-with(@class, 'card card-')]")
            }    
    }

    @pytest.mark.parametrize("locator_lang", ['xpath', 'css'])
    def test_cards_exist_CSS(self, driver:webdriver.Chrome, locator_lang):
        by, btn_locator = self.Locators[locator_lang]['bnt_dnld_cards']
        by, cards_locator = self.Locators[locator_lang]['lst_of_cards']

        button = driver.find_element(by, btn_locator)
        button.click()

        time.sleep(5)
        cards = driver.find_elements(by, cards_locator)

        print(f"\nNumber of cards = {len(cards)}\n")
        assert len(cards) > 0
