from __future__ import annotations

import pytest
from deepdiff import DeepDiff

# This import is necessary for the test to pass.
from pydantic import BaseModel

from pydantic_discriminator import DiscriminatedBaseModel


class Shape(DiscriminatedBaseModel):
    position: tuple[float, float]


class Circle(Shape, discriminator="circle"):
    radius: float


class Square(Shape, discriminator="square"):
    side: float


class Rectangle(Shape, discriminator="rectangle"):
    width: float
    height: float


class Animal(DiscriminatedBaseModel):
    name: str
    age: int


class Mammal(Animal, discriminator="mammal"):
    pass


class Reptile(Animal, discriminator="reptile"):
    pass


class Bird(Animal, discriminator="bird"):
    pass


class Cat(Mammal, discriminator="cat"):
    color: str
    meow_pitch: float
    purrosity: float


class Dog(Mammal, discriminator="dog"):
    color: str
    bark_pitch: float
    size: float


class Snake(Reptile, discriminator="snake"):
    length: float
    killcount: int


class Lizard(Reptile, discriminator="lizard"):
    length: float
    tails_lost: int


class Eagle(Bird, discriminator="eagle"):
    wingspan: float
    divespeed: float


class Penguin(Bird, discriminator="penguin"):
    wingspan: float
    waddlespeed: float
    fatness: float


@pytest.mark.parametrize(
    ["code", "dict_data"],
    [
        [
            """
expected = Cat(name="Mittens", age=5, color="black", meow_pitch=0.5, purrosity=0.9)
            """,
            {
                "type": "cat",
                "name": "Mittens",
                "age": 5,
                "color": "black",
                "meow_pitch": 0.5,
                "purrosity": 0.9,
            },
        ],
        [
            """
class Client(BaseModel):
    an_animal: Animal

expected = Client(an_animal=Cat(name="Mittens", age=5, color="black", meow_pitch=0.5, purrosity=0.9))
            """,
            {
                "an_animal": {
                    "type": "cat",
                    "name": "Mittens",
                    "age": 5,
                    "color": "black",
                    "meow_pitch": 0.5,
                    "purrosity": 0.9,
                }
            },
        ],
        [
            """
class Client(BaseModel):
    many_animals: list[Animal]

expected = Client(
    many_animals=[
        Cat(name="Mittens", age=5, color="black", meow_pitch=0.5, purrosity=0.9),
        Dog(name="Fido", age=3, color="brown", bark_pitch=0.4, size=0.8),
        Cat(name="Mittens", age=5, color="black", meow_pitch=0.5, purrosity=0.9),
        Lizard(name="Lizzy", age=4, length=0.5, tails_lost=1),
    ]
)
            """,
            {
                "many_animals": [
                    {
                        "type": "cat",
                        "name": "Mittens",
                        "age": 5,
                        "color": "black",
                        "meow_pitch": 0.5,
                        "purrosity": 0.9,
                    },
                    {
                        "type": "dog",
                        "name": "Fido",
                        "age": 3,
                        "color": "brown",
                        "bark_pitch": 0.4,
                        "size": 0.8,
                    },
                    {
                        "type": "cat",
                        "name": "Mittens",
                        "age": 5,
                        "color": "black",
                        "meow_pitch": 0.5,
                        "purrosity": 0.9,
                    },
                    {
                        "type": "lizard",
                        "name": "Lizzy",
                        "age": 4,
                        "length": 0.5,
                        "tails_lost": 1,
                    },
                ]
            },
        ],
        [
            """
class Client(BaseModel):
    many_animals: tuple[Animal, ...]

expected = Client(
    many_animals=(
        Cat(name="Mittens", age=5, color="black", meow_pitch=0.5, purrosity=0.9),
        Dog(name="Fido", age=3, color="brown", bark_pitch=0.4, size=0.8),
        Cat(name="Mittens", age=5, color="black", meow_pitch=0.5, purrosity=0.9),
        Lizard(name="Lizzy", age=4, length=0.5, tails_lost=1),
    )
)
            """,
            {
                "many_animals": (
                    {
                        "type": "cat",
                        "name": "Mittens",
                        "age": 5,
                        "color": "black",
                        "meow_pitch": 0.5,
                        "purrosity": 0.9,
                    },
                    {
                        "type": "dog",
                        "name": "Fido",
                        "age": 3,
                        "color": "brown",
                        "bark_pitch": 0.4,
                        "size": 0.8,
                    },
                    {
                        "type": "cat",
                        "name": "Mittens",
                        "age": 5,
                        "color": "black",
                        "meow_pitch": 0.5,
                        "purrosity": 0.9,
                    },
                    {
                        "type": "lizard",
                        "name": "Lizzy",
                        "age": 4,
                        "length": 0.5,
                        "tails_lost": 1,
                    },
                )
            },
        ],
        [
            """
class Client(BaseModel):
    many_animals: dict[str, Animal]

expected = Client(
    many_animals={
        "mittens": Cat(name="Mittens", age=5, color="black", meow_pitch=0.5, purrosity=0.9),
        "fido": Dog(name="Fido", age=3, color="brown", bark_pitch=0.4, size=0.8),
        "mittens2": Cat(name="Mittens", age=5, color="black", meow_pitch=0.5, purrosity=0.9),
        "lizzy": Lizard(name="Lizzy", age=4, length=0.5, tails_lost=1),
    }
)
            """,
            {
                "many_animals": {
                    "mittens": {
                        "type": "cat",
                        "name": "Mittens",
                        "age": 5,
                        "color": "black",
                        "meow_pitch": 0.5,
                        "purrosity": 0.9,
                    },
                    "fido": {
                        "type": "dog",
                        "name": "Fido",
                        "age": 3,
                        "color": "brown",
                        "bark_pitch": 0.4,
                        "size": 0.8,
                    },
                    "mittens2": {
                        "type": "cat",
                        "name": "Mittens",
                        "age": 5,
                        "color": "black",
                        "meow_pitch": 0.5,
                        "purrosity": 0.9,
                    },
                    "lizzy": {
                        "type": "lizard",
                        "name": "Lizzy",
                        "age": 4,
                        "length": 0.5,
                        "tails_lost": 1,
                    },
                }
            },
        ],
        [
            """
class Client(BaseModel):
    a_cat: Cat
    an_animal: Animal
    many_animals: list[Animal]

    a_circle: Circle
    a_shape: Shape
    many_shapes: list[Shape]

expected = Client(
    a_cat=Cat(
        name="Mittens",
        age=5,
        color="black",
        meow_pitch=0.5,
        purrosity=0.9,
        position=(0.0, 0.0),
    ),
    an_animal=Dog(
        name="Fido",
        age=3,
        color="brown",
        bark_pitch=0.4,
        size=0.8,
        position=(0.0, 0.0),
    ),
    many_animals=[
        Snake(
            name="Slither",
            age=1,
            length=1.2,
            killcount=0,
            position=(0.0, 0.0),
        ),
        Eagle(
            name="Swoop",
            age=2,
            wingspan=1.5,
            divespeed=0.6,
            position=(0.0, 0.0),
        ),
    ],
    a_circle=Circle(position=(0.0, 0.0), radius=1.0),
    a_shape=Rectangle(position=(1.0, 1.0), width=2.0, height=3.0),
    many_shapes=[
        Circle(position=(0.0, 0.0), radius=1.0),
        Square(position=(1.0, 1.0), side=2.0),
        Rectangle(position=(2.0, 2.0), width=3.0, height=4.0),
    ],
)
            """,
            {
                "a_cat": {
                    "type": "cat",
                    "name": "Mittens",
                    "age": 5,
                    "color": "black",
                    "meow_pitch": 0.5,
                    "purrosity": 0.9,
                },
                "an_animal": {
                    "type": "dog",
                    "name": "Fido",
                    "age": 3,
                    "color": "brown",
                    "bark_pitch": 0.4,
                    "size": 0.8,
                },
                "many_animals": [
                    {
                        "type": "snake",
                        "name": "Slither",
                        "age": 1,
                        "length": 1.2,
                        "killcount": 0,
                    },
                    {
                        "type": "eagle",
                        "name": "Swoop",
                        "age": 2,
                        "wingspan": 1.5,
                        "divespeed": 0.6,
                    },
                ],
                "a_circle": {"type": "circle", "position": (0.0, 0.0), "radius": 1.0},
                "a_shape": {
                    "type": "rectangle",
                    "position": (1.0, 1.0),
                    "width": 2.0,
                    "height": 3.0,
                },
                "many_shapes": [
                    {"type": "circle", "position": (0.0, 0.0), "radius": 1.0},
                    {"type": "square", "position": (1.0, 1.0), "side": 2.0},
                    {
                        "type": "rectangle",
                        "position": (2.0, 2.0),
                        "width": 3.0,
                        "height": 4.0,
                    },
                ],
            },
        ],
        [
            """
class Client(BaseModel):
    very_deep: list[tuple[dict[str, list[Shape]], ...]]

expected = Client(
    very_deep=[
        (
            {
                "shapes": [
                    Circle(position=(0.0, 0.0), radius=1.0),
                    Square(position=(1.0, 1.0), side=2.0),
                ]
            },
        ),
    ]
)   
            """,
            {
                "very_deep": [
                    (
                        {
                            "shapes": [
                                {
                                    "type": "circle",
                                    "position": (0.0, 0.0),
                                    "radius": 1.0,
                                },
                                {"type": "square", "position": (1.0, 1.0), "side": 2.0},
                            ]
                        },
                    ),
                ]
            },
        ],
    ],
)
def test_discriminated_base_model(parse_fn, dump_fn, code, dict_data):
    exec(code)
    client_cls = locals()["expected"].__class__
    example = parse_fn(client_cls)(dict_data)
    assert example == locals()["expected"]
    assert not DeepDiff(dump_fn(example)(), dict_data, ignore_order=True)


def test_fail_unknown_discriminator():
    with pytest.raises(ValueError):
        Shape(type="triangle", position=(0.0, 0.0))


def test_fail_wrong_discriminator():
    with pytest.raises(ValueError):
        Circle(type="rectangle", position=(0.0, 0.0), radius=1.0)


def test_typefield_in_parse(parse_fn):
    circle = parse_fn(Shape)({"type_": "circle", "position": (0.0, 0.0), "radius": 1.0})
    assert isinstance(circle, Circle)


def test_typefield_in_constructor():
    circle = Circle(type_="circle", position=(0.0, 0.0), radius=1.0)
    assert isinstance(circle, Circle)


def test_alias_in_parse(parse_fn):
    circle = parse_fn(Shape)({"type": "circle", "position": (0.0, 0.0), "radius": 1.0})
    assert isinstance(circle, Circle)


def test_alias_in_constructor():
    circle = Circle(type="circle", position=(0.0, 0.0), radius=1.0)
    assert isinstance(circle, Circle)


def test_parse_invalid_stuff(parse_fn):
    with pytest.raises((ValueError, TypeError)):
        parse_fn(Circle)(1)
