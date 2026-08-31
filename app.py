# Import de Python
from http import HTTPStatus

# Import de las librerías
from flask import redirect
from flask_openapi import Info, OpenAPI

# Import del proyecto
from api.v1.errors.handlers import internal_server_error, not_found
from api.v1.routes.health import health_blueprint
from api.v1.routes.root import api_v1_blueprint

# Inicialización de variables del proyecto
api_prefix = '/api/v1'

# Configuración de OpenAPI
info = Info(
    title='sitio-api',
    description='API del sitio personal.',
    version='1.0.0',
)

# Inicialización de Flask/OpenAPI
app = OpenAPI(
    __name__,
    info=info,
    servers=[
        {
            'url': api_prefix,
        },
    ],
    doc_prefix=f'{api_prefix}/docs',
    doc_url='/openapi.json',
)

# Registro de blueprints
app.register_api(
    health_blueprint,
    url_prefix=api_prefix,
)

app.register_api(
    api_v1_blueprint,
    url_prefix=api_prefix,
)

# Registro de errores
app.register_error_handler(
    HTTPStatus.NOT_FOUND,
    not_found,
)

app.register_error_handler(
    HTTPStatus.INTERNAL_SERVER_ERROR,
    internal_server_error,
)

# OpenAPI JSON
@app.get(
    f'{api_prefix}/openapi.json',
    doc_ui=False,
)
def openapi_document():
    return app.api_doc


# Redirección de la raiz hacia versión actual del app
@app.get(
    '/',
    doc_ui=False,
)
def root():
    return redirect(f'{api_prefix}/')
