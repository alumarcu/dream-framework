def engine_params(key=None, section=None):
    """
    Returns a parameter or a section of engine parameters
    """
    if engine_params.cache is None:
        from dream.core.models import EngineParam
        engine_params.cache = EngineParam.objects.all()

    # Return a single parameter by key
    if key is not None:
        params = [ep for ep in engine_params.cache if ep.key == key]
        if len(params) == 1:
            return params[0]
        else:
            raise IndexError("Cannot find engine param with key '{}'".format(key))

    # Return a whole section
    elif section is not None:
        params = [ep for ep in engine_params.cache if ep.section == section]
        return {p.key: p.value for p in params}

    else:
        return engine_params.cache

# A cache with all parameters defined in that table
engine_params.cache = None
