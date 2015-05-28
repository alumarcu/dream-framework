class SimulationError(Exception):
    pass

class InitError(SimulationError):
    pass

class LoopError(SimulationError):
    pass
