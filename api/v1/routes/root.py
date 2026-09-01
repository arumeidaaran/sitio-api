from http import HTTPStatus

from flask_openapi import APIBlueprint

from schemas.responses import (
    InternalServerErrorResponse,
    NotFoundResponse,
    OkResponse,
)


api_v1_blueprint = APIBlueprint('root', __name__)


@api_v1_blueprint.get(
    '/',
    responses={
        HTTPStatus.OK.value: OkResponse,
        HTTPStatus.NOT_FOUND.value: NotFoundResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR.value: InternalServerErrorResponse,
    },
    validate_response=True,
)
def root():
    response = OkResponse(
        status='ok',
        message='API disponible.',
    )

    return response.model_dump(mode='json'), HTTPStatus.OK
