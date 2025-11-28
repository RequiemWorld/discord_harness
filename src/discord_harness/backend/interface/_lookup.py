import abc
from ... import SystemState


class DiscordBackendLookup(abc.ABC):
    @abc.abstractmethod
    async def lookup_id_for_name(self, user_name: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def lookup_user_existence_by_name(self, user_name: str):
        raise NotImplementedError

    @abc.abstractmethod
    async def lookup_guild_existence_by_name(self, guild_name: str):
        raise NotImplementedError


class SystemStateBackendLookup(DiscordBackendLookup):
    def __init__(self, state: SystemState):
        self._state = state

    async def lookup_id_for_name(self, user_name: str):
        return self._state.users.find_id_for_username(username=user_name)

    async def lookup_user_existence_by_name(self, user_name: str):
        return self._state.users.find_by_username(user_name) is not None

    async def lookup_guild_existence_by_name(self, guild_name: str):
        return self._state.guilds.find_guild_by_name(guild_name) is not None
