from pydantic import BaseModel


class Shape(BaseModel):
    x: float
    y: float


class Circle(Shape):
    radius: float


class Hexagon(Shape):
    radius: float


class Rectangle(Shape):
    width: float
    height: float


class Container(BaseModel):
    shapes: list[Shape]


my_data = {
    "shapes": [
        {"x": 0, "y": 0, "radius": 1},  # This is a Circle
        {"x": 1, "y": 2, "radius": 1},  # This is a Hexagon (WTF?)
        {"x": 5, "y": 3, "width": 1, "height": 1},  # This is a Rectangle
    ]
}

cont = Container.model_validate(my_data)
print(cont)
