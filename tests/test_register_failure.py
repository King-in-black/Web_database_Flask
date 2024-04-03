import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
def test_register_failure(driver, live_server):
    '''
    1. Jump to homepage
    2. Jump to register through homepage button
    3 . test to register an account called Ali; player ; password 123456 ; his trainer is KG.
    4.He tries to register again with same username and with different password
    5.An error of 404 is raised.
    '''
    driver.get("http://localhost:5000")
    # Here is the home page
    assert "homepage" in driver.page_source
    # find register link through navigation bar
    # step 1:
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "register")))
    # wait when the page finish loading
    register_link = driver.find_element(By.ID, "register")
    ActionChains(driver).move_to_element(register_link).perform()
    register_link.click()
    # step 2:
    assert driver.current_url.endswith("/register")
    register_form_player_ID = driver.find_element(By.ID, "Player_ID")
    register_form_trainer_ID = driver.find_element(By.ID, "Trainer_ID")
    register_option_role = driver.find_element(By.ID, "Role")
    register_form_password = driver.find_element(By.ID, "password")
    register_form_player_ID.send_keys("Ali")
    register_form_trainer_ID.send_keys("KG")
    register_form_password.send_keys("123456")
    register_role_select = Select(register_option_role)
    register_role_select.select_by_visible_text("Player")
    button_register = driver.find_element(By.ID, "submit")
    button_register.click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "user_id")))
    assert driver.current_url.endswith("/login")
    # step 3:
    register_link = driver.find_element(By.ID, "nav_register")
    register_link.click()
    time.sleep(5)
    # step 4:
    assert driver.current_url.endswith("/register")
    register_form_player_ID = driver.find_element(By.ID, "Player_ID")
    register_form_trainer_ID = driver.find_element(By.ID, "Trainer_ID")
    register_option_role = driver.find_element(By.ID, "Role")
    register_form_password = driver.find_element(By.ID, "password")
    register_form_player_ID.send_keys("Ali")
    register_form_trainer_ID.send_keys("KG")
    register_form_password.send_keys("123456")
    register_role_select = Select(register_option_role)
    register_role_select.select_by_visible_text("Player")
    button_register = driver.find_element(By.ID, "submit")
    button_register.click()
    time.sleep(5)
    assert "404 Not Found" in driver.page_source






