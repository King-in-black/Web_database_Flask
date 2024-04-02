
def test_home_page(driver, live_server):
    '''
    A trainer wants to register an account to predict the result of activity for IMU
    1. He needs to jump in Homepage
    2. He needs to jump to register page
    3. He needs to choose role as trainer and type the user_name as arnold, password as 123456
    4. He registers successfully and jumps to login page
    5. He logins in with the password and jumps to predict page
    6. He types in 0.1,0.1,0.1,0.1,0.1,0.1 for AccX, AccY, AccZ, gyroX, gyroY and gyroZ.
    7. The results should be:
    Movement: stationary
    Prediction: 0.0

    :param driver: the driver to Google Chrome
    :param live_server: the live_server on the Selenium tests
    :return:
    '''
    driver.get("http://localhost:5000")
    assert "homepage" in driver.page_source