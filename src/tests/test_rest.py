import pytest

def test_home_page(driver, live_server):
    driver.get("http://localhost:5000")
    assert "Hello, Flask!" in driver.page_source