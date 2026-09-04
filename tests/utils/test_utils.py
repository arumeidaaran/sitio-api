from json import JSONDecodeError

import pytest

from utils.utils import read_json_file


def test_read_json_file_debe_retornar_contenido_del_archivo(tmp_path):
    json_file = tmp_path / 'contenido.json'
    json_file.write_text(
        '{"nombre": "perfil", "activo": true}',
        encoding='utf8',
    )

    result = read_json_file(json_file)

    assert result == {
        'nombre': 'perfil',
        'activo': True,
    }


def test_read_json_file_debe_aceptar_camino_como_string(tmp_path):
    json_file = tmp_path / 'contenido.json'
    json_file.write_text('{"id": 1}', encoding='utf8')

    result = read_json_file(str(json_file))

    assert result == {'id': 1}


def test_read_json_file_con_json_invalido_debe_producir_error(tmp_path):
    json_file = tmp_path / 'contenido.json'
    json_file.write_text('{"nombre":', encoding='utf8')

    with pytest.raises(JSONDecodeError):
        read_json_file(json_file)


def test_read_json_file_con_archivo_inexistente_debe_producir_error(
    tmp_path,
):
    json_file = tmp_path / 'inexistente.json'

    with pytest.raises(FileNotFoundError):
        read_json_file(json_file)
