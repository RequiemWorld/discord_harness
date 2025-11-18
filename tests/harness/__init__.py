import unittest
from discord_harness import SystemState
from discord_harness import HarnessUsers
from discord_harness import HarnessGuilds


class HarnessPiecesTestFixture(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self._system_state = SystemState()
        self._harness_users = HarnessUsers(self._system_state)
        self._harness_guilds = HarnessGuilds(self._system_state)