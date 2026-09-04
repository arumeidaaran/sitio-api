from http import HTTPStatus
from pathlib import Path

from flask import current_app
from flask_openapi import APIBlueprint

from schemas.profile import (
    ProfileConfig,
    ProfileData,
    ProfilePath,
    ProfileResponse,
)
from schemas.responses import (
    InternalServerErrorResponse,
    NotFoundResponse,
    OkResponse,
    StatusResponse,
)
from utils.utils import read_json_file

profile_blueprint = APIBlueprint('profile', __name__)
ALLOWED_LANGS = ('es-co', 'pt-br', 'en-us', 'ja-jp')


@profile_blueprint.get(
    '/<string:lang>/profile/',
    responses={
        HTTPStatus.OK.value: ProfileResponse,
        HTTPStatus.NOT_FOUND.value: NotFoundResponse,
        HTTPStatus.INTERNAL_SERVER_ERROR.value: InternalServerErrorResponse,
    },
    validate_response=True,
)
def profile(
    path: ProfilePath,
) -> tuple[dict[str, object], HTTPStatus]:
    response = StatusResponse(
        status='',
        status_code=0,
        message='',
        data=None,
    )

    try:
        lang_path = str(path.lang).lower()

        if lang_path not in ALLOWED_LANGS:
            response = NotFoundResponse(
                message='Idioma no localizado.',
            )

            raise ValueError(response.message)

        profile_config_file_path = current_app.config['PROFILE_CONFIG_FILE']
        profile_config_file = Path(profile_config_file_path).absolute()

        if not profile_config_file.exists():
            response = InternalServerErrorResponse(
                message=(
                    'Camino del archivo de configuración '
                    'de perfil no encontrado.'
                ),
            )

            raise RuntimeError(response.message)

        profile_config_file_content = ProfileConfig.model_validate(
            read_json_file(profile_config_file),
        )
        profile = [
            perfil
            for perfil in profile_config_file_content.perfiles
            if lang_path == perfil.idioma.lower()
        ]

        if profile == []:
            response = InternalServerErrorResponse(
                message=(
                    'El idioma solicitado no está configurado en el perfil.'
                ),
            )

            raise RuntimeError(response.message)

        response = ProfileResponse(
            message='Idioma encontrado.',
            data=ProfileData(
                perfil=profile[0],
                contactos=profile_config_file_content.contactos,
            ).model_dump(mode='json'),
        )
    except Exception:
        if response.status_code == 0:
            current_app.logger.exception(
                'Error inesperado al consultar el perfil.',
            )
            response = InternalServerErrorResponse()

    return response.model_dump(mode='json'), response.status_code
