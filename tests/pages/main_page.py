import json
import logging
from playwright.sync_api import sync_playwright, Page

_logger = logging.getLogger(__name__)

class WebUser:
    """
        A wrapper class around a Playwright Page to simulate a user's interaction
        with the file upload UI.
    """

    def __init__(self, page: Page):
        """
            Initializes WebUser with a Playwright Page object and maps relevant UI elements.
        """
        self.page = page
        self.choose_file_input = page.locator('input[type="file"]')
        self.upload_button = page.locator('button[type="submit"]')
        self.results_block = page.locator('#results')

    def navigate(self, url):
        """
            Navigates the browser to the specified URL.

            Args:
                url (str): The target URL to navigate to.

            Returns:
                WebUser: self
        """
        self.page.goto(url)
        _logger.info("Navigated to URL: %s", url)
        return self

    def click_choose(self):
        """
            Clicks the file input element (simulate 'Choose File' interaction).

            Returns:
                WebUser: self
        """
        self.choose_file_input.click()
        _logger.info("Choose File button clicked")

        return self

    def click_upload(self):
        """
            Clicks the upload button to submit the form.

            Returns:
                WebUser: self
        """
        self.upload_button.click()
        _logger.info("Upload button clicked")
        return self

    def choose_specific_file(self, file_path):
        """
            Sets the given file path as the input for file upload.

            Args:
                file_path (str): Path to the file to upload.

            Returns:
                WebUser: self
        """
        self.choose_file_input.set_input_files(file_path)
        _logger.info("File selected: %s", file_path)
        return self

    def get_upload_result(self):
        """
            Extracts and parses the result block content after upload.

            Returns:
                dict: Parsed JSON result from UI.

            Raises:
                ValueError: If result text is empty or not received.
        """
        result_text = self.results_block.inner_text().strip()
        _logger.info("Result text received:\n%s", result_text)

        if not result_text:
            raise ValueError("No result text found – possibly due to invalid or missing file path")

        result_parse = json.loads(result_text)
        return result_parse
