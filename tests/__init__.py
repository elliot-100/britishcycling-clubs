"""Test suite."""
from unittest.mock import MagicMock, patch

import pytest

from britishcycling_clubs import get_private_member_counts, get_public_club_info

# Constants for testing
CLUB_ID = "123"
USERNAME = "user"
PASSWORD = "pass"
MANAGER_PAGE_LOAD_DELAY = 5

# Mock responses for private member counts
PRIVATE_MEMBER_COUNTS = [
    (
        {"active": "10", "pending": "5", "expired": "2"},
        {"active": 10, "pending": 5, "expired": 2},
        None,
    ),
    ({"active": "", "pending": "0", "expired": "0"}, {}, ValueError),
]

# Mock responses for public club info
PUBLIC_CLUB_INFO = [
    ("Club Name", "42"),
    ("Another Club", "0"),
]


@pytest.mark.parametrize(
    "raw_member_counts, expected_counts, expected_exception",
    PRIVATE_MEMBER_COUNTS,
    ids=["happy-path", "error-zero-active"],
)
def test_get_private_member_counts(
    raw_member_counts,
    expected_counts,
    expected_exception,
):
    with patch("britishcycling_clubs.sync_playwright") as mock_playwright:
        browser_context = MagicMock()
        page_context = MagicMock()
        mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = (
            browser_context
        )
        browser_context.new_page.return_value = page_context
        page_context.locator.side_effect = lambda x: MagicMock(
            inner_text=lambda: raw_member_counts[x.split("=")[-1]],
        )

        if expected_exception:
            with pytest.raises(expected_exception):
                # Act
                get_private_member_counts(
                    CLUB_ID,
                    USERNAME,
                    PASSWORD,
                    MANAGER_PAGE_LOAD_DELAY,
                )
        else:
            # Act
            member_counts = get_private_member_counts(
                CLUB_ID,
                USERNAME,
                PASSWORD,
                MANAGER_PAGE_LOAD_DELAY,
            )

            # Assert
            assert member_counts == expected_counts


@pytest.mark.parametrize(
    "club_name, total_members",
    PUBLIC_CLUB_INFO,
    ids=["happy-path", "zero-members"],
)
def test_get_public_club_info(club_name, total_members):
    with patch("britishcycling_clubs.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_get.return_value = mock_response
        mock_response.content = f"""
        <html>
            <h1 class="article__header__title-body__text">{club_name}</h1>
            <div id="about">
                <div>Total club members: <span>{total_members}</span></div>
            </div>
        </html>
        """
        # Act
        club_info = get_public_club_info(CLUB_ID)

        # Assert
        assert club_info == {
            "club_name": club_name,
            "total_members": int(total_members),
        }
