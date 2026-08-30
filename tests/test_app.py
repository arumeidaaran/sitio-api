from http import HTTPStatus


def test_raiz_debe_redireccionar_a_raiz_de_la_version_de_api_actual(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.FOUND
    assert response.headers['Location'] == '/api/v1/'
