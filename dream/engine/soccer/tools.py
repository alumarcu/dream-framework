from dream.tools import LoggerBaseDecorator, TimeLogDecorator, \
    LevelLogDecorator, MessageLogDecorator


def engine_params(section=None, key=None):
    """
    Returns a parameter or a section of engine parameters
    """
    if engine_params.cache is None:
        from dream.engine.soccer.models import EngineParam
        engine_params.cache = EngineParam.objects.all()

    # Return a section
    if section is not None:
        params = [ep for ep in engine_params.cache if ep.section == section]
        return {p.key: p.value for p in params}

    # Return a single parameter
    elif key is not None:
        params = [ep for ep in engine_params.cache if ep.key == key]
        if len(params) == 1:
            return params[0]
        else:
            return params
    else:
        return engine_params.cache

# A cache with all parameters defined in that table
engine_params.cache = None


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
