import os
import logging
import pendulum


TIMEZONE = pendulum.timezone("UTC")


def tz_converter(*args):
    return pendulum.now(TIMEZONE).timetuple()


logging.Formatter.converter = tz_converter
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(fmt=log_format, datefmt="%Y-%m-%d %H:%M:%S")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# log_folder = conf.get("core", "base_log_folder")
log_folder = "/tmp"
os.makedirs(log_folder, exist_ok=True)
today_file = pendulum.now(TIMEZONE).format("YYYYMMDD") + ".log"
file_handler = logging.FileHandler(os.path.join(log_folder, today_file))
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

logger.propagate = False

logging.basicConfig(level=logging.DEBUG)
