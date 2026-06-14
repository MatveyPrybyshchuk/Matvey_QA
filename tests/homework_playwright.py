from contextlib import contextmanager
import allure
from playwright.sync_api import Page, expect
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.funcore import make_screenshot


"""
1 написать автотесты на форму /automation-lab/subscription
- открытие формы - проверить что страница и главные элементы отображаются 
- проверка ввода валидного промокода Always и BASIC199
- проверка ввода NE валидного промокода (через параметризацию) BASIC199, WELCOME10
- проверка формы Тестовые карты для оплаты (5 кейсов - приоритет и критичность) 
"""

@contextmanager
def allure_step_with_screenshoot_on_failure(page: Page, step_name: str):
    "Allure step, который при ошибке сделает скриншот"
    try:
        with allure.step(step_name):
            yield
    except Exception as err:
        make_screenshot(page, step_name)
        raise err


@allure.title("Открытие формы")
@allure.description("Проверить что страница и главные элементы отображаются")
@allure.severity(allure.severity_level.MINOR)
@allure.feature("StreamVibe homepage")
@pytest.mark.play
def test_streamVibe_homepage(page: Page):
    page.goto("http://localhost:3000/automation-lab/subscription")
    page.set_viewport_size({"width": 1920, "height": 1080})
    
    logo = page.locator('.flex-shrink-0')
    bnt_back = page.locator('.back-btn')

    with allure_step_with_screenshoot_on_failure(page, "Gettin locators"):
        subscription_title = page.locator('.subscription-title')
        subscription_subtitle = page.locator('.subscription-subtitle')
        btn_help = page.locator('.promo-hint-btn')
        btn_goals = page.locator('.task-goals-btn')

        section_period = page.locator('.period-section')
        section_tariffs = page.locator('.tariffs-section')
        section_promo = page.locator('.promo-section')
        section_payment = page.locator('.payment-section')
        section_summary = page.locator('.summary-section')

    with allure_step_with_screenshoot_on_failure(page, "Checking elements to be visible"):
        expect(logo).to_be_visible()
        expect(bnt_back).to_be_visible()

        expect(subscription_title).to_be_visible()
        expect(subscription_subtitle).to_be_visible()
        expect(btn_help).to_be_visible()
        expect(btn_goals).to_be_visible()

        expect(section_period).to_be_visible()
        expect(section_tariffs).to_be_visible()
        expect(section_promo).to_be_visible()
        expect(section_payment).to_be_visible()
        expect(section_summary).to_be_visible()


@allure.title("Проверка валидного промокода")
@allure.description("проверка ввода валидного промокода Always и BASIC199")
@allure.severity(allure.severity_level.MINOR)
@allure.feature("Promocode")
@pytest.mark.parametrize("valid_promo", ['Always', 'BASIC199'])
@pytest.mark.play
def test_enter_valid_promocode(page: Page, valid_promo):
    page.goto("http://localhost:3000/automation-lab/subscription")

    with allure_step_with_screenshoot_on_failure(page, "Gettin locators"):
        inputfield_promocode = page.locator('.promo-input')
        btn_accept = page.locator('.promo-apply-btn')
        promo_error = page.locator('.promo-message.error')
        promo_success = page.locator('.promo-message.success')

    with allure_step_with_screenshoot_on_failure(page, "Checking that textfields are hidden"):
        expect(promo_error).to_be_hidden()
        expect(promo_success).to_be_hidden()

    with allure_step_with_screenshoot_on_failure(page, "Entering promocode"):
        inputfield_promocode.fill(valid_promo)
        btn_accept.click()

    with allure_step_with_screenshoot_on_failure(page, "Checking expected textfield"):
        expect(promo_success).to_be_visible()
        expect(promo_success).to_have_text("Промокод применён: Скидка 15% для для всех тарифов")


@allure.title("Проверка НЕ валидного промокода")
@allure.description("проверка ввода NE валидного промокода (через параметризацию) BASIC199, WELCOME10")
@allure.severity(allure.severity_level.MINOR)
@allure.feature("Promocode")
@pytest.mark.parametrize("invalid_promo", ['BASIC199', 'WELCOME10'])
@pytest.mark.play
def test_enter_invalid_promocode(page: Page, invalid_promo):
    page.goto("http://localhost:3000/automation-lab/subscription")

    with allure_step_with_screenshoot_on_failure(page, "Gettin locators"):
        inputfield_promocode = page.locator('.promo-input')
        btn_accept = page.locator('.promo-apply-btn')
        promo_error = page.locator('.promo-message.error')
        promo_success = page.locator('.promo-message.success')

    with allure_step_with_screenshoot_on_failure(page, "Checking that textfields are hidden"):
        expect(promo_error).to_be_hidden()
        expect(promo_success).to_be_hidden()

    with allure_step_with_screenshoot_on_failure(page, "Entering promocode"):
        inputfield_promocode.fill(invalid_promo)
        btn_accept.click()

    with allure_step_with_screenshoot_on_failure(page, "Checking expected textfield"):
        expect(promo_error).to_be_visible()
        if invalid_promo in 'BASIC199':
            expect(promo_error).to_have_text("Промокод только для: Базовый")
        else:
            expect(promo_error).to_have_text("Промокод истек 31.12.2024")


@allure.title("Проверка карт")
@allure.description("Оплата валидной платежной картой")
@allure.severity(allure.severity_level.MINOR)
@allure.feature("Credit_card")
@allure.testcase("TC_1")
@pytest.mark.play
def test_card_success_pay(page: Page):
    page.goto("http://localhost:3000/automation-lab/subscription")

    inputfield_cardnum = page.locator('#card-number-input')
    inputfield_carddate = page.locator('#card-expiry-input')
    inputfield_cardCVV = page.locator('#card-cvv-input')
    bnt_subscribe = page.locator('.pay-button')

    popup_success_pay= page.locator('.modal-content.success-modal')
    popup_success_details = page.locator('.success-details')
    popup_success_btn_Great = page.locator('.modal-close-btn')

    with allure_step_with_screenshoot_on_failure(page, "check default fields"):
        expect(inputfield_cardnum).to_be_empty()
        expect(inputfield_carddate).to_be_empty()
        expect(inputfield_cardCVV).to_be_empty()
        expect(bnt_subscribe).to_be_disabled()

    with allure_step_with_screenshoot_on_failure(page, "Insert valid card"):
        inputfield_cardnum.fill("4111 1111 1111 1111")
        inputfield_carddate.fill("1130")
        inputfield_cardCVV.fill("222")
        bnt_subscribe.click()

    with allure_step_with_screenshoot_on_failure(page, "Check pop appeared"):
        expect(popup_success_pay).to_be_visible()
        expect(popup_success_details).to_be_visible()
        expect(popup_success_btn_Great).to_be_visible()
    

@allure.title("Проверка карт")
@allure.description("Использование карты с истекшим сроком")
@allure.severity(allure.severity_level.MINOR)
@allure.feature("Credit_card")
@allure.testcase("TC_2")
@pytest.mark.play
def test_card_old_date(page: Page):
    page.goto("http://localhost:3000/automation-lab/subscription")

    inputfield_cardnum = page.locator('#card-number-input')
    inputfield_carddate = page.locator('#card-expiry-input')
    inputfield_cardCVV = page.locator('#card-cvv-input')
    bnt_subscribe = page.locator('.pay-button')

    with allure_step_with_screenshoot_on_failure(page, "check default fields"):
        expect(inputfield_cardnum).to_be_empty()
        expect(inputfield_carddate).to_be_empty()
        expect(inputfield_cardCVV).to_be_empty()
        expect(bnt_subscribe).to_be_disabled()

    with allure_step_with_screenshoot_on_failure(page, "Insert card with invalid date"):
        inputfield_cardnum.fill("4111 1111 1111 1111")
        inputfield_carddate.fill("1110")
        inputfield_cardCVV.fill("222")

    with allure_step_with_screenshoot_on_failure(page, "Button to sybscribe is still disabled"):
        expect(bnt_subscribe).to_be_disabled()
    

@allure.title("Проверка карт")
@allure.description("Использование карты с пустым CVV")
@allure.severity(allure.severity_level.MINOR)
@allure.feature("Credit_card")
@allure.testcase("TC_3")
@pytest.mark.play
def test_card_empty_CVV(page: Page):
    page.goto("http://localhost:3000/automation-lab/subscription")

    inputfield_cardnum = page.locator('#card-number-input')
    inputfield_carddate = page.locator('#card-expiry-input')
    inputfield_cardCVV = page.locator('#card-cvv-input')
    bnt_subscribe = page.locator('.pay-button')

    with allure_step_with_screenshoot_on_failure(page, "check default fields"):
        expect(inputfield_cardnum).to_be_empty()
        expect(inputfield_carddate).to_be_empty()
        expect(inputfield_cardCVV).to_be_empty()
        expect(bnt_subscribe).to_be_disabled()

    with allure_step_with_screenshoot_on_failure(page, "Insert card with empty CVV"):
        inputfield_cardnum.fill("4111 1111 1111 1111")
        inputfield_carddate.fill("1130")

    with allure_step_with_screenshoot_on_failure(page, "Button to sybscribe is still disabled"):
        expect(bnt_subscribe).to_be_disabled()
    

@allure.title("Проверка карт")
@allure.description("Использование невалидной карты")
@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Credit_card")
@allure.testcase("TC_4")
@pytest.mark.play
def test_card_invalid_card(page: Page):
    page.goto("http://localhost:3000/automation-lab/subscription")

    inputfield_cardnum = page.locator('#card-number-input')
    inputfield_carddate = page.locator('#card-expiry-input')
    inputfield_cardCVV = page.locator('#card-cvv-input')
    bnt_subscribe = page.locator('.pay-button')

    card_errors = page.locator('.card-errors')
    
    popup_success_pay= page.locator('.modal-content.success-modal')
    popup_success_details = page.locator('.success-details')
    popup_success_btn_Great = page.locator('.modal-close-btn')

    with allure_step_with_screenshoot_on_failure(page, "check default fields"):
        expect(inputfield_cardnum).to_be_empty()
        expect(inputfield_carddate).to_be_empty()
        expect(inputfield_cardCVV).to_be_empty()
        expect(bnt_subscribe).to_be_disabled()

    with allure_step_with_screenshoot_on_failure(page, "Insert invalid card"):
        inputfield_cardnum.fill("4000 0000 0000 0002")
        inputfield_carddate.fill("1130")
        inputfield_cardCVV.fill("222")
        bnt_subscribe.click()

    with allure_step_with_screenshoot_on_failure(page, "Check pop not appeared"):
        expect(popup_success_pay).not_to_be_visible()
        expect(popup_success_details).not_to_be_visible()
        expect(popup_success_btn_Great).not_to_be_visible()

    with allure_step_with_screenshoot_on_failure(page, "Error text appeared"):
        expect(card_errors).to_have_text("Карта отклонена. Попробуйте другую карту")


@allure.title("Проверка карт")
@allure.description("Недостаточно средств")
@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Credit_card")
@allure.testcase("TC_5")
@pytest.mark.play
def test_card_no_cash(page: Page):
    page.goto("http://localhost:3000/automation-lab/subscription")

    inputfield_cardnum = page.locator('#card-number-input')
    inputfield_carddate = page.locator('#card-expiry-input')
    inputfield_cardCVV = page.locator('#card-cvv-input')
    bnt_subscribe = page.locator('.pay-button')

    card_errors = page.locator('.card-errors')
    
    popup_success_pay= page.locator('.modal-content.success-modal')
    popup_success_details = page.locator('.success-details')
    popup_success_btn_Great = page.locator('.modal-close-btn')

    with allure_step_with_screenshoot_on_failure(page, "check default fields"):
        expect(inputfield_cardnum).to_be_empty()
        expect(inputfield_carddate).to_be_empty()
        expect(inputfield_cardCVV).to_be_empty()
        expect(bnt_subscribe).to_be_disabled()

    with allure_step_with_screenshoot_on_failure(page, "Insert card with no cash"):
        inputfield_cardnum.fill("4000 0000 0000 9995")
        inputfield_carddate.fill("1130")
        inputfield_cardCVV.fill("222")
        bnt_subscribe.click()

    with allure_step_with_screenshoot_on_failure(page, "Check pop not appeared"):
        expect(popup_success_pay).not_to_be_visible()
        expect(popup_success_details).not_to_be_visible()
        expect(popup_success_btn_Great).not_to_be_visible()

    with allure_step_with_screenshoot_on_failure(page, "Error text appeared"):
        expect(card_errors).to_have_text("Недостаточно средств на карте")
        