import abc
from dataclasses import dataclass
from discord_harness import SystemState
from discord_harness.backend import Guild


@dataclass(frozen=True, slots=True)
class GuildCreationRequest:
    guild_name: str
    guild_owner_name: str  # TODO decide if requests to backend should take ids or names


class DiscordBackendGuilds(abc.ABC):

    @abc.abstractmethod
    async def create_guild(self, request: GuildCreationRequest) -> None:
        raise NotImplementedError


class SystemStateBackendGuilds(DiscordBackendGuilds):
    def __init__(self, system_state: SystemState):
        self._state = system_state

    async def create_guild(self, request: GuildCreationRequest) -> None:
        owner_id = self._state.users.find_id_for_username(request.guild_owner_name)
        new_guild = Guild(id_=self._state.next_id(), name=request.guild_name, owner_id=owner_id)
        self._state.guilds.add_new_guild(new_guild)
