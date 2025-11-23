from . import BackendPiecesTestFixture
from discord_harness.backend.interface import UserCreationRequest


class TestBackendSystemStateUserCreation(BackendPiecesTestFixture):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        _new_user_request = UserCreationRequest("MyName123")
        self.override_next_id_indefinitely(514)
        await self._backend_users.create_user(_new_user_request)

    async def test_should_create_user_in_system_state_with_name_sent_in_request(self):
        self.assertIsNotNone(self._system_state.users.find_by_username("MyName123"))

    async def test_should_create_user_in_system_state_with_next_id_given_by_system_state(self):
        id_of_created_user = self._system_state.users.find_id_for_username("MyName123")
        self.assertEqual(514, id_of_created_user)