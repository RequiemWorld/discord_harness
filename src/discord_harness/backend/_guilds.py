
class GuildMessage:
    def __init__(self, id_: int, author_id: int, content: str):
        self.id = id_
        self.author_id = author_id
        self.content = content


class GuildChannel:
    def __init__(self, id_: int, name: str):
        self.id = id_
        self.name = name
        self._messages = list()

    @property
    def messages(self) -> list[GuildMessage]:
        """
        The list of messages that are in the guild.
        """
        return self._messages


class Guild:
    def __init__(self, id_: int, name: str, owner_id: int):
        self.id = id_
        self.name = name
        self.owner_id = owner_id
        self._members = list()
        self._channels = list()

    @property
    def members(self) -> list[int]:
        """
        The list of identifiers for members who are in the guild.
        """
        return self._members

    @property
    def channels(self) -> list[GuildChannel]:
        return self._channels


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