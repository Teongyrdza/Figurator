from typing import Union
from point import *
from overload import overload


class BoundingRect:
    def __init__(self, x1: Union[int, float], y1: Union[int, float], x2: Union[int, float], y2: Union[int, float]):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def width(self) -> Union[int, float]:
        return self.x2 - self.x1

    @property
    def height(self) -> Union[int, float]:
        return self.y2 - self.y1

    @property
    def cx(self) -> Union[int, float]:
        return self.x1 + (self.width / 2)

    @property
    def cy(self) -> Union[int, float]:
        return self.y1 + (self.height / 2)

    def contains(self, other):
        return (self.x1 <= other.x1 <= self.x2) and (self.y1 <= other.y1 <= self.y2) and (
                self.x1 <= other.x2 <= self.x2) and (self.y1 <= other.y2 <= self.y2)

    def chopped(self, bounds):
        x1 = self.x1 if bounds.x1 <= self.x1 <= bounds.x2 else bounds.x1
        y1 = self.y1 if bounds.y1 <= self.y1 <= bounds.y2 else bounds.y1
        x2 = self.x2 if bounds.x1 <= self.x2 <= bounds.x2 else bounds.x2
        y2 = self.y2 if bounds.y1 <= self.y2 <= bounds.y2 else bounds.y2
        return BoundingRect(x1, y1, x2, y2)

    def __lt__(self, other):
        return self.x1 < other.x1 and self.y1 < other.y1

    def __str__(self):
        return f"{self.x1}, {self.y1} to {self.x2}, {self.y2}"

    def __repr__(self):
        return f"BoundingRect({self.x1}, {self.y1}, {self.x2}, {self.y2})"

    def intersects(self, other):
        return within(self, other)


def within(co1: BoundingRect, co2: BoundingRect) -> bool:
    return within_x(co1, co2) and within_y(co1, co2)


def within_x(co1: BoundingRect, co2: BoundingRect) -> bool:
    return (co2.x1 < co1.x1 < co2.x2) or (co2.x1 < co1.x2 < co2.x2) or (co1.x1 < co2.x1 < co1.x2) or (
            co1.x1 < co2.x2 < co1.x2)


def within_y(co1: BoundingRect, co2: BoundingRect) -> bool:
    return (co2.y1 < co1.y1 < co2.y2) or (co2.y1 < co1.y2 < co2.y2) or (co1.y1 < co2.y1 < co1.y2) or (
            co1.y1 < co2.y2 < co1.y2)


@overload
def collided(co1: BoundingRect, co2: BoundingRect) -> bool:
    return collided_left(co1, co2) or collided_right(co1, co2) or collided_top(co1, co2) or collided_bottom(co1, co2)


@overload
def collided_left(co1: BoundingRect, co2: BoundingRect) -> bool:
    if within_y(co1, co2):
        if co2.x1 <= co1.x1 <= co2.x2:
            return True
    return False


@overload
def collided_right(co1: BoundingRect, co2: BoundingRect) -> bool:
    if within_y(co1, co2):
        if co2.x1 <= co1.x2 <= co2.x2:
            return True
    return False


@overload
def collided_top(co1: BoundingRect, co2: BoundingRect) -> bool:
    if within_x(co1, co2):
        if co2.y1 <= co1.y1 <= co2.y2:
            return True
    return False


@overload
def collided_bottom(co1: BoundingRect, co2: BoundingRect) -> bool:
    if within_x(co1, co2):
        if co2.y1 <= co1.y2 <= co2.y2:
            return True
    return False
