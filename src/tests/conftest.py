import pytest
import subprocess
import time
import os
from selenium import webdriver
import socket

@pytest.fixture(scope='module')
def live_server():
    '''
    Define a live_server for the Selenium tests on the Chrome Browser
    '''
    server=subprocess.Popen(['flask',"--app","controller","run","--port","5000"])
    time.sleep(5)
    try:
        yield server
    finally:
        server.terminate()

@pytest.fixture(scope="module")
def driver():
    '''
    Define the server to used Chrome driver
    '''
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

