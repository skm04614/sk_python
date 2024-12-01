import logging
from logging import Logger


class LogLevelContext:
    _logger: Logger
    _log_level: int
    _orig_log_level: int

    def __init__(self, logger: Logger, log_level: int) -> None:
        self._logger = logger
        self._log_level = log_level

    def __enter__(self) -> None:
        self._orig_log_level = self._logger.level
        self._logger.setLevel(self._log_level)

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._logger.setLevel(self._orig_log_level)


def adjust_log_level(log_level: int):
    def decorator(fn):
        def wrapper(logger, *args, **kwargs):
            with LogLevelContext(logger, log_level):
                return fn(logger, *args, **kwargs)

        return wrapper

    return decorator


def initialize_logger(logger_name: str | None = None, initial_log_level: int = logging.INFO) -> Logger:
    if not (logger := logging.getLogger(logger_name)).hasHandlers():
        logger.setLevel(initial_log_level)
        formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


@adjust_log_level(logging.WARNING)
def fn(logger: Logger) -> None:
    logger.info("1")
    logger.debug("2")
    logger.warning("3")
    logger.critical("4")
    logger.critical("5")
    logger.warning("6")
    logger.debug("7")
    logger.info("8")


if __name__ == "__main__":
    local_logger = initialize_logger(__file__, logging.DEBUG)

    fn(local_logger)
    local_logger.info("=======================")
    fn(local_logger)
    local_logger.info("=======================")
