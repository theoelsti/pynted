"""
This module contains the Pynted class for interacting with the Vinted API.

The Pynted class provides methods to get information about a brand and a
user by their username. These methods are:
- get_brand: Retrieves information about a given brand.
- get_user_by_username: Retrieves information about a user given
by their username.

Example usage:

    vinted = Pynted()
    celine = vinted.get_brand("Celine")
    user = vinted.get_user_by_username("user")
"""

import unittest

from pynted.pynted import Pynted


class TestPynted(unittest.TestCase):
    """Test the Pynted class."""

    def setUp(self):
        self.vinted = Pynted()

    def test_get_brand(self):
        """Try to get a brand by its name."""
        celine = self.vinted.get_brand("Celine")
        self.assertIsNotNone(celine)

    def test_get_user_by_username(self):
        """Try to get a user by its username."""
        user = self.vinted.get_user_by_username("user")
        self.assertIsNotNone(user)


if __name__ == "__main__":
    unittest.main()
