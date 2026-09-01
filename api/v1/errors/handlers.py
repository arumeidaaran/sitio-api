from http import HTTPStatus

from schemas.responses import (
    InternalServerErrorResponse,
    NotFoundResponse,
)


def not_found(error):
    response = NotFoundResponse(
        error='not_found',
        message='Recurso no encontrado.',
    )

    return response.model_dump(mode='json'), HTTPStatus.NOT_FOUND


def internal_server_error(error):
    response = InternalServerErrorResponse(
        error='internal_server_error',
        message='Error interno del servidor.',
    )

    return response.model_dump(mode='json'), HTTPStatus.INTERNAL_SERVER_ERROR
