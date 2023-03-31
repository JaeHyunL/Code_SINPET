import os
import logging
import pendulum


TIMEZONE = pendulum.timezone("Asia/Seoul")
logging.basicConfig(level=logging.DEBUG)


def tz_converter(*args):
    return pendulum.now(TIMEZONE).timetuple()


def setLog(name: str = __name__) -> logging:
    """logging 관련 메서드

    Args:
        name (str, optional): 로깅에 구분 명

    Returns:
        logging: logging.getlogger 객체 반환.
    """
    logging.Formatter.converter = tz_converter
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(fmt=log_format, datefmt="%Y-%m-%d %H:%M:%S")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    log_folder = "/tmp"
    os.makedirs(log_folder, exist_ok=True)
    today_file = pendulum.now(TIMEZONE).format("YYYYMMDD") + ".log"
    file_handler = logging.FileHandler(os.path.join(log_folder, today_file))
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    logger = logging.getLogger(name)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger
