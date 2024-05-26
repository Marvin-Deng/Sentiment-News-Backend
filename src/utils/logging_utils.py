import logging
import traceback

logging.basicConfig(filename="error.log", level=logging.ERROR)


class LoggingUtils:

    @staticmethod
    def log_error(error, message, return_obj, status):
        error_message = f"{message}: {error}"
        logging.error(error_message)
        logging.error(traceback.format_exc())
        return error_message, return_obj, status
