import json
import logging
from pathlib import Path

_logger = logging.getLogger(__name__)

class Validator:
    """
    Validates actual upload result against expected results from a JSON file.

    Attributes:
        actual (dict): The actual result returned from the system under test.
        expected (dict): The expected result loaded from the JSON file.
        expected_key (str): The key in the expected results JSON to compare against.
    """


    def __init__(self, actual_result, expected_file_path, expected_key):
        """
            Initializes the Validator with actual result, path to expected results file,
            and the key representing the specific test scenario.

            Raises:
                FileNotFoundError: If the expected results file does not exist.
                ValueError: If the file is not valid JSON or the expected key is missing.
        """
        self.actual = actual_result
        expected_file_path = Path(expected_file_path)

        try:
            all_expected = json.loads(expected_file_path.read_text())
        except FileNotFoundError:
            raise FileNotFoundError(f"Expected results file not found at: {expected_file_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Expected results file is not a valid JSON: {expected_file_path}")

        if expected_key not in all_expected:
            raise ValueError(f"Expected key '{expected_key}' not found in expected results file.")

        self.expected = all_expected[expected_key]
        self.expected_key = expected_key

    def assert_result_matches(self):
        """
            Validates that the actual result matches the expected result.

            Compares:
                - Status ("success" or "error")
                - Number of successful items (success_count)
                - Number of errors (error_count)
                - Error messages (expected_errors)

            Raises:
                AssertionError: If any mismatch is found between actual and expected.
            """
        actual = self.actual
        expected = self.expected

        # Determine expected status if not explicitly set
        expected_status = expected.get("status") or (
            "success" if expected.get("error_count", 0) == 0 else "error"
        )

        assert actual.get("status") == expected_status, (
            f"Status mismatch:\nExpected: {expected_status}\nActual:   {actual.get('status')}"
        )
        _logger.info("✅ Status matches expected.")

        # Validate success count
        if "success_count" in expected:
            actual_success = len(actual.get("data", []))
            assert actual_success == expected["success_count"], (
                f"Success count mismatch:\nExpected: {expected['success_count']}\nActual:   {actual_success}"
            )
            _logger.info("✅ Success count matches expected.")

        #Validate error count
        if "error_count" in expected:
            actual_errors = len(actual.get("errors", []))
            assert actual_errors == expected["error_count"], (
                f"Error count mismatch:\nExpected: {expected['error_count']}\nActual:   {actual_errors}"
            )
            _logger.info("✅ Error count matches expected.")

        # Validate exact error messages if provided
        if "expected_errors" in expected:
            assert "errors" in actual, (
                f"Missing 'errors' field in actual result.\nExpected: {expected['expected_errors']}\nActual: {actual}"
            )

            assert actual.get("errors", []) == expected["expected_errors"], (
                f"Error messages mismatch:\nExpected: {expected['expected_errors']}\nActual:   {actual.get('errors', [])}"
            )
            _logger.info("✅ Error messages match expected.")