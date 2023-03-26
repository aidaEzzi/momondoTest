from selenium import webdriver
from selenium.webdriver.common.by import *
import pytest
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



MOMONDO_SITE = "https://www.momondo.se/"

@pytest.fixture
def load_driver():
    driver = webdriver.Chrome()
    driver.get(MOMONDO_SITE)
    driver.implicitly_wait(5)
    yield driver
    



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
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/div[5]/div[1]/div[1]/div/div[1]/div/section[2]/div/div/div/div/div/div[1]/div[2]/div/div[3]/div/div/input"))).send_keys("Paris, Frankrike (PAR)")
    search_box_selection = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/ul/li[1]')
    to_search_box = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[5]/div[1]/div[1]/div/div[1]/div/section[2]/div/div/div/div/div/div[1]/div[2]/div/div[3]')

    search_box_selection.send_keys(Keys.ENTER)

    assert to_search_box.text == 'Paris, Frankrike (PAR)'

def test_flight_class_selection(load_driver):
    driver = load_driver
    flight_class_selection = Select(driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[5]/div[1]/div[1]/div/div[1]/div/section[2]/div/div/div/div/div/div[1]/div[1]/div[3]/select'))
    selected_option = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[5]/div[1]/div[1]/div/div[1]/div/section[2]/div/div/div/div/div/div[1]/div[1]/div[3]/div/span[1]')

    flight_class_selection.select_by_visible_text("Business")

    assert selected_option.text == 'Business'


def test_teardown(load_driver):
    driver = load_driver
    driver.delete_all_cookies
    driver.quit()
    
