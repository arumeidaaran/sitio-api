import pytest
from pydantic import ValidationError

from schemas.profile import ProfileConfig, ProfileData


def test_configuracion_de_profile_debe_validar_datos_anidados(
    profile_config_data,
):
    profile_config = ProfileConfig.model_validate(profile_config_data)

    assert profile_config.perfiles[0].idioma == 'pt-br'
    assert profile_config.contactos.sitio_web is None
    assert (
        profile_config.contactos.correos_electronicos[0].direccion
        == 'alias@subdominio.dominio'
    )
    assert profile_config.contactos.telefonos[0].numero == '9999999999999'


def test_sitio_web_debe_aceptar_texto(profile_config_data):
    profile_config_data['contactos']['sitio_web'] = (
        'https://subdominio.dominio'
    )

    profile_config = ProfileConfig.model_validate(profile_config_data)

    assert profile_config.contactos.sitio_web == 'https://subdominio.dominio'


def test_sitio_web_debe_ser_obligatorio(profile_config_data):
    profile_config_data['contactos'].pop('sitio_web')

    with pytest.raises(ValidationError):
        ProfileConfig.model_validate(profile_config_data)


def test_datos_de_profile_deben_incluir_perfil_y_contactos(
    profile_config_data,
):
    profile_config = ProfileConfig.model_validate(profile_config_data)

    profile_data = ProfileData(
        perfil=profile_config.perfiles[0],
        contactos=profile_config.contactos,
    )

    assert profile_data.perfil.idioma == 'pt-br'
    assert profile_data.contactos.sitio_web is None


def test_configuracion_de_profile_debe_exigir_campos_del_perfil(
    profile_config_data,
):
    profile_config_data['perfiles'][0].pop('nombre')

    with pytest.raises(ValidationError):
        ProfileConfig.model_validate(profile_config_data)


def test_configuracion_de_profile_no_debe_aceptar_campos_adicionales(
    profile_config_data,
):
    profile_config_data['perfiles'][0]['campo_adicional'] = True

    with pytest.raises(ValidationError):
        ProfileConfig.model_validate(profile_config_data)
