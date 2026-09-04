from http import HTTPStatus

import pytest

from app import create_app


def test_raiz_debe_redirigir_a_raiz_de_la_version_de_api_actual(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.FOUND
    assert response.headers['Location'] == '/api/v1/'


def test_openapi_debe_retornar_documentacion(client):
    response = client.get('/api/v1/openapi.json')

    assert response.status_code == HTTPStatus.OK

    openapi = response.get_json()

    assert openapi['openapi'] == '3.1.0'
    assert openapi['info']['title'] == 'sitio-api'
    assert openapi['info']['version'] == '1.0.0'
    assert '/api/v1/' in openapi['paths']
    assert '/api/v1/health/' in openapi['paths']
    assert '/api/v1/{lang}/profile/' in openapi['paths']


def assert_openapi_response_schemas(
    openapi,
    path,
    ok_schema,
):
    responses = openapi['paths'][path]['get']['responses']

    expected_schemas = {
        '200': ok_schema,
        '404': 'NotFoundResponse',
        '500': 'InternalServerErrorResponse',
    }

    for status_code, schema in expected_schemas.items():
        response_schema = responses[status_code]['content'][
            'application/json'
        ]['schema']

        assert response_schema == {
            '$ref': f'#/components/schemas/{schema}',
        }


def test_openapi_debe_documentar_respuestas_de_root(client):
    openapi = client.get('/api/v1/openapi.json').get_json()

    assert_openapi_response_schemas(
        openapi=openapi,
        path='/api/v1/',
        ok_schema='OkResponse',
    )


def test_openapi_debe_documentar_respuestas_de_health(client):
    openapi = client.get('/api/v1/openapi.json').get_json()

    assert_openapi_response_schemas(
        openapi=openapi,
        path='/api/v1/health/',
        ok_schema='OkResponse',
    )


def test_openapi_debe_documentar_respuestas_de_profile(client):
    openapi = client.get('/api/v1/openapi.json').get_json()

    assert_openapi_response_schemas(
        openapi=openapi,
        path='/api/v1/{lang}/profile/',
        ok_schema='ProfileResponse',
    )


def test_openapi_debe_documentar_datos_de_profile(client):
    openapi = client.get('/api/v1/openapi.json').get_json()
    schemas = openapi['components']['schemas']

    assert schemas['ProfileResponse']['properties']['data'] == {
        '$ref': '#/components/schemas/ProfileData',
    }
    assert schemas['ProfileData']['properties']['perfil'] == {
        '$ref': '#/components/schemas/Profile',
    }
    assert schemas['ProfileData']['properties']['contactos'] == {
        '$ref': '#/components/schemas/Contacts',
    }


def test_aplicacion_debe_exigir_archivo_de_configuracion(monkeypatch):
    with monkeypatch.context() as context:
        context.delenv(
            'PROFILE_CONFIG_FILE',
            raising=False,
        )

        with pytest.raises(
            OSError,
            match='Variable de entorno PROFILE_CONFIG_FILE no definida.',
        ):
            create_app(
                cors_allowed_origin='https://frontend.example',
            )


def test_aplicacion_debe_permitir_origen_cors_configurado(
    client,
    cors_allowed_origin,
):
    response = client.get(
        '/api/v1/health/',
        headers={
            'Origin': cors_allowed_origin,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.headers['Access-Control-Allow-Origin'] == (
        cors_allowed_origin
    )


def test_aplicacion_no_debe_permitir_origen_cors_desconocido(client):
    response = client.get(
        '/api/v1/health/',
        headers={
            'Origin': 'https://origen-desconocido.example',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert 'Access-Control-Allow-Origin' not in response.headers


def test_aplicacion_debe_cargar_origen_cors_desde_entorno(monkeypatch):
    cors_allowed_origin = 'https://frontend-entorno.example'

    with monkeypatch.context() as context:
        context.setenv(
            'CORS_ALLOWED_ORIGIN',
            cors_allowed_origin,
        )

        application = create_app(
            profile_config_file='profile-config.json',
        )

    response = application.test_client().get(
        '/api/v1/health/',
        headers={
            'Origin': cors_allowed_origin,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.headers['Access-Control-Allow-Origin'] == (
        cors_allowed_origin
    )


def test_aplicacion_debe_exigir_origen_cors(monkeypatch):
    with monkeypatch.context() as context:
        context.delenv(
            'CORS_ALLOWED_ORIGIN',
            raising=False,
        )

        with pytest.raises(
            OSError,
            match='Variable de entorno CORS_ALLOWED_ORIGIN no definida.',
        ):
            create_app(
                profile_config_file='profile-config.json',
            )


def test_aplicacion_no_debe_aplicar_cors_fuera_de_la_api(
    client,
    cors_allowed_origin,
):
    response = client.get(
        '/',
        headers={
            'Origin': cors_allowed_origin,
        },
    )

    assert response.status_code == HTTPStatus.FOUND
    assert 'Access-Control-Allow-Origin' not in response.headers
