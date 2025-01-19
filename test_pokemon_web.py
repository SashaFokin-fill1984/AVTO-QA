import pytest
import requests

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = 'https://pokemonbattle-stage.ru/'

def test_positive_login(browser):
    """
    TRP-1. Positive case
    """
    browser.get (URL)
    
    email_input = browser.find_element(by=By.CSS_SELECTOR, value='[class="auth__input k_form_f_email"]')
    email_input.click()
    email_input.send_keys('Fill19842605@yandex.ru')

    password_input = browser.find_element (by=By.ID, value= 'password')
    password_input.click()
    password_input.send_keys ('Egor2605!@!')

    button = browser.find_element(by = By.CSS_SELECTOR, value = '[class="auth__button k_form_send_auth"]')
    button.click()

    WebDriverWait(browser, timeout=20, poll_frequency=2).until(EC.url_to_be('https://pokemonbattle-stage.ru/'))
    trainer_id = browser.find_element(by = By.CSS_SELECTOR, value='[class="header__id-texts"]')
    
    #text_id = trainer_id.text.replace('\n','')
    #assert text_id == 'ID 1863', 'Unexpected trainer id'
    assert trainer_id.text.replace('\n', ': ') == 'ID: 1863', 'Unexpected ID trainer' 

CASES = [
    ('1', 'Fill19842605yandex.ru' , 'Egor2605!@!' , ['Введите почту', '']),
    ('2', 'Fill19842605@yandex.ru' , 'Egor2605!@' , ['', 'Неверные логин или пароль']),
    ('3', 'Fill19842605@yandex' , 'Egor2605!@!' , ['Введите почту', '']),
    ('4', '' , 'Egor2605!@!' , ['Введите почту', '']),
    ('5', 'Fill19842605@yandex.ru' , '' , ['', 'Введите пароль']),
]

@pytest.mark.parametrize('case_number, email, password, alerts' , CASES)
def test_nigative_login(case_number, email, password, alerts, browser):
    """
    TRP-1. Negative case
    """
    logger.info(f'CASE : {case_number}')
    browser.get(URL)
    
    email_input = browser.find_element(by=By.CSS_SELECTOR, value='[class="auth__input k_form_f_email"]')
    email_input.click()
    email_input.send_keys(email)

    password_input = browser.find_element (by=By.ID, value= 'password')
    password_input.click()
    password_input.send_keys(password)

    button = browser.find_element(by = By.CSS_SELECTOR, value = '[class="auth__button k_form_send_auth"]')
    button.click()

    alerts_messages = browser.find_elements(by=By.CSS_SELECTOR, value= '[class*="auth__error"]')
    alerts_list = []
    for elements in alerts_messages:
        alerts_list.append(elements.text)

    assert alerts_list == alerts, 'Unexpected alerts in authentication form'


