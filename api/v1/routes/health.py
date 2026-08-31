from http import HTTPStatus
from flask_openapi import APIBlueprint


health_blueprint = APIBlueprint('health', __name__)


@health_blueprint.get('/health')
def health():
    return {'status': 'ok'}, HTTPStatus.OK
