import discord
from ._users import HarnessUsers
from ._guilds import HarnessGuilds
from discord_harness.backend import SystemState
from discord_harness.backend.interface import SystemStateBackendUsers
from discord_harness.backend.interface import SystemStateBackendGuilds
from discord_harness.backend.interface import SystemStateBackendLookup
from discord_harness.backend.interface import SystemStateGatewayInformationInterface
from ._communicator import ClientEventCommunicator

class Harness:
    def __init__(self):
        self._state = SystemState()
        backend_users = SystemStateBackendUsers(self._state)
        backend_guilds = SystemStateBackendGuilds(self._state)
        backend_lookup = SystemStateBackendLookup(self._state)
        self._backend_gateway = SystemStateGatewayInformationInterface(self._state)
        self._users = HarnessUsers(backend_users)
        self._guilds = HarnessGuilds(backend_guilds, backend_lookup)
        self._communicator = ClientEventCommunicator(connection_state=None)

    @property
    def users(self):
        return self._users

    @property
    def guilds(self):
        return self._guilds

    async def initialize(self, client: discord.Client, discord_name: str):
        """
        :param client: The discord client to perform initialization on.
        :param discord_name: The name of the discord account to use for the bot.
        """
        # The client will expect a READY event with a list of every guild the user is in
        # None of the events will reach event listeners later if this hook isn't awaited.
        await client._async_setup_hook()
        self._communicator.set_connection_state(client._connection)
        # ConnectionState.parse_x is where the data off the websocket would usually get handled,
        # we can create the data as necessary and inject it there after we've called the setup hook.
        discord_id = self._state.users.find_id_for_username(discord_name)
        ready_info = await self._backend_gateway.get_ready_info(discord_id)
        self._communicator.communicate_ready_info(ready_info)
        for create_info in await self._backend_gateway.get_guild_creates(discord_id):
            self._communicator.communicate_guild_create(create_info)
