from coloredlogs import ColoredFormatter
from logging import getLogger, StreamHandler, CRITICAL, INFO, basicConfig

logs = getLogger(__name__)
logging_format = "%(levelname)s [%(asctime)s] [%(name)s] %(message)s"
logging_handler = StreamHandler()
logging_handler.setFormatter(ColoredFormatter(logging_format))
root_logger = getLogger()
root_logger.setLevel(CRITICAL)
root_logger.addHandler(logging_handler)
basicConfig(level=INFO)
logs.setLevel(INFO)
