import unittest
from discord_harness.backend import Guilds
from discord_harness.backend import Users
from discord_harness.backend import SystemState


class TestSystemStateProperties(unittest.TestCase):
    def setUp(self):
        self._state = SystemState()

    def test_should_have_guilds_property_or_attribute(self):
        self.assertIsInstance(self._state.guilds, Guilds)

    def test_should_have_users_property_or_attribute(self):
        self.assertIsInstance(self._state.users, Users)