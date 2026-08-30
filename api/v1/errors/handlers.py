from http import HTTPStatus


def not_found(error):
    return {
        'error': 'not_found',
        'message': 'Recurso no encontrado.',
    }, HTTPStatus.NOT_FOUND


def internal_server_error(error):
    return {
        'error': 'internal_server_error',
        'message': 'Error interno del servidor.',
    }, HTTPStatus.INTERNAL_SERVER_ERROR
