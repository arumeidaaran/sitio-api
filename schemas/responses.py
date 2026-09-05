from http import HTTPStatus
from typing import Literal

from pydantic import ConfigDict, Field

from schemas.base import ApiModel


class StatusResponse(ApiModel):
    model_config = ConfigDict(frozen=True)

    status: str
    status_code: int
    message: str
    data: dict[str, object] | None


class OkResponse(StatusResponse):
    status: Literal['ok'] = 'ok'
    status_code: Literal[HTTPStatus.OK] = HTTPStatus.OK
    message: str
    data: dict[str, object] = Field(default_factory=dict)


class NotFoundResponse(StatusResponse):
    status: Literal['not_found'] = 'not_found'
    status_code: Literal[HTTPStatus.NOT_FOUND] = HTTPStatus.NOT_FOUND
    message: str = 'Recurso no encontrado.'
    data: None = None


class InternalServerErrorResponse(StatusResponse):
    status: Literal['internal_server_error'] = 'internal_server_error'
    status_code: Literal[HTTPStatus.INTERNAL_SERVER_ERROR] = (
        HTTPStatus.INTERNAL_SERVER_ERROR
    )
    message: str = 'Error interno del servidor.'
    data: None = None
