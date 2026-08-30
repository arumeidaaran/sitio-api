def not_found(error):
    return {
        'error': 'not_found',
        'message': 'Recurso no encontrado.',
    }, 404


def internal_server_error(error):
    return {
        "error": 'internal_server_error',
        "message": 'Error interno del servidor.',
    }, 500
