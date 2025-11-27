import abc
import discord
from discord.state import ConnectionState
from discord_harness import make_ready_payload
from discord_harness.backend.information import ReadyInfo
from discord_harness.backend.information import GuildCreateInfo


# No automated tests exist for this, it's mostly meant as an implementation
# detail to be covered by BDD style integration tests of the harness with the client.
class ClientEventCommunicator:
    """
    A class to communicate gateway event information to the client,
    not sending anything if connection state hasn't been setup. You can
    inject this class into component pieces prior to setting the client up.
    """
    def __init__(self, connection_state: ConnectionState | None):
        self._connection_state = connection_state

    def set_connection_state(self, connection_state: ConnectionState):
        self._connection_state = connection_state

    def communicate_ready_info(self, ready_info: ReadyInfo):
        if self._connection_state is None:
            return
        ready_event_data = make_ready_payload(username=ready_info.username, guild_ids=ready_info.unavailable_guild_ids)
        self._connection_state.parse_ready(ready_event_data)

    def communicate_guild_create(self, guild_create: GuildCreateInfo):
        if self._connection_state is None:
            return
        guild_create_data = {"id": guild_create.guild_id, "name": guild_create.guild_name}
        self._connection_state.parse_guild_create(guild_create_data)
