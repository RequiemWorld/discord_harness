import abc
from ..information import GuildCreateInfo

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
