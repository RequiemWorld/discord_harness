import abc
from dataclasses import dataclass
from discord_harness import User
from discord_harness import SystemState


@dataclass(frozen=True, slots=True)
class UserCreationRequest:
    username: str


class DiscordBackendUsers(abc.ABC):

    @abc.abstractmethod
    async def create_user(self, request: UserCreationRequest):
        raise NotImplementedError


class SystemStateBackendUsers(DiscordBackendUsers):
    def __init__(self, system_state: SystemState):
        self._system_state = system_state

    async def create_user(self, request: UserCreationRequest):
        new_user_id = self._system_state.next_id()
        new_user_username = request.username
        new_user = User(id_=new_user_id, username=new_user_username)
        self._system_state.users.add_new_user(new_user)