
import logging
import pytest
from tests.utils.path_utils import find_project_root
from tests.utils.validator import Validator
from pathlib import Path
import os

_logger = logging.getLogger(__name__)

PROJECT_ROOT = find_project_root()
DATA_DIR = PROJECT_ROOT / "data"
EXPECTED_RESULTS_PATH = PROJECT_ROOT / "data" / "expected_results.json"

@pytest.mark.parametrize(
    "file_path, expected_key",
    [
        # Valid and invalid test cases
        ( DATA_DIR / "valid_files/valid_products.csv", "valid_products"),
        ( DATA_DIR / "invalid_files/invalid_products.csv", "invalid_products"),
    ]
)
def test_upload(file_path, expected_key, web_user):
    """
        Uploads a file and validates the result against expected JSON data.
    """
    file_path = Path(file_path).resolve()
    _logger.info("Running test for file: %s", file_path)
    result = web_user.choose_specific_file(file_path).click_upload().get_upload_result()
    _logger.info("Parsed result: %s", result)

    validator = Validator(
        actual_result=result,
        expected_file_path=os.path.realpath(EXPECTED_RESULTS_PATH),
        expected_key=expected_key
    )
    validator.assert_result_matches()

