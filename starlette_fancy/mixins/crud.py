from starlette.requests import Request
from starlette.responses import Response

from starlette_fancy.processors import Processor
from starlette_fancy.validators import Validator

try:
    from starlette_marshal import json
except ImportError:
    import json

try:
    from starlette_marshal import JSONResponse
except ImportError:
    from starlette.responses import JSONResponse


class CreateMixin(object):
    validator: Validator
    processor: Processor

    async def post(self, request: Request) -> Response:
        body: dict = json.loads(s=await request.body())
        query_params: dict = dict(request.query_params)

        validated_body: dict = await self.validator(
            data=body,
        )
        validated_params: dict = await self.validator(
            data=query_params,
            source="query_params",
        )
        processed_data: dict = await self.processor.post(
            validated_data=validated_body | validated_params,
        )

        return JSONResponse(content=processed_data)


class ReadMixin(object):
    validator: Validator
    processor: Processor

    async def get(self, request: Request) -> Response:
        query_params: dict = dict(request.query_params)

        validated_data: dict = await self.validator(
            data=query_params,
            source="query_params",
        )
        processed_data: list = await self.processor.get(
            validated_data=validated_data,
        )

        return JSONResponse(content=processed_data)


class UpdateMixin(object):
    validator: Validator
    processor: Processor

    async def patch(self, request: Request) -> Response:
        body: dict = json.loads(s=await request.body())

        validated_data: dict = await self.validator(
            data=body,
        )
        processed_data: dict = await self.processor.patch(
            validated_data=validated_data | request.path_params,
        )

        return JSONResponse(content=processed_data)


class DeleteMixin(object):
    processor: Processor

    async def delete(self, request: Request) -> Response:
        await self.processor.delete(
            validated_data=request.path_params,
        )

        return Response(status_code=204)
