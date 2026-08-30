from flask import Blueprint


api_v1_blueprint = Blueprint('root', __name__)


@api_v1_blueprint.get('/')
def root():
    return {'status': 'ok'}, 200
