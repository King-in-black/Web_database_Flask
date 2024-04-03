import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
def test_navigation_bar(driver, live_server):
    '''
    Tests all functions of navigation bar. Switch to homepage link and then switch to register link,
    :param driver:
    :param live_server:
    :return:
    '''
    driver.get("http://localhost:5000")
    # Here is the home page
    assert "homepage" in driver.page_source
    # jump to register page.
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "nav_register")))
    register_link = driver.find_element(By.ID, "nav_register")
    ActionChains(driver).move_to_element(register_link).perform()
    register_link.click()
    assert driver.current_url.endswith("/register")
    # jump to login page
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "nav_login")))
    login_link = driver.find_element(By.ID, "nav_login")
    ActionChains(driver).move_to_element(login_link).perform()
    login_link.click()
    assert driver.current_url.endswith("/login")
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "nav_homepage")))
    # return to homepage
    homepage_link = driver.find_element(By.ID, "nav_homepage")
    ActionChains(driver).move_to_element(homepage_link).perform()
    homepage_link.click()
    assert driver.current_url.endswith("/homepage")