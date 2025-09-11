from abc import ABC, abstractmethod
from typing import TypeVar

Raw = TypeVar("Raw")
Parsed = TypeVar("Parsed")


class FSBase[Raw, Parsed](ABC):
    @abstractmethod
    def write(self, data: Raw, dest: str): ...

    @abstractmethod
    def read(self, src: str) -> Parsed: ...
