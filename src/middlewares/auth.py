from typing import Optional
import functools
import src.utils.exceptions as exception

import src.models as models
from src.utils.webtokens import retrieve_access_token


# use auth_required()
def auth_required(*args, **kwargs):
    def _auth_required(handler):
        @functools.wraps(handler)
        async def wrapper(*args, **kwargs):
            try:
                request = kwargs["request"]
                token = request.cookies.get("authenticator")

                if token is None:
                    raise exception.permissionDenied()

                retrieve_access_token(token)
            except KeyError:
                raise exception.internalServerError(
                    "Missing request|db parameter in route declaration"
                )

            return handler(*args, **kwargs)

        return wrapper

    return _auth_required
