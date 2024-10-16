import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests


def test_complete_function_Database_check(driver, live_server):
    """
     A player wants to register an account to predict the result of activity for IMU. The storage of data is
     also under test.
    1. He needs to jump in register through the button in navigation bar
    2. He needs to jump to login page through the card body
    3. He needs to choose role as player and type the user_name as a password as 123456
    4. He finds there is an account_ID already
    5. He logs in with account name 'bill' and password 123456 and jumps to predict page
    6. He types in 1,1,1,1,1,1 for AccX, AccY, AccZ, gyroX, gyroY and gyroZ.
    7. The results should be:
    Movement: Moving
    Prediction: 1.0
    Resultant_Acc= 1.0
    Resultant_gyro= 1.0
    :param driver: the driver to Google Chrome
    :param live_server: the live_server on the Selenium tests
    :return:1
    """
    driver.get("http://localhost:5000")
    assert "homepage" in driver.page_source
    time.sleep(10)
    # find register link through navigation bar
    # step 1:
    register_link = driver.find_element(By.ID, "nav_register")
    register_link.click()
    assert driver.current_url.endswith("/register")
    # step 2:
    register_form_player_ID = driver.find_element(By.ID, "Player_ID")
    register_form_trainer_ID = driver.find_element(By.ID, "Trainer_ID")
    register_option_role = driver.find_element(By.ID, "Role")
    register_form_password = driver.find_element(By.ID, "password")
    register_form_player_ID.send_keys("bill")
    register_form_trainer_ID.send_keys("bill")
    register_form_password.send_keys("123456")
    register_role_select = Select(register_option_role)
    register_role_select.select_by_visible_text("Player")
    button_register = driver.find_element(By.ID, "submit")
    button_register.click()
    time.sleep(3)
    assert driver.current_url.endswith("/login")
    # interfere with The Rest Api
    response_user = requests.get("http://localhost:5000/get/get_player/bill")
    assert response_user.status_code == 200
    json_data = response_user.json()
    assert json_data["Player_ID"] == "bill"
    # step 3:
    login_form_user_id = driver.find_element(By.ID, "user_id")
    login_option_role = driver.find_element(By.ID, "role")
    login_form_password = driver.find_element(By.ID, "password")
    login_form_user_id.send_keys("bill")
    login_form_password.send_keys("123456")
    login_role_select = Select(login_option_role)
    login_role_select.select_by_visible_text("Player")
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
    predict_form_trainer_id.send_keys("bill")
    predict_form_player_id.send_keys("bill")
    predict_form_accX.send_keys(0.01)
    predict_form_accY.send_keys(0.01)
    predict_form_accZ.send_keys(0.01)
    predict_form_gyroX.send_keys(0.01)
    predict_form_gyroY.send_keys(0.01)
    predict_form_gyroZ.send_keys(0.01)
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
    assert "0" in predict_result_prediction.text
    assert "Status" in predict_result_move.text
    assert "Stationary" in predict_result_move.text
    assert "Acceleration" in predict_result_ra.text
    assert "0173" in predict_result_ra.text
    assert "Gyro" in predict_result_rg.text
    assert "0173" in predict_result_rg.text
