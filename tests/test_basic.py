"""
Basic tests for the draw_things package.
"""

import unittest
from draw_things import __version__


class TestBasic(unittest.TestCase):
    """Basic test cases."""

    def test_version(self):
        """Test that version is a string."""
        self.assertIsInstance(__version__, str)


if __name__ == "__main__":
    unittest.main()