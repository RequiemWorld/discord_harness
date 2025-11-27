import discord
from ._users import HarnessUsers
from ._guilds import HarnessGuilds
from discord_harness.backend import SystemState
from discord_harness.backend.interface import SystemStateBackendUsers
from discord_harness.backend.interface import SystemStateBackendGuilds
from discord_harness.backend.interface import SystemStateBackendLookup
from discord_harness.backend.interface import SystemStateGatewayInformationInterface
from discord_harness.payloads import make_ready_payload


class Harness:
    def __init__(self):
        self._state = SystemState()
        backend_users = SystemStateBackendUsers(self._state)
        backend_guilds = SystemStateBackendGuilds(self._state)
        backend_lookup = SystemStateBackendLookup(self._state)
        self._backend_gateway = SystemStateGatewayInformationInterface(self._state)
        self._users = HarnessUsers(backend_users)
        self._guilds = HarnessGuilds(backend_guilds, backend_lookup)

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
        connection_state = client._connection
        # ConnectionState.parse_x is where the data off the websocket would usually get handled,
        # we can create the data as necessary and inject it there after we've called the setup hook.
        discord_id = self._state.users.find_id_for_username(discord_name)
        ready_info = await self._backend_gateway.get_ready_info(discord_id)
        ready_event_data = make_ready_payload(username=discord_name, guild_ids=ready_info.unavailable_guild_ids)
        connection_state.parse_ready(ready_event_data)
        for create_info in await self._backend_gateway.get_guild_creates(discord_id):
            guild_create_data = {"id": create_info.guild_id, "name": create_info.guild_name}
            connection_state.parse_guild_create(guild_create_data)
