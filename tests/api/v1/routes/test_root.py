from http import HTTPStatus


def test_raiz_de_la_version_de_api_actual_debe_retornar_200_ok(client):
    response = client.get('/api/v1/')

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {
        'status': 'ok',
        'status_code': HTTPStatus.OK,
        'message': 'API disponible.',
        'data': {},
    }


def test_error_inesperado_de_raiz_debe_retornar_500(
    client,
    monkeypatch,
):
    from api.v1.routes import root

    def generar_error(**kwargs):
        raise RuntimeError('Error interno de prueba.')

    monkeypatch.setattr(root, 'OkResponse', generar_error)

    response = client.get('/api/v1/')

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.get_json() == {
        'status': 'internal_server_error',
        'status_code': HTTPStatus.INTERNAL_SERVER_ERROR,
        'message': 'Error interno del servidor.',
        'data': None,
    }
