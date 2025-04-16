# 🛒 Shopic Home Assignment – Automated Testing with Playwright

This repository contains my submission for Shopic’s Software Engineering Internship assignment.  
It features an end-to-end testing framework built with **Python** and **Playwright**, validating CSV file uploads to the product management system.

---

##  Setup Instructions

> Requires **Python 3.12+** installed on your system.

  1. **Clone the repository**  
   *(Skip this if you already have the files locally)*

   ```bash
   git clone <repo-url>
   cd home_assignment
   ```

   2. **Create and activate a virtual environment**

      ```bash
      python -m venv venv
      source venv/bin/activate      # On Windows: venv\Scripts\activate
      ```
   3. **Install dependencies**

      ```bash
      pip install -r requirements.txt
      ```
  ---

##  Running the Tests
  
  You can run all tests or specific test files via `pytest`.  
  Make sure you run from the project root and set `PYTHONPATH=.` to enable relative imports.
  
  ### Run all tests:
  
  ```bash
  PYTHONPATH=. pytest tests/web_tests -s
  ```
  
  ### Run a specific test file:
  
  ```bash
  PYTHONPATH=. pytest tests/web_tests/valid_invalid_tests.py -s
  ```
  
  ---

##  Project Structure
  
```plaintext
   home_assignment/
  │
  ├── data/                     
  │
  ├── server/                  
  │   ├── main.py               
  │   └── ...                   
  │
  ├── tests/                    # Automated UI test suite using Playwright + Pytest
  │   ├── web_tests/            # Main directory for test cases
  │   │   ├── edge_cases_tests.py        # Tests for edge-case CSV inputs (e.g., empty fields, incorrect types)
  │   │   ├── valid_invalid_tests.py     # Tests for validating both valid and invalid product uploads
  │   │   └── conftest.py                # Shared fixtures (e.g., browser setup, base URL)
  │   │
  │   ├── pages/               # Page Object Models (POM)
  │   │   └── main_page.py     # UI element selectors and page interaction logic
  │   │
  │   └── utils/               # Validation utilities for test assertions
  │       └── validator.py     # Custom class to assert actual vs. expected upload results
  │
  ├── requirements.txt         # Python dependencies
  └── README.md                
```
    ---

##  Assumptions

  - File format is CSV 
  - The uploaded file is expected to be in valid .csv format with comma-separated values.
  - Expected results are correct
  - The content in expected_results.json is assumed to be valid and trusted as the ground truth for test validations.
  - Test environment is properly set up
  - It is assumed that the server is running at http://localhost:8000 before tests are executed.
  - Browser automation works reliably
  - The Playwright environment is assumed to correctly handle browser automation and interactions.
---

##  Known Limitations

  - Relies on static DOM selectors (`#results`, specific button types).
  - Visual UI checks are not implemented.
  - Edge cases not fully covered:
  - Multibyte characters (e.g., Hebrew, Japanese)
  - Extremely large CSVs
  - Malformed files (e.g., broken delimiters, unescaped characters)

---

##  Test Categories
  
  | Category       | Description                                                                               |
  |----------------|-------------------------------------------------------------------------------------------|
  | Valid Uploads  | Tests well-formed CSVs with valid fields and values                                       |
  | Invalid Inputs | Detects missing fields, incorrect types, and formatting issues                            |
  | Edge Cases     | Handles empty files, missing headers, non-text values, mixed-validity rows, invalid file formats, and errors such as "No such file or directory". |    
    ---

