"""
Custom exception handling for the OpenCare API.
"""

from __future__ import annotations

import logging
from typing import Any

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger("opencare.exceptions")

GENERIC_MESSAGE = _("An unexpected error occurred. Please try again later.")
BASIC_MESSAGE_MAP = {
    status.HTTP_400_BAD_REQUEST: _("Request validation failed."),
    status.HTTP_401_UNAUTHORIZED: _("Authentication credentials were not provided or are invalid."),
    status.HTTP_403_FORBIDDEN: _("You do not have permission to perform this action."),
    status.HTTP_404_NOT_FOUND: _("The requested resource could not be found."),
}


def sanitized_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    """
    Wrap DRF's exception handler to standardize and sanitize error responses.

    * Returns a structured payload with `code` and `message`.
    * Logs full details server-side for operational visibility.
    * Ensures generic messaging for all 5xx responses to avoid leaking secrets.
    """

    response = drf_exception_handler(exc, context)
    request = context.get("request")
    metadata = {
        "path": getattr(request, "path", None),
        "method": getattr(request, "method", None),
        "user_id": getattr(getattr(request, "user", None), "pk", None),
        "view": context.get("view").__class__.__name__ if context.get("view") else None,
    }

    if response is None:
        logger.exception("Unhandled exception", extra={"request": metadata})
        return Response(
            {"code": "server_error", "message": GENERIC_MESSAGE},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    status_code = response.status_code
    raw_data = response.data
    if isinstance(raw_data, dict):
        code = raw_data.get("code") or getattr(exc, "default_code", None) or "error"
    else:
        code = getattr(exc, "default_code", None) or "error"

    if status_code >= 500:
        logger.exception("Internal server error", extra={"request": metadata})
        return Response(
            {"code": "server_error", "message": GENERIC_MESSAGE},
            status=status_code,
        )

    if 400 <= status_code < 500:
        logger.warning("API request failed", extra={"request": metadata, "code": code})
        message = BASIC_MESSAGE_MAP.get(status_code, response.status_text)
        normalized_errors = _normalize_errors(raw_data)
        payload: dict[str, Any] = {"code": code, "message": message}
        if normalized_errors:
            payload["errors"] = normalized_errors
        response.data = payload
        return response

    # Fallback for any other status codes (should be rare)
    logger.error("Unexpected exception handler pathway", extra={"request": metadata, "code": code})
    return Response(
        {"code": code, "message": GENERIC_MESSAGE},
        status=status_code,
    )


def _normalize_errors(data: Any) -> Any:
    """
    Recursively convert DRF ErrorDetail objects into primitive types for JSON.
    """

    if data is None:
        return None
    if isinstance(data, (list, tuple)):
        return [_normalize_errors(item) for item in data]
    if isinstance(data, dict):
        return {key: _normalize_errors(value) for key, value in data.items()}
    return str(data)
