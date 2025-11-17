class User:
    def __init__(self, id_: int, username: str):
        self.id = id_
        self.username = username


class Users:
    def __init__(self):
        self._users = []

    # There is no discriminator logic for this yet.
    def find_by_username(self, username: str) -> User | None:
        for user in self._users:
            if user.username == username:
                return user
        return None

    def add_new_user(self, user: User) -> None:
        self._users.append(user)

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


class SystemState:
    def __init__(self):
        self._id_to_increment_from = 0

    def next_id(self):
        next_id = self._id_to_increment_from + 1
        self._id_to_increment_from = next_id
        return next_id