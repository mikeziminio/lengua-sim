from enum import Enum, auto

__all__ = [
    "SimulatorMode",
    "SimulatorCommand",
]


class SimulatorMode(Enum):
    RAW = auto()
    CORRECT = auto()
    CORRECT_WITH_NATIVE = auto()
    CORRECT_AND_ANSWER = auto()
    CORRECT_AND_ANSWER_WITH_NATIVE = auto()
    ANSWER = auto()
    ANSWER_WITH_NATIVE = auto()


class SimulatorCommand(Enum):
    EXIT = auto()
    OUTPUT_HELP = auto()
    CHANGE_TARGET_LANGUAGE = auto()
    CHANGE_NATIVE_LANGUAGE = auto()
