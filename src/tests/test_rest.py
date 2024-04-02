import time

from selenium.webdriver.common.by import By
def test_complete_function_1(driver, live_server):
    '''
    A trainer wants to register an account to predict the result of activity for IMU
    1. He needs to jump in register through the button in card body
    2. He needs to jump to login page through the navigation bar
    3. He needs to choose role as trainer and type the user_name as arnold, password as 123456
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
    assert "homepage" in driver.page_source
    time.sleep(2)
    # find register link through navigation bar
    register_link = driver.find_element(By.LINK_TEXT, "register")
    register_link.click()
    assert driver.current_url.endswith("/register")
    register_form_player_ID = driver.find_element(By.ID, "register")
    register_form_trainer_ID = driver.find_element(By.ID, "register")
    register_option_role = driver.find_element(By.ID, "register")
    register_form_password = driver.find_element(By.ID, "register")


def test_complete_function_2(driver, live_server):
    '''
    A player wants to register an account to predict the result of activity for IMU
    1. He needs to jump in register through the button in card body
    2. He needs to jump to login page through the page button
    3. He needs to choose role as player and type the user_name as a password as 123456
    4. He finds there is an account_ID already
    5. He logs in with account name 'a' and password 'a' and jumps to predict page
    6. He types in 1,1,1,1,1,1 for AccX, AccY, AccZ, gyroX, gyroY and gyroZ.
    7. The results should be:
    Movement: Moving
    Prediction: 1.0
    Resultant_Acc= 1.0
    Resultant_gyro= 1.0
    :param driver: the driver to Google Chrome
    :param live_server: the live_server on the Selenium tests
    :return:
    '''
    driver.get("http://localhost:5000")
    assert "homepage" in driver.page_source