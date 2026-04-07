from abc import ABC, abstractmethod

class BaseChannel(ABC):

    @abstractmethod
    async def send(self, recipient: str, message: str):
        pass