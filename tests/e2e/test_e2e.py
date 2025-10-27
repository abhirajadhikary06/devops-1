import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()

def test_fetch_weather(browser_context):
    page = browser_context.new_page()
    page.goto("http://localhost:5000/")
    
    # Fill form and submit
    page.fill('input[name="city"]', "Berlin")
    page.click('button[type="submit"]')
    
    # Check weather data and time display
    page.wait_for_selector('p')
    assert "Temperature:" in page.inner_html('body')
    assert "Humidity:" in page.inner_html('body')
    assert "Weather Code:" in page.inner_html('body')
    assert "Response Time:" in page.inner_html('body')
    assert "seconds" in page.inner_html('body')
