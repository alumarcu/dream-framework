from dream.tools import LoggerBaseDecorator, TimeLogDecorator, \
    LevelLogDecorator, MessageLogDecorator


class SimulationLogDecorator(LoggerBaseDecorator):
    def _token(self):
        return '%simtime%'

    def _replace(self):
        if 'simtime' not in self._params:
            return ''
        return '[M:%03d_T:%04d] ' % (self._params['simtime'][0], self._params['simtime'][1])


def simulation_log_message(params):
    if 'time_format' not in params:
        params['time_format'] = '%y%m%d::%H:%M:%S.%f'

    @SimulationLogDecorator(params)
    @TimeLogDecorator(params)
    @LevelLogDecorator(params)
    @MessageLogDecorator(params)
    def message():
        return '%level%%time%%simtime%%message%'
    return message
