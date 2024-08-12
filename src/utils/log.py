import logging.handlers
import logging
import os


# Create a logs directory if it does not exist
if not os.path.exists("./logs"):
    os.makedirs("./logs")


# Set up the logger configuration
def setup_logger(name, log_file, log_level, backup_count=7):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.handlers.TimedRotatingFileHandler(log_file, when='D', backupCount=backup_count)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# Set up the loggers
logger_info = setup_logger("infoLog", "./logs/info.log", logging.INFO)
logger_error = setup_logger("errorLog", "./logs/error.log", logging.ERROR)


def write_log(log_type: str, message: str) -> None:
    """
    Write a log message to the log file.
    
    Args:
        log_type (str): The type of log message.
        message (str): The log message.
    """
    try:
        if log_type == "debug":
            logger_info.debug(message)
        elif log_type == "info":
            logger_info.info(message)
        elif log_type == "warning":
            logger_error.warning(message)
        elif log_type == "error":
            logger_error.error(message)
        elif log_type == "critical":
            logger_error.critical(message)
        else:
            logger_error.error("Unknown log method")
    except Exception as e:
        logger_error.error(f"Failed to write log message: {e}")
