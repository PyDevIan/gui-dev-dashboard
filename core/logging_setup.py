# app/core/logging_setup.py
from loguru import logger
import logging, sys
from pathlib import Path

def setup_logging(log_file: Path | None = None, level: str = "INFO"):
    logger.remove()
    logger.add(sys.stderr, level=level, backtrace=True, diagnose=False)

    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            log_file,
            rotation="10 MB",
            retention="14 days",
            compression="zip",
            level="DEBUG",
            backtrace=True,
            diagnose=False,
        )

    class InterceptHandler(logging.Handler):
        def emit(self, record):
            try:
                lvl = logger.level(record.levelname).name
            except Exception:
                lvl = record.levelno
            frame, depth = logging.currentframe(), 2
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1
            logger.opt(depth=depth, exception=record.exc_info).log(lvl, record.getMessage())

    # DO NOT use force=True in a library; here in bootstrap it's okay
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("pdfminer").setLevel(logging.WARNING)
    logging.getLogger("pdfplumber").setLevel(logging.WARNING)
    return logger
