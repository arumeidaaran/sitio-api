from typing import Literal

from schemas.base import ApiModel


class StatusResponse(ApiModel):
    status: str
    message: str


class OkResponse(StatusResponse):
    status: Literal['ok']
    message: Literal['API disponible.']


class NotFoundResponse(StatusResponse):
    status: Literal['not_found']
    message: Literal['Recurso no encontrado.']


class InternalServerErrorResponse(StatusResponse):
    status: Literal['internal_server_error']
    message: Literal['Error interno del servidor.']
