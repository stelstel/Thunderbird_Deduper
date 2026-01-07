"""
Configuration module for pytest that sets up the Python path for the Thunderbird_Deduper project.
This module initializes the test environment by adding the project root directory to the Python
path, allowing tests to import modules from the project without requiring installation.
The ROOT_DIR is determined by resolving the absolute path of the current file's parent directory.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))
