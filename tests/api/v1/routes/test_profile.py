from http import HTTPStatus
from unittest.mock import Mock

from api.v1.routes import profile


def test_profile_de_idioma_disponible_debe_retornar_200_ok(
    client,
    profile_config_path_mock,
    read_profile_config_mock,
):
    response = client.get('/api/v1/pt-BR/profile/')

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {
        'status': 'ok',
        'status_code': HTTPStatus.OK,
        'message': 'Idioma encontrado.',
        'data': {
            'perfil': {
                'id': 2,
                'idioma': 'pt-br',
                'nombre': 'nome_sobrenome',
                'descripcion': 'descricao_profissional',
                'acerca_de': 'texto_profissional',
            },
            'contactos': {
                'linkedin': 'https://www.linkedin.com/in/usuario/',
                'github': 'https://github.com/usuario/',
                'sitio_web': None,
                'correos_electronicos': [
                    {
                        'tipo': 'personal',
                        'direccion': 'alias@subdominio.dominio',
                    },
                ],
                'telefonos': [
                    {
                        'tipo': 'celular',
                        'formato': 'brasil',
                        'numero': '9999999999999',
                    },
                ],
            },
        },
    }
    read_profile_config_mock.assert_called_once_with(
        profile_config_path_mock,
    )
    profile_config_path_mock.absolute.assert_called_once_with()
    profile_config_path_mock.exists.assert_called_once_with()


def test_profile_debe_retornar_caracteres_unicode_sin_escape(
    client,
    profile_config_path_mock,
    profile_config_data,
    read_profile_config_mock,
):
    profile_config_data['perfiles'][0]['nombre'] = 'アラン'
    profile_config_data['perfiles'][0]['acerca_de'] = (
        'Automação de processos.'
    )

    response = client.get('/api/v1/pt-BR/profile/')

    response_text = response.get_data(as_text=True)

    assert 'アラン' in response_text
    assert 'Automação de processos.' in response_text
    assert '\\u30a2' not in response_text
    assert '\\u00e7' not in response_text


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


def test_archivo_de_configuracion_inexistente_debe_retornar_500(
    client,
    profile_config_path_mock,
    read_profile_config_mock,
):
    profile_config_path_mock.exists.return_value = False

    response = client.get('/api/v1/pt-BR/profile/')

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.get_json() == {
        'status': 'internal_server_error',
        'status_code': HTTPStatus.INTERNAL_SERVER_ERROR,
        'message': (
            'Camino del archivo de configuración de perfil no encontrado.'
        ),
        'data': None,
    }
    read_profile_config_mock.assert_not_called()


def test_idioma_ausente_en_configuracion_debe_retornar_500(
    client,
    profile_config_path_mock,
    profile_config_data,
    read_profile_config_mock,
):
    profile_config_data['perfiles'] = []

    response = client.get('/api/v1/pt-BR/profile/')

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.get_json() == {
        'status': 'internal_server_error',
        'status_code': HTTPStatus.INTERNAL_SERVER_ERROR,
        'message': 'El idioma solicitado no está configurado en el perfil.',
        'data': None,
    }
    read_profile_config_mock.assert_called_once_with(
        profile_config_path_mock,
    )


def test_error_inesperado_de_profile_debe_retornar_500(
    client,
    monkeypatch,
    profile_config_path_mock,
):
    read_json_file_mock = Mock(
        side_effect=RuntimeError('Error de lectura.'),
    )

    monkeypatch.setattr(
        profile,
        'read_json_file',
        read_json_file_mock,
    )

    response = client.get('/api/v1/pt-BR/profile/')

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.get_json() == {
        'status': 'internal_server_error',
        'status_code': HTTPStatus.INTERNAL_SERVER_ERROR,
        'message': 'Error interno del servidor.',
        'data': None,
    }
    read_json_file_mock.assert_called_once_with(profile_config_path_mock)
