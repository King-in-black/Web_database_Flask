import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
def test_log_failure(driver, live_server):
    '''
    1. Jump to homepage
    2. Jump to register through homepage button
    3 . test to register an account called Ali; player ; password 123456 ; his trainer is KG.
    4.He tries to log in and he fails because he types ali and password 123456
    5.He retypes to change ali to Ali and successfully logins
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
    login_form_user_id = driver.find_element(By.ID, "user_id")
    login_option_role = driver.find_element(By.ID, "role")
    login_form_password = driver.find_element(By.ID, "password")
    login_form_user_id.send_keys("ali")
    login_form_password.send_keys("123456")
    login_role_select = Select(login_option_role)
    login_role_select.select_by_visible_text("Player")
    button_login = driver.find_element(By.ID, "submit")
    button_login.click()
    time.sleep(3)
    # step 4:
    assert driver.current_url.endswith("/login")
    assert "Invalid Player ID or password" in driver.page_source
    login_form_user_id = driver.find_element(By.ID, "user_id")
    login_form_password = driver.find_element(By.ID, "password")
    login_option_role = driver.find_element(By.ID, "role")
    login_form_user_id.clear()
    login_form_password.clear()
    login_form_user_id.send_keys("Ali")
    login_form_password.send_keys("123456")
    login_role_select = Select(login_option_role)
    login_role_select.select_by_index(0)
    login_role_select.select_by_visible_text("Player")
    button_login = driver.find_element(By.ID, "submit")
    button_login.click()
    time.sleep(3)
    # step 5:
    assert driver.current_url.endswith("/predict")





