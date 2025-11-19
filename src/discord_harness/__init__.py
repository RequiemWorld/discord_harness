import discord
from discord_harness.backend import User
from discord_harness.backend import Guild
from discord_harness.backend import SystemState
from discord_harness.payloads import make_ready_payload


class HarnessError(Exception):
    pass

class NoSuchGuildError(HarnessError):
    pass


class NoSuchUserError(HarnessError):
    pass


class HarnessUsers:
    def __init__(self, state: SystemState):
        self._state = state

    async def new_user(self, name: str) -> None:
        new_user = User(id_=self._state.next_id(), username=name)
        self._state.users.add_new_user(new_user)


class HarnessGuilds:
    def __init__(self, state: SystemState):
        self._state = state

    async def new_guild(self, guild_name: str, owner_name: str) -> None:
        """
        :raises ValueError: When the there is no user in the system with the given owner name.
        """
        if (user := self._state.users.find_by_username(owner_name)) is None:
            raise ValueError(f"no user with the name {owner_name} could be found in system")
        guild_id = self._state.next_id()
        guild_name = guild_name
        guild_owner_id = user.id
        new_guild = Guild(guild_id, guild_name, guild_owner_id)
        new_guild.members.append(guild_owner_id)
        self._state.guilds.add_new_guild(new_guild)


class Harness:
    def __init__(self):
        self._state = SystemState()
        self._users = HarnessUsers(self._state)
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
        ready_event_data_no_guilds = make_ready_payload(username=discord_name, guild_ids=[])
        connection_state.parse_ready(ready_event_data_no_guilds)
