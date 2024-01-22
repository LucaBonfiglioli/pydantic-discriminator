from __future__ import annotations

from typing import Callable

import pydantic as pyd
from packaging.version import parse
from pydantic import BaseModel
from pytest import fixture


@fixture(scope="session")
def parse_fn() -> Callable[[type[BaseModel]], BaseModel]:
    if parse(pyd.__version__).major < 2:
        return lambda x: x.parse_obj  # type: ignore
    elif parse(pyd.__version__).major < 3:
        return lambda x: x.model_validate  # type: ignore
    raise NotImplementedError("pydantic version not supported")


@fixture(scope="session")
def dump_fn() -> Callable[[BaseModel], dict]:
    if parse(pyd.__version__).major < 2:
        return lambda x: x.dict  # type: ignore
    elif parse(pyd.__version__).major < 3:
        return lambda x: x.model_dump  # type: ignore
    raise NotImplementedError("pydantic version not supported")
