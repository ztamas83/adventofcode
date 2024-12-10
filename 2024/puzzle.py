import os
from typing import Any
from aocd import get_data, submit
from abc import ABC, abstractmethod

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Puzzle:
    def __init__(self, year: int, day: int) -> None:
        self._day = day
        self._year = year
        self._data: str = []

    @abstractmethod
    def solve_a(self) -> Any:
        pass

    @abstractmethod
    def solve_b(self) -> Any:
        pass

    @abstractmethod
    def solve(self) -> tuple[Any, Any]:
        return (self.solve_a(), self.solve_b())

    def submit(self, sub_a=True, sub_b=True):
        self.init_data(True)
        (a, b) = self.solve()
        if sub_a:
            submit(a, day=self._day, year=self._year, part="a")
        if sub_b:
            submit(b, day=self._day, year=self._year, part="b")

    def init_data(self, remote: bool = False):
        """Return daily puzzle input"""
        if remote:
            self._data = get_data(day=self._day, year=self._year)
        else:
            with open(
                os.path.join(__location__, f"input_{self._year}_{self._day}.txt"), "r"
            ) as f:
                lines = f.read()
                self._data = lines
