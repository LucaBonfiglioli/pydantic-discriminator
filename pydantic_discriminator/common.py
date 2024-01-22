from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping, MutableMapping
from typing import Generic, TypeVar


class Naming:
    REGISTRY: str = "__pyd_discriminator_registry__"
    DISCRIMINATOR: str = "__pyd_discriminator_field__"
    DISCRIMINATOR_KWARG: str = "discriminator"
    TYPE_FIELD_NAME: str = "type_"
    TYPE_FIELD_ALIAS: str = "type"


T = TypeVar("T")


class Discriminated(ABC, Generic[T]):
    @classmethod
    @abstractmethod
    def discriminator(cls) -> str:
        ...

    @classmethod
    @abstractmethod
    def get_registry(cls) -> MutableMapping[str, type[T]]:
        ...

    @classmethod
    @abstractmethod
    def get_registry_recur(cls) -> Mapping[str, type[T]]:
        ...


class DiscriminatedBase(Discriminated[T]):
    @classmethod
    def discriminator(cls) -> str:
        return getattr(cls, Naming.DISCRIMINATOR)

    @classmethod
    def get_registry(cls) -> MutableMapping[str, type[T]]:
        return getattr(cls, Naming.REGISTRY)

    @classmethod
    def get_registry_recur(cls) -> Mapping[str, type[T]]:
        all_registered = {}
        for k, registered in cls.get_registry().items():
            all_registered[k] = registered
            if issubclass(registered, Discriminated):  # pragma: no branch
                all_registered.update(registered.get_registry_recur())
        return all_registered
