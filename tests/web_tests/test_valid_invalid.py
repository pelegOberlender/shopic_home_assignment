
import logging
import pytest
from pathlib import Path
from tests.utils.validator import Validator

_logger = logging.getLogger(__name__)

@pytest.mark.parametrize(
    "file_path, expected_key",
    [
        # Valid and invalid test cases
        ("/Users/pelegoberlender/Desktop/school/home_assignment/data/valid_files/valid_products.csv", "valid_products"),
        ("/Users/pelegoberlender/Desktop/school/home_assignment/data/invalid_files/invalid_products.csv", "invalid_products"),
    ]
)
def test_upload(file_path, expected_key, web_user):
    """
        Uploads a file and validates the result against expected JSON data.
    """
    _logger.info("Running test for file: %s", file_path)
    result = web_user.choose_specific_file(file_path).click_upload().get_upload_result()
    _logger.info("Parsed result: %s", result)

    validator = Validator(result, Path("/Users/pelegoberlender/Desktop/school/home_assignment/data/expected_results.json"), expected_key)
    validator = Validator(
        actual_result=result,
        expected_file_path=Path("/Users/pelegoberlender/Desktop/school/home_assignment/data/expected_results.json"),
        expected_key=expected_key
    )
    validator.assert_result_matches()

