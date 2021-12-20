from abc import ABC, abstractmethod
from typing import Union, Literal


class Validator(ABC):
    @abstractmethod
    async def __call__(
        self,
        data: Union[list, dict],
        source: Literal["body", "query_params", "path_params"] = "body",
        response: bool = False,
        partial: bool = False,
    ) -> dict:
        ...
