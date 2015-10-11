import logging
from datetime import datetime


class LoggerBaseDecorator:
    def __init__(self, params=None):
        self._message = ''
        self._params = params

    def __call__(self, callback):
        def decorated_callback():
            output = callback()
            output = output.replace(self._token(), self._replace())
            return output
        return decorated_callback

    def _token(self):
        return ''

    def _replace(self):
        return ''


class MessageLogDecorator(LoggerBaseDecorator):
    def _token(self):
        return '%message%'

    def _replace(self):
        return self._params['message']


class TimeLogDecorator(LoggerBaseDecorator):
    def _token(self):
        return '%time%'

    def _replace(self):
        now = datetime.now()
        if 'time_format' not in self._params:
            self._params['time_format'] = '%Y-%m-%d %H:%M:%S.%f'
        return '[%s]' % now.strftime(self._params['time_format'])


class LevelLogDecorator(LoggerBaseDecorator):
    def _token(self):
        return '%level%'

    def _replace(self):
        return '[%s]' % logging.getLevelName(self._params['level'])


class Logger:
    LEVEL_DEBUG = 10
    LEVEL_INFO = 20
    LEVEL_WARNING = 30
    LEVEL_ERROR = 40
    LEVEL_CRITICAL = 50

    def __init__(self, module, message_callback):
        self._logger = logging.getLogger(module)
        self._message = message_callback

    def log(self, message, level=LEVEL_DEBUG, **kwargs):
        kwargs['message'] = message
        kwargs['level'] = level
        entry = self._message(kwargs)()
        self._logger.log(msg=entry, level=level)

    @staticmethod
    def default_message(params):
        @TimeLogDecorator(params)
        @LevelLogDecorator(params)
        @MessageLogDecorator(params)
        def message():
            return '%level%%time% %message%'
        return message
