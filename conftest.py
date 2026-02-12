# conftest.py

"""
Configuration file for pytest that sets up the Python path for the Thunderbird Deduper project.
This module ensures that the root directory of the project is added to the Python path,
allowing imports from the project root to work correctly during testing.
Module-level variables:
    ROOT_DIR (Path): Absolute path to the directory containing this conftest.py file.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))
