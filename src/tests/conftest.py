import pytest
import subprocess
import time
import os
from selenium import webdriver
import socket
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
option = webdriver.ChromeOptions()
option.add_argument("start-maximized")

@pytest.fixture(scope='module')
def live_server():
    '''
    Define a live_server for the Selenium tests on the Chrome Browser
    '''
    server=subprocess.Popen(['flask',"--app","controller_tests","run","--port","5000"])
    time.sleep(10)
    try:
        yield server
    finally:
        server.terminate()

@pytest.fixture(scope="module")
def driver():
    '''
    Define the server to used Chrome driver
    '''
    # make sure that drive's version is suitable for ChromeDriver.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)
    yield driver
    driver.quit()

