import abc
from dataclasses import dataclass
from ... import SystemState

@dataclass(frozen=True, slots=True)
class ReadyInfo:
    userid: int
    username: str
    unavailable_guild_ids: list[int]


@dataclass(frozen=True, slots=True)
class GuildCreateInfo:
    guild_id: int
    guild_name: str


class GatewayInformationInterface(abc.ABC):
    """
    The interface for pulling information necessary for gateway events.
    """
    @abc.abstractmethod
    async def get_ready_info(self, userid: int) -> ReadyInfo:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_guild_creates(self, userid: int) -> list[GuildCreateInfo]:
        raise NotImplementedError

class SystemStateGatewayInformationInterface(GatewayInformationInterface):

    def __init__(self, system_state: SystemState):
        self._state = system_state

    async def get_ready_info(self, userid: int) -> ReadyInfo:
        user_with_id = self._state.users.find_by_id(userid=userid)
        unavailable_guild_ids = []
        for guild in self._state.guilds.get_guilds_by_member_id(userid):
            unavailable_guild_ids.append(guild.id)
        return ReadyInfo(user_with_id.id, user_with_id.username, unavailable_guild_ids)

    async def get_guild_creates(self, userid: int) -> list[GuildCreateInfo]:
        guild_create_entries = []
        guilds_containing_user = self._state.guilds.get_guilds_by_member_id(userid)
        for guild in guilds_containing_user:
            guild_create_info = GuildCreateInfo(guild_id=guild.id, guild_name=guild.name)
            guild_create_entries.append(guild_create_info)
        return guild_create_entries