# Import de Python
from http import HTTPStatus
from os import environ

# Import de las librerías
from flask import redirect
from flask_cors import CORS
from flask_openapi import Info, OpenAPI

# Import del proyecto
from api.v1.errors.handlers import internal_server_error, not_found
from api.v1.routes.health import health_blueprint
from api.v1.routes.profile import profile_blueprint
from api.v1.routes.root import root_blueprint


def create_app(
    profile_config_file: str | None = None,
    cors_allowed_origin: str | None = None,
) -> OpenAPI:
    api_prefix = '/api/v1'

    if profile_config_file is None:
        profile_config_file = environ.get('PROFILE_CONFIG_FILE')

    if not profile_config_file:
        raise OSError('Variable de entorno PROFILE_CONFIG_FILE no definida.')

    if cors_allowed_origin is None:
        cors_allowed_origin = environ.get('CORS_ALLOWED_ORIGIN')

    if not cors_allowed_origin:
        raise OSError(
            'Variable de entorno CORS_ALLOWED_ORIGIN no definida.',
        )

    info = Info(
        title='sitio-api',
        description='API del sitio personal.',
        version='1.0.0',
    )

    application = OpenAPI(
        __name__,
        info=info,
        doc_ui=True,
        doc_prefix=f'{api_prefix}/docs',
        doc_url='/openapi.json',
    )

    CORS(
        application,
        resources={
            r'/api/*': {
                'origins': cors_allowed_origin,
            },
        },
    )

    application.json.ensure_ascii = False
    application.config['SWAGGER_CONFIG'] = {
        'validatorUrl': None,
    }
    application.config['PROFILE_CONFIG_FILE'] = profile_config_file

    application.register_api(
        health_blueprint,
        url_prefix=api_prefix,
    )
    application.register_api(
        root_blueprint,
        url_prefix=api_prefix,
    )
    application.register_api(
        profile_blueprint,
        url_prefix=api_prefix,
    )

    application.register_error_handler(
        HTTPStatus.NOT_FOUND,
        not_found,
    )
    application.register_error_handler(
        HTTPStatus.INTERNAL_SERVER_ERROR,
        internal_server_error,
    )

    @application.get(
        f'{api_prefix}/openapi.json',
        doc_ui=False,
    )
    def openapi_document():
        return application.api_doc

    @application.get(
        '/',
        doc_ui=False,
    )
    def root():
        return redirect(f'{api_prefix}/')

    return application


app = create_app()
