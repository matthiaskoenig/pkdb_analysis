""".Utility functions."""
import functools
import logging
import warnings
from pathlib import Path
from typing import Callable

from depinfo import print_dependencies  # type: ignore


logger = logging.getLogger(__name__)


def show_versions() -> None:
    """Print dependency information."""
    print_dependencies("pkdb_analysis")


def create_parent(path: Path) -> None:
    """Creates directory for given path."""
    _dir = path.parent
    if not _dir.exists():
        logger.warning(f"Creating directory: {_dir}")
        _dir.mkdir(parents=True)


def deprecated(func: Callable) -> Callable:
    """Decorate function as deprecated.

    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter("always", DeprecationWarning)  # turn off filter
        warnings.warn(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            stacklevel=2,
        )
        warnings.simplefilter("default", DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func


def recursive_iter(obj, keys=()):
    """Create dictionary with key:object from nested JSON data structure."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from recursive_iter(v, keys + (k,))

    elif any(isinstance(obj, t) for t in (list, tuple)):
        for idx, item in enumerate(obj):
            yield from recursive_iter(item, keys + (idx,))

        if len(obj) == 0:
            yield keys, None

    else:
        yield keys, obj
