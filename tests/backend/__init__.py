import unittest
from discord_harness import SystemState
from discord_harness.backend.interface import UserCreationRequest
from discord_harness.backend.interface import GuildCreationRequest
from discord_harness.backend.interface import SystemStateBackendUsers
from discord_harness.backend.interface import SystemStateBackendGuilds


class BackendPiecesTestFixture(unittest.IsolatedAsyncioTestCase):
    """
    A fixture that will system state versions of backend objects,
    with access to the same system state that they're using, for assertion.
    """

    def setUp(self):
        self._system_state = SystemState()
        self._backend_users = SystemStateBackendUsers(self._system_state)
        self._backend_guilds = SystemStateBackendGuilds(self._system_state)

    async def create_user(self, username: str):
        creation_request = UserCreationRequest(username=username)
        await self._backend_users.create_user(creation_request)

    async def create_guild(self, guild_name: str, username: str):
        creation_request = GuildCreationRequest(guild_name, username)
        await self._backend_guilds.create_guild(creation_request)

    async def create_user_and_guild(self, username: str, guild_name: str):
        await self.create_user(username)
        await self.create_guild(guild_name, username)

    def override_next_id_indefinitely(self, next_id: int):
        self._system_state.next_id = lambda: next_id