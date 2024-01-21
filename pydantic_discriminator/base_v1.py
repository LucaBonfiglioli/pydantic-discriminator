from typing import Any, TypeVar

from pydantic import BaseModel, Field, root_validator
from pydantic.main import ModelMetaclass

from pydantic_discriminator.common import DiscriminatedBase, Naming


class DiscriminatedMeta(ModelMetaclass):
    def __new__(cls, name, bases, namespace, **kwargs):
        discriminator = kwargs.pop(Naming.DISCRIMINATOR_KWARG, name.lower())
        new_cls = super().__new__(cls, name, bases, namespace, **kwargs)
        setattr(new_cls, Naming.REGISTRY, {})
        setattr(new_cls, Naming.DISCRIMINATOR, discriminator)
        for base in bases:
            if hasattr(base, Naming.REGISTRY):
                getattr(base, Naming.REGISTRY)[discriminator] = new_cls
        return new_cls


_T = TypeVar("_T", bound="DiscriminatedBaseModel")


class DiscriminatedBaseModel(
    BaseModel, DiscriminatedBase[BaseModel], metaclass=DiscriminatedMeta
):
    type_: str = Field(alias=Naming.TYPE_FIELD_ALIAS, description="The type of model.")

    def __new__(cls: type[_T], *args, **kwargs) -> _T:
        if Naming.TYPE_FIELD_ALIAS not in kwargs:
            kwargs[Naming.TYPE_FIELD_ALIAS] = cls.discriminator()
        type_ = kwargs[Naming.TYPE_FIELD_ALIAS]
        if cls.discriminator() == type_:
            return super().__new__(cls)  # type: ignore
        registry = cls.get_registry_recur()
        if kwargs[Naming.TYPE_FIELD_ALIAS] not in registry:
            raise ValueError(
                f"Unknown discriminator {kwargs[Naming.TYPE_FIELD_ALIAS]} for {cls}"
            )
        other_cls = registry[kwargs[Naming.TYPE_FIELD_ALIAS]]
        return other_cls.__new__(other_cls, *args, **kwargs)  # type: ignore

    def dict(self, *args, **kwargs) -> dict:
        super_dict = super().dict(*args, **kwargs)
        super_dict[Naming.TYPE_FIELD_ALIAS] = super_dict.pop(Naming.TYPE_FIELD_NAME)
        return super_dict

    @root_validator(pre=True)
    def _validate_type_field(cls, v):
        if Naming.TYPE_FIELD_NAME in v:
            v[Naming.TYPE_FIELD_ALIAS] = v.pop(Naming.TYPE_FIELD_NAME)
        if Naming.TYPE_FIELD_ALIAS not in v:
            v[Naming.TYPE_FIELD_ALIAS] = cls.discriminator()
        return v

    @classmethod
    def parse_obj(cls: type[_T], obj: Any) -> _T:
        obj = cls._enforce_dict_if_root(obj)
        if not isinstance(obj, dict):
            try:
                obj = dict(obj)
            except (TypeError, ValueError) as e:
                pass
        if isinstance(obj, dict) and Naming.TYPE_FIELD_NAME in obj:
            obj[Naming.TYPE_FIELD_ALIAS] = obj.pop(Naming.TYPE_FIELD_NAME)
        return super().parse_obj(obj)
