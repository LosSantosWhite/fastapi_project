from functools import wraps
from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError
from app.exceptions.http import HTTP404, HTTP409


if TYPE_CHECKING:
    from typing import Callable


def transaction(fn: "Callable"):
    """Class method decorator to control session transaction."""

    @wraps(fn)
    async def wrapper(*args, **kwargs):
        commit = kwargs.pop("_commit", True)
        result = await fn(*args, **kwargs)

        self = args[0]
        if commit:
            await self.session.commit()
        else:
            await self.session.flush()

        return result

    return wrapper


def not_found(detail: str = None):
    """Class method decorator to control must exist behaviour."""

    def constructor(fn: "Callable"):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            one_or_none = kwargs.pop("_one_or_none", False)
            result = await fn(*args, **kwargs)
            if not one_or_none and result is None:
                raise HTTP404(detail=detail)

            return result

        return wrapper

    return constructor


def duplicate(detail: str = None):
    """Class method decorator to control database integration errors."""

    def constructor(fn: "Callable"):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            try:
                result = await fn(*args, **kwargs)
            except IntegrityError:
                raise HTTP409(detail=detail)

            return result

        return wrapper

    return constructor
