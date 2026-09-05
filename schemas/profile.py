from schemas.base import ApiModel
from schemas.responses import OkResponse


class ProfilePath(ApiModel):
    lang: str


class Profile(ApiModel):
    id: int
    idioma: str
    nombre: str
    descripcion: str
    acerca_de: str


class Email(ApiModel):
    tipo: str
    direccion: str


class Phone(ApiModel):
    tipo: str
    formato: str
    numero: str


class Contacts(ApiModel):
    linkedin: str
    github: str
    sitio_web: str | None
    correos_electronicos: list[Email]
    telefonos: list[Phone]


class ProfileConfig(ApiModel):
    perfiles: list[Profile]
    contactos: Contacts


class ProfileData(ApiModel):
    perfil: Profile
    contactos: Contacts


class ProfileResponse(OkResponse):
    data: ProfileData
