from http import HTTPStatus
from flask import Blueprint


health_blueprint = Blueprint('health', __name__)


@health_blueprint.get('/health')
def health():
    return {'status': 'ok'}, HTTPStatus.OK
