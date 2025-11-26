import abc
from ._users import DiscordBackendUsers
from ._users import SystemStateBackendUsers
from ._users import UserCreationRequest
from ._guilds import DiscordBackendGuilds
from ._guilds import SystemStateBackendGuilds
from ._guilds import GuildCreationRequest
from ._guilds import GuildJoinRequest
from ._gateway import GatewayInformationInterface
from ._gateway import SystemStateGatewayInformationInterface
from ._lookup import DiscordBackendLookup
from ._lookup import SystemStateBackendLookup

class DiscordBackendInterface(abc.ABC):
    def __init__(self,
                 users: DiscordBackendUsers,
                 guilds: DiscordBackendGuilds,
                 gateway: GatewayInformationInterface):
        self._guilds = guilds
        self._users = users
        self._gateway = gateway

    @property
    def guilds(self) -> DiscordBackendGuilds:
        return self._guilds

    @property
    def users(self) -> DiscordBackendUsers:
        return self._users

    @property
    def gateway(self) -> GatewayInformationInterface:
        return self._gateway