"""Trivial test that package imports OK."""

import britishcycling_clubs as bc


def test_spond_import():
    """Won't get to this test if imports fail."""
    assert "bc" in globals()
