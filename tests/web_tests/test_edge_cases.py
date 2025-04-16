import logging
import pytest
from tests.utils.validator import Validator
from pathlib import Path


_logger = logging.getLogger(__name__)

@pytest.mark.parametrize(
    "file_path, expected_key",
    [
        # Edge cases
        ("/Users/pelegoberlender/Desktop/school/home_assignment/data/edge_case/empty_file.csv", "empty_file"),
        ("/Users/pelegoberlender/Desktop/school/home_assignment/data/edge_case/missing_headers.csv", "missing_headers"),
        ("/Users/pelegoberlender/Desktop/school/home_assignment/data/edge_case/missing_cell.csv", "missing_cell"),
        ("/Users/pelegoberlender/Desktop/school/home_assignment/data/edge_case/non_numeric_price.csv", "non_numeric_price"),
        ("/Users/pelegoberlender/Desktop/school/home_assignment/data/edge_case/mixed_validity.csv", "mixed_validity"),
        ("/Users/pelegoberlender/Desktop/school/home_assignment/data/edge_case/text_in_numeric.csv", "text_in_numeric"),
        ("/Users/pelegoberlender/Desktop/school/home_assignment/data/edge_case/not_csv.txt", "non_csv_format"),
        ("/Users/pelegoberlender/Desktop/school/home_assignment/data/edge_case/file_not_found", "file_not_found")
    ]
)

def test_upload(file_path, expected_key, web_user):
    """
        Runs upload tests for edge-case files and validates the results.
        Handles the 'file not found' case separately using pytest.raises.
    """
    _logger.info("Testing edge case file: %s", file_path)

    if expected_key == "file_not_found":
        with pytest.raises(ValueError, match="No result text found"):
            web_user.choose_specific_file(file_path).click_upload().get_upload_result()
        return

    result = web_user.choose_specific_file(file_path).click_upload().get_upload_result()
    _logger.info("result: {}".format(result))

    validator = Validator(
        actual_result=result,
        expected_file_path=Path("/Users/pelegoberlender/Desktop/school/home_assignment/data/expected_results_edge_case.json"),
        expected_key=expected_key
    )
    validator.assert_result_matches()


