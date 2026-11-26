from abc import ABC, abstractmethod

from .Types import DataType


class DataReader(ABC):
    @abstractmethod
    def read(self, path: str) -> DataType:
        """Read student grades from the given file."""
