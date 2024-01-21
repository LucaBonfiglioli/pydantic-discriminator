import warnings
from collections.abc import MutableMapping
from re import S
from typing import Any, Mapping, TypeVar

from pydantic import BaseModel, Field, model_validator
from pydantic._internal._model_construction import ModelMetaclass
from pydantic_core import SchemaSerializer

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


old_to_python = SchemaSerializer.to_python


def _new_to_python(ss_self, v_self, *args, **kwargs):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = old_to_python(ss_self, v_self, *args, **kwargs)

    if isinstance(v_self, BaseModel):
        for k in v_self.model_fields.keys():
            fval = getattr(v_self, k)
            res[k] = _new_to_python(ss_self, fval, *args, **kwargs)
    if isinstance(res, dict):
        if Naming.TYPE_FIELD_NAME in res:
            res[Naming.TYPE_FIELD_ALIAS] = res.pop(Naming.TYPE_FIELD_NAME)
        for k, v in res.items():
            res[k] = _new_to_python(ss_self, v, *args, **kwargs)
    elif isinstance(res, list):
        for i, v in enumerate(res):
            res[i] = _new_to_python(ss_self, v, *args, **kwargs)
    elif isinstance(res, tuple):
        res = tuple(_new_to_python(ss_self, v, *args, **kwargs) for v in res)

    return res


if SchemaSerializer.to_python is not _new_to_python:  # pragma: no branch
    setattr(SchemaSerializer, "to_python", _new_to_python)


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

    #! If the __new__ is called in rust, the redefined __new__ will not be called.
    #! But by simply adding a no-op constructor, the __new__ will be called as expected.
    #! This technique was condemned by the old ones.
    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

    @model_validator(mode="before")
    def _validate_type_field(cls, v):
        if Naming.TYPE_FIELD_NAME in v:
            v[Naming.TYPE_FIELD_ALIAS] = v.pop(Naming.TYPE_FIELD_NAME)
        if Naming.TYPE_FIELD_ALIAS not in v:
            v[Naming.TYPE_FIELD_ALIAS] = cls.discriminator()
        return v

    @classmethod
    def model_validate(
        cls: type[_T],
        obj: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: dict[str, Any] | None = None,
    ) -> _T:
        if isinstance(obj, MutableMapping) and Naming.TYPE_FIELD_NAME in obj:
            obj[Naming.TYPE_FIELD_ALIAS] = obj.pop(Naming.TYPE_FIELD_NAME)
        return super().model_validate(
            obj, strict=strict, from_attributes=from_attributes, context=context
        )
