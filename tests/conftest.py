from os import environ
from unittest.mock import Mock, patch

import pytest

with patch.dict(
    environ,
    {'PROFILE_CONFIG_FILE': 'profile-config.json'},
):
    from api.v1.routes import profile
    from app import create_app


@pytest.fixture()
def app():
    application = create_app('profile-config.json')
    application.config['TESTING'] = True

    return application


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def profile_config_path_mock(monkeypatch):
    config_path = Mock()
    config_path.absolute.return_value = config_path
    config_path.exists.return_value = True

    monkeypatch.setattr(
        profile,
        'Path',
        Mock(return_value=config_path),
    )

    return config_path


@pytest.fixture()
def profile_config_data():
    return {
        'perfiles': [
            {
                'id': 2,
                'idioma': 'pt-br',
                'nombre': 'nome_sobrenome',
                'descripcion': 'descricao_profissional',
                'acerca_de': 'texto_profissional',
            },
        ],
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
    }


@pytest.fixture()
def read_profile_config_mock(monkeypatch, profile_config_data):
    read_json_file_mock = Mock(return_value=profile_config_data)

    monkeypatch.setattr(
        profile,
        'read_json_file',
        read_json_file_mock,
    )

    return read_json_file_mock
