from .._entities import Guild
from .._entities import SystemState


class GuildOperationsService:
    def __init__(self, state: SystemState):
        self._state = state

    def create_guild(self, guild_name: str, owner_name: str) -> None:
        id_for_owner = self._state.users.find_id_for_username(owner_name)
        if id_for_owner is None:
            raise ValueError
        new_guild_id = self._state.next_id()
        new_guild = Guild(id_=new_guild_id, name=guild_name, owner_id=id_for_owner)
        self._state.guilds.add_new_guild(new_guild)