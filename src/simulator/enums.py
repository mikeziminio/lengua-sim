from enum import Enum, auto

__all__ = [
    "SimulatorMode",
    "SimulatorCommand",
]


class SimulatorMode(Enum):
    CORRECT = "c"
    CORRECT_WITH_NATIVE = "cn"
    CORRECT_AND_ANSWER = "ca"
    CORRECT_AND_ANSWER_WITH_NATIVE = "can"
    ANSWER = "a"
    ANSWER_WITH_NATIVE = "an"
    TO_NATIVE = "n"


class SimulatorCommand(Enum):
    EXIT = "exit"
    OUTPUT_HELP = "help"
    OUTPUT_PARAMS = "params"
    CHANGE_TARGET_LANGUAGE = "target"
    CHANGE_NATIVE_LANGUAGE = "native"
    CHANGE_PARTNER = "partner"
