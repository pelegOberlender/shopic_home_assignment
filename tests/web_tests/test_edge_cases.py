import logging
import pytest
from tests.utils.validator import Validator
from tests.utils.path_utils import find_project_root
from pathlib import Path
import os

_logger = logging.getLogger(__name__)

PROJECT_ROOT = find_project_root()
DATA_DIR = PROJECT_ROOT / "data" / "edge_case"
EXPECTED_RESULTS_PATH = PROJECT_ROOT / "data" / "expected_results_edge_case.json"

@pytest.mark.parametrize(
    "file_path, expected_key",
    [
        (DATA_DIR / "empty_file.csv", "empty_file"),
        (DATA_DIR / "missing_headers.csv", "missing_headers"),
        (DATA_DIR / "missing_cell.csv", "missing_cell"),
        (DATA_DIR / "non_numeric_price.csv", "non_numeric_price"),
        (DATA_DIR / "mixed_validity.csv", "mixed_validity"),
        (DATA_DIR / "text_in_numeric.csv", "text_in_numeric"),
        (DATA_DIR / "not_csv.txt", "non_csv_format"),
        (DATA_DIR / "file_not_found", "file_not_found")
    ]
)

def test_upload(file_path, expected_key, web_user):
    """
        Runs upload tests for edge-case files and validates the results.
        Handles the 'file not found' case separately using pytest.raises.
    """
    file_path = os.path.realpath(file_path)
    _logger.info("Testing edge case file: %s", file_path)

    if expected_key == "file_not_found":
        with pytest.raises(ValueError, match="No result text found"):
            web_user.choose_specific_file(file_path).click_upload().get_upload_result()
        return

    result = web_user.choose_specific_file(file_path).click_upload().get_upload_result()
    _logger.info("Result: %s", result)

    validator = Validator(
        actual_result=result,
        expected_file_path=os.path.realpath(EXPECTED_RESULTS_PATH),
        expected_key=expected_key
    )
    validator.assert_result_matches()


