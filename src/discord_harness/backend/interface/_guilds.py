import abc
from dataclasses import dataclass
from discord_harness import SystemState
from discord_harness.backend import Guild


@dataclass(frozen=True, slots=True)
class GuildCreationRequest:
    guild_name: str
    guild_owner_name: str  # TODO decide if requests to backend should take ids or names


@dataclass(frozen=True, slots=True)
class GuildJoinRequest:
    guild_name: str
    user_name: str


class DiscordBackendGuilds(abc.ABC):

    @abc.abstractmethod
    async def create_guild(self, request: GuildCreationRequest) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def join_guild(self, request: GuildJoinRequest) -> None:
        raise NotImplementedError

class SystemStateBackendGuilds(DiscordBackendGuilds):
    def __init__(self, system_state: SystemState):
        self._state = system_state

    async def create_guild(self, request: GuildCreationRequest) -> None:
        owner_id = self._state.users.find_id_for_username(request.guild_owner_name)
        new_guild = Guild(id_=self._state.next_id(), name=request.guild_name, owner_id=owner_id)
        new_guild.members.append(owner_id)
        self._state.guilds.add_new_guild(new_guild)

    async def join_guild(self, request: GuildJoinRequest) -> None:
        # todo plan explicit logic for when there are multiple guilds with the same name
        id_for_user_with_name = self._state.users.find_id_for_username(request.user_name)
        first_guild_with_name = self._state.guilds.find_guild_by_name(request.guild_name)
        first_guild_with_name.members.append(id_for_user_with_name)
