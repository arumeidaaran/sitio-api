from http import HTTPStatus

from flask import current_app

from schemas.responses import (
    InternalServerErrorResponse,
    NotFoundResponse,
    StatusResponse,
)


def not_found(
    error,
) -> tuple[dict[str, object], HTTPStatus]:
    response = StatusResponse(
        status='',
        status_code=0,
        message='',
        data=None,
    )

    try:
        response = NotFoundResponse()
    except Exception:
        if response.status_code == 0:
            current_app.logger.exception(
                'Error inesperado al tratar un recurso no encontrado.',
            )
            response = InternalServerErrorResponse()

    return response.model_dump(mode='json'), response.status_code


def internal_server_error(
    error,
) -> tuple[dict[str, object], HTTPStatus]:
    response = StatusResponse(
        status='',
        status_code=0,
        message='',
        data=None,
    )

    try:
        response = InternalServerErrorResponse()
    except Exception:
        if response.status_code == 0:
            current_app.logger.exception(
                'Error inesperado al construir la respuesta interna.',
            )
            response = StatusResponse(
                status='internal_server_error',
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                message='Error interno del servidor.',
                data=None,
            )

    return response.model_dump(mode='json'), response.status_code
