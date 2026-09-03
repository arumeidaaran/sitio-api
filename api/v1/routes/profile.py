from http import HTTPStatus

from flask import current_app
from flask_openapi import APIBlueprint

from schemas.profile import ProfilePath
from schemas.responses import (
    InternalServerErrorResponse,
    NotFoundResponse,
    OkResponse,
    StatusResponse,
)

idioma_profile_blueprint = APIBlueprint('profile', __name__)
IDIOMAS_PERMITIDOS = ('es-CO', 'pt-BR', 'en-US', 'ja-JP')


@idioma_profile_blueprint.get(
    '/<string:idioma>/profile/',
    responses={
        HTTPStatus.OK.value: OkResponse,
        HTTPStatus.NOT_FOUND.value: NotFoundResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR.value: InternalServerErrorResponse,
    },
    validate_response=True,
)
def idioma_profile(
    path: ProfilePath,
) -> tuple[dict[str, object], HTTPStatus]:
    response = StatusResponse(
        status='',
        status_code=0,
        message='',
        data=None,
    )

    try:
        if path.idioma not in IDIOMAS_PERMITIDOS:
            response = NotFoundResponse(
                message='Idioma no localizado.',
            )

            raise ValueError(response.message)

        response = OkResponse(
            message='Idioma encontrado.',
        )
    except Exception:
        if response.status_code == 0:
            current_app.logger.exception(
                'Error inesperado al consultar el perfil.',
            )
            response = InternalServerErrorResponse()

    return response.model_dump(mode='json'), response.status_code
