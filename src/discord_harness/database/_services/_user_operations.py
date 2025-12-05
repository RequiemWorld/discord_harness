from .._entities import User
from .._entities import SystemState


class UserOperationsService:
    def __init__(self, state: SystemState):
        self._state = state

    def new_user(self, username: str) -> None:
        new_user_id = self._state.next_id()
        new_user = User(id_=new_user_id, username=username)
        self._state.users.add_new_user(new_user)
