from ._users import User
from ._users import Users


class Guild:
    def __init__(self, id_: int, name: str, owner_id: int):
        self.id = id_
        self.name = name
        self.owner_id = owner_id
        self._members = list()

    @property
    def members(self) -> list[int]:
        """
        The list of identifiers for members who are in the guild.
        """
        return self._members


class Guilds:
    def __init__(self):
        self._guild_list: list[Guild] = []

    def add_new_guild(self, guild: Guild) -> None:
        self._guild_list.append(guild)

    def get_all_guilds(self) -> list[Guild]:
        return self._guild_list.copy()

    def get_guilds_by_member_id(self, member_id: int) -> list[Guild]:
        guilds_with_member = []
        for guild in self._guild_list:
            if member_id in guild.members:
                guilds_with_member.append(guild)
        return guilds_with_member

    def find_guild_by_name(self, guild_name: str) -> Guild | None:
        for guild in self._guild_list:
            if guild.name == guild_name:
                return guild
        return None


class SystemState:
    def __init__(self):
        self._guilds = Guilds()
        self._users = Users()
        self._id_to_increment_from = 0

    @property
    def users(self):
        return self._users

    @property
    def guilds(self):
        return self._guilds

    def next_id(self):
        next_id = self._id_to_increment_from + 1
        self._id_to_increment_from = next_id
        return next_id