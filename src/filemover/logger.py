import logging
import datetime as dt

def create_logger(name: str, verbose: bool, log_file: str | None = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger.propagate = False

    if not logger.hasHandlers():
        stream_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

        if log_file:
            if verbose:
                with open(log_file, 'a') as f:
                    # add a line to separate individual executions this is
                    # just a style choice to make the logs easier to read
                    # when using a single log file
                    date = dt.datetime.now().strftime("%Y-%m-%d")
                    f.write(f"\n===== {date} ===============================================================\n")
                    f.close()
            file_handler = logging.FileHandler(log_file, "a")
            file_formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
    return logger
