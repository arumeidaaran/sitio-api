from schemas.responses import (
    InternalServerErrorResponse,
    NotFoundResponse,
)


def not_found(error):
    response = NotFoundResponse()

    return response.model_dump(mode='json'), response.status_code


def internal_server_error(error):
    response = InternalServerErrorResponse()

    return (
        response.model_dump(mode='json'),
        response.status_code,
    )
