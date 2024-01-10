from abc import ABC, abstractmethod
from simulator import SimulatorMode


class AbstractIOInterface(ABC):

    @abstractmethod
    async def input(self) -> str | SimulatorMode: ...

    @abstractmethod
    async def text_output(self, content: str) -> None: ...
