from abc import ABC,abstractmethod
class Target(ABC):
    @abstractmethod
    def send(self,prompt:str,context:dict |None=None) -> str:
        raise NotImplementedError
