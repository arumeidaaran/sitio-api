# Import de Python
from http import HTTPStatus

# Import de las librerías
from flask import Flask, redirect

# Import del proyecto
from api.v1.errors.handlers import not_found, internal_server_error
from api.v1.routes.health import health_blueprint
from api.v1.routes.root import api_v1_blueprint

# Inicialización de Flask
app = Flask(__name__)

# Inicialización de variables del proyecto
api_prefix = '/api/v1'

# Registro de blueprints
app.register_blueprint(health_blueprint, url_prefix=api_prefix)
app.register_blueprint(api_v1_blueprint, url_prefix=api_prefix)

# Registro de errores
app.register_error_handler(HTTPStatus.NOT_FOUND, not_found)
app.register_error_handler(
    HTTPStatus.INTERNAL_SERVER_ERROR,
    internal_server_error,
)

# Redirección de la raiz hacia versión actual del app
@app.get('/')
def root():
    return redirect(f'{api_prefix}/')
