from enum import Enum, auto
import asyncio
import dotenv

dotenv.load_dotenv("../.env")


class SimulatorMode(Enum):
    RAW = auto()
    CORRECT_ME = auto()
    CORRECT_ME_AND_ANSWER = auto()


class Simulator:

    target_language: str
    native_language: str
    mode: SimulatorMode

    def __init__(self, target_language: str, native_language: str, mode: SimulatorMode):
        self.target_language = target_language
        self.native_language = native_language
        self.mode = mode

    def process_request(self, request: str, mode: SimulatorMode = SimulatorMode.RAW):
        match mode:
            case SimulatorMode.RAW:
                return request
            case SimulatorMode.CORRECT_ME:
                result = (f"Correct the phrase in {self.target_language} language: \"{request}\". " +
                          f"In the response, just write the corrected phrase on {self.target_language}")
                return result
            case _:
                raise Exception("Неизвестный режим")
                # TODO: добавить исключение
