from abc import ABC, abstractmethod



class CopyAbstract(ABC):
    @abstractmethod
    def copy(self) -> 'CopyAbstract':
        pass

    @abstractmethod
    def __copy__(self) -> 'CopyAbstract':
        pass

    @abstractmethod
    def __deepcopy__(self, memo={}) -> 'CopyAbstract':
        pass
