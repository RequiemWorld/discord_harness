import abc
from ..information import GuildCreateInfo
from .._entities import SystemState


class GatewayInformationPuller(abc.ABC):

    @abc.abstractmethod
    def pull_guild_create_info_for_guild(self, guild_id: int) -> GuildCreateInfo | None:
        raise NotImplementedError


class MockGatewayInformationPuller(GatewayInformationPuller):
    def __init__(self):
        self._guild_ids_to_preset_info = {}

    def set_result_for_guild_id(self, guild_id: int, result: GuildCreateInfo):
        self._guild_ids_to_preset_info[guild_id] = result

    def pull_guild_create_info_for_guild(self, guild_id: int) -> GuildCreateInfo | None:
        return self._guild_ids_to_preset_info.get(guild_id)



class SystemStateGatewayInformationPuller(GatewayInformationPuller):
    def __init__(self, system_state: SystemState):
        self._state = system_state

    def pull_guild_create_info_for_guild(self, guild_id: int) -> GuildCreateInfo | None:
        found_guild = self._state.guilds.find_guild_by_id(guild_id)
        if found_guild is not None:
            return GuildCreateInfo(guild_id=found_guild.id, guild_name=found_guild.name)
        return None
