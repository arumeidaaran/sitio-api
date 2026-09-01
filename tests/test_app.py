from http import HTTPStatus


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
    assert '/api/v1/health' in openapi['paths']
