import discord
from discord_harness.payloads import make_ready_payload


class HarnessUsers:

    async def new_user(self, name: str) -> None:
        pass


class Harness:
    def __init__(self):
        self._users = HarnessUsers()

    @property
    def users(self):
        return self._users

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
