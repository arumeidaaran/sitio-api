from http import HTTPStatus

from api.v1.routes import profile


def test_profile_de_idioma_disponible_debe_retornar_200_ok(client):
    response = client.get('/api/v1/pt-BR/profile/')

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {
        'status': 'ok',
        'status_code': HTTPStatus.OK,
        'message': 'Idioma encontrado.',
        'data': {},
    }


def test_profile_de_idioma_inexistente_debe_retornar_404_not_found(client):
    response = client.get('/api/v1/fr-FR/profile/')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == {
        'status': 'not_found',
        'status_code': HTTPStatus.NOT_FOUND,
        'message': 'Idioma no localizado.',
        'data': None,
    }


def test_profile_no_debe_aceptar_post(client):
    response = client.post('/api/v1/pt-BR/profile/')

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_error_inesperado_de_profile_debe_retornar_500(
    client,
    monkeypatch,
):
    class IdiomasConError:
        def __contains__(self, idioma):
            raise RuntimeError('Error interno del servidor.')

    monkeypatch.setattr(
        profile,
        'IDIOMAS_PERMITIDOS',
        IdiomasConError(),
    )

    response = client.get('/api/v1/pt-BR/profile/')

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.get_json() == {
        'status': 'internal_server_error',
        'status_code': HTTPStatus.INTERNAL_SERVER_ERROR,
        'message': 'Error interno del servidor.',
        'data': None,
    }
