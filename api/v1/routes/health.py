from http import HTTPStatus

from flask import current_app
from flask_openapi import APIBlueprint

from schemas.responses import (
    InternalServerErrorResponse,
    NotFoundResponse,
    OkResponse,
    StatusResponse,
)

health_blueprint = APIBlueprint('health', __name__)


@health_blueprint.get(
    '/health/',
    responses={
        HTTPStatus.OK.value: OkResponse,
        HTTPStatus.NOT_FOUND.value: NotFoundResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR.value: InternalServerErrorResponse,
    },
    validate_response=True,
)
def health() -> tuple[dict[str, object], HTTPStatus]:
    response = StatusResponse(
        status='',
        status_code=0,
        message='',
        data=None,
    )

    try:
        response = OkResponse(
            message='API disponible.',
        )
    except Exception:
        current_app.logger.exception(
            'Error inesperado al consultar la salud de la API.',
        )
        response = InternalServerErrorResponse()

    return response.model_dump(mode='json'), response.status_code
