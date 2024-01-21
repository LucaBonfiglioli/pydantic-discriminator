import pydantic as pyd
from packaging.version import parse

if parse(pyd.__version__).major < 2:
    from pydantic_discriminator.base_v1 import DiscriminatedBaseModel
elif parse(pyd.__version__).major < 3:
    from pydantic_discriminator.base_v2 import DiscriminatedBaseModel
else:
    raise NotImplementedError(
        f"pydantic-discriminator does not support pydantic {pyd.__version__}"
    )
