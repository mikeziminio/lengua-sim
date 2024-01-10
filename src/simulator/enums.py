from enum import Enum, auto

__all__ = [
    "SimulatorMode",
    "SimulatorCommand",
]


class SimulatorMode(Enum):
    RAW = auto()
    CORRECT = auto()
    CORRECT_WITH_NATIVE = auto()              # with native language
    CORRECT_AND_ANSWER = auto()
    CORRECT_AND_ANSWER_WITH_NATIVE = auto()   # with native language


class SimulatorCommand(Enum):
    EXIT = auto()
