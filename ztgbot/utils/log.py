log_dict = {
    "INFO": 3,
    "ERROR":2,
    "WARNING": 0
}

class InvalidLogTypeError(Exception):
    "Raise when log_type parameter of log fnction is invalid"

def log(message, log_type="INFO"):
    """
    Log various messages into stdout

    message
        Message to be logged
    log_type
        ( values : ["INFO", "ERROR", "WARNING"] )
        Type of log

    Example 

    >>> log("looks like something went wrong", "ERROR")

    Output
    >>> [ERROR] [looks like something went wrong]
    """

    if log_type in log_dict:
        print(f"[{log_type}{' '*log_dict[log_type]}] [{message}]")

    else:
        raise InvalidLogTypeError