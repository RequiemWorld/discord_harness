import abc
from ._users import DiscordBackendUsers
from ._users import SystemStateBackendUsers
from ._users import UserCreationRequest
from ._guilds import DiscordBackendGuilds
from ._guilds import SystemStateBackendGuilds
from ._guilds import GuildCreationRequest


class DiscordBackendInterface(abc.ABC):
    def __init__(self, users: DiscordBackendUsers, guilds: DiscordBackendGuilds):
        self._guilds = guilds
        self._users = users

    @property
    def guilds(self) -> DiscordBackendGuilds:
        return self._guilds

    @property
    def users(self) -> DiscordBackendUsers:
        return self._users