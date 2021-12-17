from abc import ABC
from typing import Any


class Processor(ABC):
    async def get(self, validated_data: dict) -> Any:
        ...

    async def post(self, validated_data: dict) -> Any:
        ...

    async def put(self, validated_data: dict) -> Any:
        ...

    async def delete(self, validated_data: dict) -> Any:
        ...

    async def patch(self, validated_data: dict) -> Any:
        ...
