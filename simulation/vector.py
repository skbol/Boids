from math import sqrt
from typing import Union, Tuple

Number = Union[int, float]

class BaseVector:
    def __init__(self, *components: Number):
        self.coords = tuple(components)

    def __repr__(self):
        return f"{self.__class__.__name__}{self.coords}"

    def __add__(self, other: "BaseVector") -> "BaseVector":
        return self.__class__(*(a + b for a, b in zip(self.coords, other.coords)))

    def __sub__(self, other: "BaseVector") -> "BaseVector":
        return self.__class__(*(a - b for a, b in zip(self.coords, other.coords)))

    def __mul__(self, scalar: Number) -> "BaseVector":
        return self.__class__(*(a * scalar for a in self.coords))

    def __truediv__(self, scalar: Number) -> "BaseVector":
        return self.__class__(*(a / scalar for a in self.coords))

    def __neg__(self) -> "BaseVector":
        return self.__class__(*(-a for a in self.coords))

    def magnitude(self) -> float:
        return sqrt(sum(a * a for a in self.coords))

    def normalize(self) -> "BaseVector":
        mag = self.magnitude()
        if mag == 0:
            return self.__class__(*([0] * len(self.coords)))
        return self / mag

    def distance_to(self, other: "BaseVector") -> float:
        return (self - other).magnitude()


class Vector2D(BaseVector):
    def __init__(self, x: Number, y: Number):
        super().__init__(x, y)

    @property
    def x(self) -> Number:
        return self.coords[0]
    
    @x.setter
    def x(self, value: Number):
        self.coords = (value, self.coords[1])
    
    @property
    def y(self) -> Number:
        return self.coords[1]
    
    @y.setter
    def y(self, value: Number):
        self.coords = (self.coords[0], value)
    
    @classmethod
    def zero(cls):
        return cls(0.0, 0.0)
