import pytest
import os
from playwright.sync_api import sync_playwright
from playwright._impl._errors import Error as PlaywrightError

@pytest.fixture(scope="session")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()

@pytest.mark.skipif(os.environ.get('CI') == 'true', 
                   reason="Test skipped in CI environment - no local server")
def test_fetch_weather(browser_context):
    page = browser_context.new_page()
    try:
        page.goto("http://localhost:5000/", timeout=5000)
        
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
    except PlaywrightError as e:
        if "ERR_CONNECTION_REFUSED" in str(e):
            pytest.skip("Local server not available - skipping test")
        else:
            raise
