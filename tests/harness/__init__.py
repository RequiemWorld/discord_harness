import unittest
from discord_harness import SystemState
from discord_harness import HarnessUsers
from discord_harness import HarnessGuilds
from discord_harness.backend.interface import SystemStateBackendUsers
from discord_harness.backend.interface import SystemStateBackendLookup
from discord_harness.backend.interface import SystemStateBackendGuilds


class HarnessPiecesTestFixture(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self._system_state = SystemState()
        backend_users = SystemStateBackendUsers(self._system_state)
        backend_guilds = SystemStateBackendGuilds(self._system_state)
        backend_lookup = SystemStateBackendLookup(self._system_state)
        self._harness_users = HarnessUsers(backend_users)
        self._harness_guilds = HarnessGuilds(backend_guilds, backend_lookup)

    async def create_user_and_guild(self, new_user_name: str, new_guild_name: str):
        await self._harness_users.new_user(new_user_name)
        await self._harness_guilds.new_guild(new_guild_name, new_user_name)