from discord_harness import DiscordBackendUsers, UserCreationRequest


class HarnessUsers:
    def __init__(self, backend_users: DiscordBackendUsers):
        self._backend_users = backend_users

    async def new_user(self, name: str) -> None:
        creation_request = UserCreationRequest(username=name)
        await self._backend_users.create_user(creation_request)
