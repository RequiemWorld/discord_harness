import unittest
from discord_harness.database import SystemState
from discord_harness.backend.interface import UserCreationRequest
from discord_harness.backend.interface import GuildCreationRequest
from discord_harness.backend.interface import SystemStateBackendUsers
from discord_harness.backend.interface import SystemStateBackendGuilds
from discord_harness.backend.interface import SystemStateBackendLookup
from discord_harness.backend.interface import SystemStateGatewayInformationInterface

class BackendPiecesTestFixture(unittest.IsolatedAsyncioTestCase):
    """
    A fixture that will system state versions of backend objects,
    with access to the same system state that they're using, for assertion.
    """

    def setUp(self):
        self._system_state = SystemState()
        self._backend_users = SystemStateBackendUsers(self._system_state)
        self._backend_guilds = SystemStateBackendGuilds(self._system_state)
        self._backend_gateway = SystemStateGatewayInformationInterface(self._system_state)
        self._backend_lookup = SystemStateBackendLookup(self._system_state)

    def assertGuildWithNameHasMemberWithId(self, member_id: int, guild_name: str):
        fail_message = f"member with id {member_id} could not be found in guild with name {guild_name}"
        guild = self._system_state.guilds.find_guild_by_name(guild_name)
        self.assertIn(member_id, guild.members, msg=fail_message)

    def assertGuildWithNameHasChannelWithName(self, channel_name: str, guild_name: str):
        found_channel_with_name_in_guild = False
        for channel in self._system_state.guilds.find_guild_by_name(guild_name).channels:
            if channel.name == channel_name:
                found_channel_with_name_in_guild = True
                break
        fail_message = f"no channel with name {channel_name} could be found in guild with name {guild_name}"
        if not found_channel_with_name_in_guild:
            self.fail(fail_message)

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