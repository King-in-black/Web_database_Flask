import pytest
import subprocess
import time
import os
from selenium import webdriver
import socket
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("window-size=1920x1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

@pytest.fixture(scope='module')
def live_server():
    '''
    Define a live_server for the Selenium tests on the Chrome Browser
    '''
    server=subprocess.Popen(['flask',"--app","controller_tests","run","--port","5000"])
    time.sleep(20)
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
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()