from fastapi import HTTPException
from starlette import status


def raise_http_exception(status_code: int, detail: str) -> None:
    raise HTTPException(status_code=status_code, detail=detail)


def not_found_exception(message: str):
    raise HTTPException(status_code=404, detail=message)


def not_found(detail: str = "Not found") -> None:
    raise_http_exception(status.HTTP_404_NOT_FOUND, detail)


def bad_request(detail: str = "Bad request") -> None:
    raise_http_exception(status.HTTP_400_BAD_REQUEST, detail)


def conflict_exception(message: str):
    raise HTTPException(status_code=409, detail=message)


def forbidden(detail: str = "Forbidden") -> None:
    raise_http_exception(status.HTTP_403_FORBIDDEN, detail)


def conflict(detail: str = "Conflict") -> None:
    raise_http_exception(status.HTTP_409_CONFLICT, detail)


def unauthorized(detail: str = "Unauthorized") -> None:
    raise_http_exception(status.HTTP_401_UNAUTHORIZED, detail)