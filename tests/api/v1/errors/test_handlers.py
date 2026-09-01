from http import HTTPStatus

from werkzeug.exceptions import NotFound, InternalServerError

from api.v1.errors.handlers import not_found, internal_server_error


def test_not_found_debe_retornar_respuesta_404():
    response, status_code = not_found(NotFound())

    assert status_code == HTTPStatus.NOT_FOUND
    assert response == {
        'status': 'not_found',
        'message': 'Recurso no encontrado.',
    }


def test_recurso_inexistente_debe_retornar_404_not_found(client):
    response = client.get('/api/v1/not_found')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == {
        'status': 'not_found',
        'message': 'Recurso no encontrado.',
    }


def test_internal_server_error_debe_retornar_respuesta_500():
    response, status_code = internal_server_error(
        InternalServerError()
    )

    assert status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response == {
        'status': 'internal_server_error',
        'message': 'Error interno del servidor.',
    }


def test_error_interno_debe_retornar_500_internal_server_error(
    client,
    monkeypatch,
):
    def generar_error():
        raise RuntimeError('Error interno de prueba.')

    monkeypatch.setitem(
        client.application.view_functions,
        'health.health',
        generar_error,
    )

    monkeypatch.setitem(
        client.application.config,
        'PROPAGATE_EXCEPTIONS',
        False,
    )

    response = client.get('/api/v1/health')

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.get_json() == {
        'status': 'internal_server_error',
        'message': 'Error interno del servidor.',
    }
