from starlette.endpoints import HTTPEndpoint

from starlette_fancy.mixins import (
    CreateMixin,
    ReadMixin,
    UpdateMixin,
    DeleteMixin,
)


class CRUDEndpoint(
    HTTPEndpoint,
    CreateMixin,
    ReadMixin,
    UpdateMixin,
    DeleteMixin,
):
    pass
