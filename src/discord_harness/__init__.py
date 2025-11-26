import discord
from discord_harness.backend import User
from discord_harness.backend import Guild
from discord_harness.backend import GuildChannel
from discord_harness.backend import SystemState
from discord_harness.backend.interface import UserCreationRequest
from discord_harness.backend.interface import DiscordBackendUsers
from discord_harness.backend.interface import SystemStateBackendUsers
from discord_harness.backend.interface import GatewayInformationInterface
from discord_harness.backend.interface import SystemStateGatewayInformationInterface
from discord_harness.payloads import make_ready_payload


class HarnessError(Exception):
    pass

class NoSuchGuildError(HarnessError):
    pass


class NoSuchUserError(HarnessError):
    pass


class HarnessUsers:
    def __init__(self, backend_users: DiscordBackendUsers):
        self._backend_users = backend_users

    async def new_user(self, name: str) -> None:
        creation_request = UserCreationRequest(username=name)
        await self._backend_users.create_user(creation_request)


class HarnessGuilds:
    def __init__(self, state: SystemState):
        self._state = state

    async def new_guild(self, guild_name: str, owner_name: str) -> None:
        """
        :raises NoSuchUserError: When the there is no user in the system with the given owner name.
        """
        if (user := self._state.users.find_by_username(owner_name)) is None:
            raise NoSuchUserError(f"no user with the name {owner_name} could be found in system")
        guild_id = self._state.next_id()
        guild_name = guild_name
        guild_owner_id = user.id
        new_guild = Guild(guild_id, guild_name, guild_owner_id)
        new_guild.members.append(guild_owner_id)
        self._state.guilds.add_new_guild(new_guild)

    # I don't like the look of guild_name, and then username even though username is one word.
    async def join_guild(self, guild_name: str, user_name: str) -> None:
        """
        :param guild_name: Name of the guild that the user will be added to.
        :param user_name: Name of the user that will be added to the guild.
        :raises NoSuchUserError: When name of guild exists, but name of user doesn't.
        :raises NoSuchGuildError: When name of guild exists, regardless to the existence of the user.
        """
        # TODO figure out broadly what to do regarding multiple guilds with the same name
        guild_with_name = self._state.guilds.find_guild_by_name(guild_name)
        if guild_with_name is None:
            raise NoSuchGuildError(f"no guild with the name {guild_name} could be found")
        id_from_username = self._state.users.find_id_for_username(user_name)
        if id_from_username is None:
            raise NoSuchUserError(f"no user with the username {user_name} could be found")
        guild_with_name.members.append(id_from_username)

    async def new_channel(self, guild_name: str, channel_name: str) -> None:
        """
        Effectively creates a public channel in the given guild name.

        :param guild_name: Name of the guild the channel should be created in.
        :param channel_name: Name of the channel to create in the guild.
        """
        new_channel_id = self._state.next_id()
        channel = GuildChannel(new_channel_id, channel_name)
        guild_with_matching_name = self._state.guilds.find_guild_by_name(guild_name)
        guild_with_matching_name.channels.append(channel)


class Harness:
    def __init__(self):
        self._state = SystemState()
        backend_users = SystemStateBackendUsers(self._state)
        self._backend_gateway = SystemStateGatewayInformationInterface(self._state)
        self._users = HarnessUsers(backend_users)
        self._guilds = HarnessGuilds(self._state)

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
