from http import HTTPStatus

from flask_openapi import APIBlueprint

from schemas.responses import (
    InternalServerErrorResponse,
    NotFoundResponse,
    OkResponse,
)

health_blueprint = APIBlueprint('health', __name__)


@health_blueprint.get(
    '/health',
    responses={
        HTTPStatus.OK.value: OkResponse,
        HTTPStatus.NOT_FOUND.value: NotFoundResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR.value: InternalServerErrorResponse,
    },
    validate_response=True,
)
def health():
    response = OkResponse(
        status='ok',
        message='API disponible.',
    )

    return response.model_dump(mode='json'), HTTPStatus.OK
