"""Module with functions to retrieve information about a club."""

from __future__ import annotations

import logging
import time

from britishcycling_clubs.manager import (
    ManagerMemberCounts,
    get_manager_member_counts,
    manager_url_via_login,
)
from britishcycling_clubs.profile_ import (
    ProfileInfo,
    get_profile_info,
    profile_url,
)

__all__ = [
    "profile_url",
    "get_profile_info",
    "ProfileInfo",
    "manager_url_via_login",
    "get_manager_member_counts",
    "ManagerMemberCounts",
]


def _log_debug(
    logger: logging.Logger,
    message: str,
    start_time: float,
) -> None:
    """Add DEBUG log entry, with elapsed time since `start_time`."""
    _log(logger=logger, level=logging.DEBUG, message=message, start_time=start_time)


def _log_info(
    logger: logging.Logger,
    message: str,
    start_time: float,
) -> None:
    """Add INFO log entry, with elapsed time since `start_time`."""
    _log(logger=logger, level=logging.INFO, message=message, start_time=start_time)


def _log(
    *,
    logger: logging.Logger,
    level: int,
    message: str,
    start_time: float,
) -> None:
    """Add log entry, with elapsed time since `start_time`."""
    elapsed_time = time.time() - start_time
    log_message = f"Elapsed: {elapsed_time:.1f} s. {message}"
    logger.log(level=level, msg=log_message)
