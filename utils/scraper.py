from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

from utils.tools import cleanup_csv, read_csv


class Scraper:
    def __init__(self):
        load_dotenv()
        self.dashboard_url = os.getenv("DASHBOARD_URL")
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")

        if not self.dashboard_url or not self.username or not self.password:
            raise ValueError("Dashboard URL, username, and password are required")

        self.playwright = None
        self.page = None


    def _start_playwright(self):
        self.playwright = sync_playwright().start()
        browser = self.playwright.chromium.launch(headless=True)
        context = browser.new_context()
        self.page = context.new_page()

    def _stop_playwright(self):
        try:
            if self.page:
                self.page.context.close()
                self.page.context.browser.close()
                self.page = None
            if self.playwright:
                self.playwright.stop()
                self.playwright = None
        except Exception as e:
            print(f"Error stopping playwright: {e}")
        finally:
                self.page = None
                self.playwright = None

    def _login_to_dashboard(self):
        """
        Logs into the dashboard using Playwright and returns the logged-in page.
        """
        self.page.goto(self.dashboard_url)
        
        # Wait for the login form
        form_selector = ".qbs-screen"
        self.page.wait_for_selector(form_selector, timeout=10000)
        
        self.page.fill('#username-input', self.username)
        self.page.click('#username-submit-button')
        self.page.wait_for_load_state('networkidle')

        self.page.fill('#password-input input', self.password)
        self.page.click('#password-submit-button')
        self.page.wait_for_load_state('networkidle')
    
    def _extract_rows(self) -> list[dict]:
        result = []

        self.page.wait_for_selector('div.grid', timeout=15000)

        #if popup is present, click the close button
        close_btn = self.page.locator('button[data-automation-id="welcome-modal-close-btn"]')
        if close_btn.count() > 0 and close_btn.is_visible():
            close_btn.click()
        
        #hover over the grid_div and click the download csv button
        self.page.hover('div.grid')
        self.page.click('.visual-menu')
        with self.page.expect_download() as download_info:
            self.page.click('li[data-automation-id="dashboard_visual_dropdown_export"]')
        download = download_info.value
        download.save_as("performance.csv")

        cells = read_csv('performance.csv')
        
        # For each row, extract the five expected columns
        for index, cell in enumerate(cells):

            if len(cell) < 5:
                raise Exception(f"Invalid row length for row {cell[0]}")
            
            #skip the first row
            if index == 0:
                continue
            
            result.append({
                "code": cell[0],
                "date": cell[1],
                "state": cell[2],
                "ftds": cell[3],
                "registration": cell[4],
            })
        return result

    def extract_data(self) -> list[dict]:
        """
        Uses Playwright to login and scrape the dashboard data
        """
        performance_data = []
        try:
            self._start_playwright()
            self._login_to_dashboard()
       
            performance_data = self._extract_rows()

        except Exception as e:
            print(f"Error extracting data: {e}")
            raise e
        finally:
            self._stop_playwright()
            cleanup_csv("performance.csv")

        return performance_data

