from ._users import User
from ._users import Users
from ._guilds import Guild
from ._guilds import GuildChannel
from ._guilds import Guilds


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