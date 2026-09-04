import pytest
from pydantic import ValidationError

from schemas.responses import (
    InternalServerErrorResponse,
    NotFoundResponse,
    OkResponse,
)


def test_status_de_respuesta_no_debe_aceptar_otro_valor():
    with pytest.raises(ValidationError):
        NotFoundResponse(status='ok')


def test_respuesta_no_debe_permitir_cambios_despues_de_creada():
    response = OkResponse(
        message='Perfil localizado.',
        data={'idioma': 'pt-br'},
    )

    with pytest.raises(ValidationError):
        response.message = 'Otro mensaje'


def test_error_interno_debe_aceptar_mensaje_personalizado():
    response = InternalServerErrorResponse(
        message='Configuración de perfil no encontrada.',
    )

    assert response.message == 'Configuración de perfil no encontrada.'
