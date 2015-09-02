def toss_coin(sides):
    """
    Choose a value from a given list of values
    [the coin can have more than two sides]
    """
    from random import choice
    return choice(sides)


def line_count(file_path):
    """
    Count the number of lines in a file with given path
    """
    with open(file_path) as file:
        return sum(1 for ln in file)


def create_reference(data, key=None, key_size=10):
    """
    Creates a md5 hash from given data and optionally
    appends an key as prefix. Used for quick integrity
    checks of db data
    """
    from hashlib import md5
    md5_object = md5(data.encode('utf-8'))
    reference = md5_object.hexdigest()
    key = str(key)
    reference = '%s_%s' % (key.zfill(key_size), reference)
    return reference.upper()


class Logger:
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

    def __init__(self, module):
        from logging import getLogger
        self.logger = getLogger(module)

    def log_with_date(self, message, level):
        import logging
        from datetime import datetime
        time_now = datetime.now()
        formatted_time = time_now.strftime('%Y-%m-%d %H:%M:%S.%f')
        self.logger.log(level, '[ %s ][ %s ] %s' % (
            logging.getLevelName(level),
            formatted_time,
            message))

    def log(self, message='', level=DEBUG):
        self.log_with_date(message, level)
