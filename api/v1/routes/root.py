from http import HTTPStatus
from flask_openapi import APIBlueprint


api_v1_blueprint = APIBlueprint('root', __name__)


@api_v1_blueprint.get('/')
def root():
    return {'status': 'ok'}, HTTPStatus.OK
