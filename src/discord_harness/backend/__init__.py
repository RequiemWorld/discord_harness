
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

class SystemState:
    def __init__(self):
        self._id_to_increment_from = 0

    def next_id(self):
        next_id = self._id_to_increment_from + 1
        self._id_to_increment_from = next_id
        return next_id