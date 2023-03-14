from selenium import webdriver
from selenium.webdriver.common.by import *
import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

MOMONDO_SITE = "https://www.momondo.se/"

@pytest.fixture
def load_driver():
    driver = webdriver.Chrome()
    driver.get(MOMONDO_SITE)
    driver.implicitly_wait(5)
    driver.delete_all_cookies
    yield driver
    driver.quit()



def test_welcome_text(load_driver):
    driver = load_driver
    welcome = driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[5]/div[1]/div[1]/div/div[1]/div/section[1]/div')
    assert welcome.text == "Välkommen! Hitta ett flexibelt flyg för din nästa resa."

def test_momondo_word_in_url(load_driver):
    driver = load_driver
    assert "momondo" in driver.current_url, f"expected momondo in url, got:{driver.current_url}"   


def test_from_search_box(load_driver):  
    driver = load_driver
    from_search_box = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[5]/div[1]/div[1]/div/div[1]/div/section[2]/div/div/div/div/div/div[1]/div[2]/div/div[1]')
    assert from_search_box.text == "Köpenhamn (CPH)"



def test_to_search_box(load_driver):
    driver = load_driver
    action = ActionChains(driver)
    to_search_box = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[5]/div[1]/div[1]/div/div[1]/div/section[2]/div/div/div/div/div/div[1]/div[2]/div/div[3]/div')
    action.move_to_element(to_search_box).click()
    action.send_keys('Paris, Frankrike (PAR)').send_keys(Keys.ENTER)

def test_flight_class_selection(load_driver):
    driver = load_driver
    action = ActionChains(driver)
    flight_class_selection = Select(driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[5]/div[1]/div[1]/div/div[1]/div/section[2]/div/div/div/div/div/div[1]/div[1]/div[3]/select'))
    flight_class_selection.select_by_visible_text("Business")
    search_flight_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[5]/div[1]/div[1]/div/div[1]/div/section[2]/div/div/div/div/div/div[1]/div[3]/button')
    action.move_to_element(search_flight_button).click()

   
    