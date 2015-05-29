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
