import logging

class SFFormatter(logging.Formatter):
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'
    def __init__(self, fmt: str) -> None:
        super(SFFormatter, self).__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class SFLogger(logging.Logger):

    DEBUG: int      = logging.DEBUG
    INFO: int       = logging.INFO
    WARN: int       = logging.WARN
    CRITICAL: int   = logging.CRITICAL

    def __init__(self, level: int, name: str) -> None:
        super(SFLogger, self).__init__(name, level)

        file_handler = logging.FileHandler(f"{name}.log")
        file_formatter = logging.Formatter("%(asctime)s | %(filename)s:%(lineno)d:%(funcName)s() [%(levelname)s] %(message)s")
        file_handler.setLevel(SFLogger.DEBUG)
        file_handler.setFormatter(file_formatter)
        self.addHandler(file_handler)

        stream_formatter = SFFormatter("%(asctime)s | %(filename)s:%(lineno)d:%(funcName)s() [%(levelname)s] %(message)s")
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(stream_formatter)
        self.addHandler(stream_handler)
