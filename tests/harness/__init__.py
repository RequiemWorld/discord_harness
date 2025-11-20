import unittest
from discord_harness import SystemState
from discord_harness import HarnessUsers
from discord_harness import HarnessGuilds


class HarnessPiecesTestFixture(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self._system_state = SystemState()
        self._harness_users = HarnessUsers(self._system_state)
        self._harness_guilds = HarnessGuilds(self._system_state)

    async def create_user_and_guild(self, new_user_name: str, new_guild_name: str):
        await self._harness_users.new_user(new_user_name)
        await self._harness_guilds.new_guild(new_guild_name, new_user_name)