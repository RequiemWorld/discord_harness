

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

    def find_id_for_username(self, username: str) -> int | None:
        """
        Find the id of the user with the given username. No discriminator/bot logic.
        """
        for user in self._users:
            if user.username == username:
                return user.id
        return None

    def add_new_user(self, user: User) -> None:
        self._users.append(user)