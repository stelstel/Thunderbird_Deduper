import logging
from logging.handlers import RotatingFileHandler
from unittest.mock import patch

import functions.logging_setup as logging_setup


def clear_root_logger():
    """Helper to reset root logger between tests."""
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    logger.setLevel(logging.NOTSET)


def test_setup_logging_adds_handler_and_sets_info_level(tmp_path):
    clear_root_logger()

    with patch("functions.logging_setup.os.makedirs"), \
         patch("functions.logging_setup.os.path.join", return_value=str(tmp_path / "log.log")):

        logging_setup.setup_logging(debug=False)

        logger = logging.getLogger()

        assert logger.level == logging.INFO
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], RotatingFileHandler)


def test_setup_logging_sets_debug_level_when_debug_true(tmp_path):
    clear_root_logger()

    with patch("functions.logging_setup.os.makedirs"), \
         patch("functions.logging_setup.os.path.join", return_value=str(tmp_path / "log.log")):

        logging_setup.setup_logging(debug=True)

        logger = logging.getLogger()

        assert logger.level == logging.DEBUG


def test_setup_logging_does_not_add_duplicate_handlers(tmp_path):
    clear_root_logger()

    with patch("functions.logging_setup.os.makedirs"), \
         patch("functions.logging_setup.os.path.join", return_value=str(tmp_path / "log.log")):

        logging_setup.setup_logging()
        logging_setup.setup_logging()  # called twice on purpose

        logger = logging.getLogger()

        assert len(logger.handlers) == 1
