from typing import Literal

from pydantic import BaseModel


class Shape(BaseModel):
    type: Literal["shape"] = "shape"
    x: float
    y: float


class Circle(Shape):
    type: Literal["circle"] = "circle"
    radius: float


class Hexagon(Shape):
    type: Literal["hexagon"] = "hexagon"
    radius: float


class Rectangle(Shape):
    type: Literal["rectangle"] = "rectangle"
    width: float
    height: float


class Container(BaseModel):
    shapes: list[Circle | Hexagon | Rectangle]


my_data = {
    "shapes": [
        {"type": "circle", "x": 0, "y": 0, "radius": 1},
        {"type": "hexagon", "x": 1, "y": 2, "radius": 1},
        {"type": "rectangle", "x": 5, "y": 3, "width": 1, "height": 1},
    ]
}

cont = Container.model_validate(my_data)
print(cont)
