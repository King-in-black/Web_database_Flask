import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def test_complete_function_1(driver, live_server):
    '''
    A trainer wants to register an account to predict the result of activity for IMU
    1. He needs to jump in register  through the navigation bar
    2. He needs to choose role as trainer and type the user_name as arnold, password as 123456
    3. He needs to jump to login page through the button in card body
    4. He registers successfully and jumps to login page
    5. He logs in  with the password and jumps to predict page
    6. He types in 0.1,0.1,0.1,0.1,0.1,0.1 for AccX, AccY, AccZ, gyroX, gyroY and gyroZ.
    7. The results should be:
    Movement: stationary
    Prediction: 0.0
    Resultant_Acc=0.1
    Resultant_gyro=0.1
    :param driver: the driver to Google Chrome
    :param live_server: the live_server on the Selenium tests
    :return:
    '''
    driver.get("http://localhost:5000")
    # Here is the home page
    assert "homepage" in driver.page_source
    time.sleep(3)
    # find register link through navigation bar
    # step 1:
    register_link = driver.find_element(By.LINK_TEXT, "register")
    register_link.click()
    assert driver.current_url.endswith("/register")
    # step 2:
    register_form_player_ID = driver.find_element(By.ID, "Player_ID")
    register_form_trainer_ID = driver.find_element(By.ID, "Trainer_ID")
    register_option_role = driver.find_element(By.ID, "Role")
    register_form_password = driver.find_element(By.ID, "password")
    register_form_player_ID.send_keys("arnold1")
    register_form_trainer_ID.send_keys("arnold1")
    register_form_password.send_keys("123456")
    register_role_select = Select(register_option_role)
    register_role_select.select_by_visible_text("Trainer")
    button_register = driver.find_element(By.ID, "submit")
    button_register.click()
    time.sleep(3)
    assert driver.current_url.endswith("/login")
    # step 3:
    login_form_user_id = driver.find_element(By.ID, "user_id")
    login_option_role = driver.find_element(By.ID, "role")
    login_form_password = driver.find_element(By.ID, "password")
    login_form_user_id.send_keys("arnold1")
    login_form_password.send_keys("123456")
    login_role_select = Select(login_option_role)
    login_role_select.select_by_visible_text("Trainer")
    button_login = driver.find_element(By.ID, "submit")
    button_login.click()
    time.sleep(3)
    assert driver.current_url.endswith("/predict")
    # step 4-5:
    predict_form_accX = driver.find_element(By.ID, "accX")
    predict_form_accY = driver.find_element(By.ID, "accY")
    predict_form_accZ = driver.find_element(By.ID, "accZ")
    predict_form_gyroX = driver.find_element(By.ID, "gyroX")
    predict_form_gyroY = driver.find_element(By.ID, "gyroY")
    predict_form_gyroZ = driver.find_element(By.ID, "gyroZ")
    predict_form_trainer_id = driver.find_element(By.ID, "Trainer_ID")
    predict_form_player_id = driver.find_element(By.ID, "Player_ID")
    predict_form_trainer_id.send_keys("arnold1")
    predict_form_player_id.send_keys("arnold1")
    predict_form_accX.send_keys(1)
    predict_form_accY.send_keys(1)
    predict_form_accZ.send_keys(1)
    predict_form_gyroX.send_keys(1)
    predict_form_gyroY.send_keys(1)
    predict_form_gyroZ.send_keys(1)
    button_predict = driver.find_element(By.ID, "turnon")
    ActionChains(driver).move_to_element(button_predict).perform()
    button_predict.click()
    time.sleep(3)
    predict_result_prediction = driver.find_element(By.ID, "prediction")
    predict_result_move = driver.find_element(By.ID, "move")
    predict_result_ra = driver.find_element(By.ID, "ra")
    predict_result_rg = driver.find_element(By.ID, "rg")

    # assert the result are correct
    assert "Prediction" in predict_result_prediction.text
    assert "1.0" in predict_result_prediction.text
    assert "Status" in predict_result_move.text
    assert "Moving" in predict_result_move.text
    assert "Acceleration" in predict_result_ra.text
    assert "1.73" in predict_result_ra.text
    assert "Gyro" in predict_result_rg.text
    assert "1.73" in predict_result_rg.text


