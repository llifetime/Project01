import logging
from pathlib import Path


def setup_logger(name, log_file, level=logging.INFO):
    """Setup a logger that handles different execution contexts"""

    # Get the project root directory
    project_root = Path(__file__).parent.parent

    # Create the full log file path
    full_log_path = project_root / log_file

    # Create the logs directory if it doesn't exist
    log_dir = full_log_path.parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create file handler
    file_handler = logging.FileHandler(full_log_path, mode='w')
    file_handler.setLevel(level)

    # Create console handler for tests (optional)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)  # Only show warnings and errors in console

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Prevent logging from propagating to the root logger
    logger.propagate = False

    return logger


# Setup loggers with absolute paths
masks_logger = setup_logger('masks', 'logs/masks.log')
main_logger = setup_logger('main', 'logs/main.log')
# Add other loggers as needed
