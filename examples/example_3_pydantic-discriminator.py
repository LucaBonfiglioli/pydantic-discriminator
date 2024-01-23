from pydantic import BaseModel

from pydantic_discriminator import DiscriminatedBaseModel


class Shape(DiscriminatedBaseModel):
    x: float
    y: float


class Circle(Shape, discriminator="circle"):
    radius: float


class Hexagon(Shape, discriminator="hexagon"):
    radius: float


class Rectangle(Shape, discriminator="rectangle"):
    width: float
    height: float


class Container(BaseModel):
    shapes: list[Shape]


my_data = {
    "shapes": [
        {"type": "circle", "x": 0, "y": 0, "radius": 1},
        {"type": "hexagon", "x": 1, "y": 2, "radius": 1},
        {"type": "rectangle", "x": 5, "y": 3, "width": 1, "height": 1},
    ]
}

cont = Container.model_validate(my_data)
print(cont)
