from http import HTTPStatus


def test_raiz_de_la_version_de_api_actual_debe_retornar_200_ok(client):
    response = client.get('/api/v1/')

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {
        'status': 'ok',
        'message': 'API disponible.',
    }
