from . import HarnessPiecesTestFixture


class TestHarnessNewUserCreation(HarnessPiecesTestFixture):

    async def test_should_make_new_user_and_add_to_system_state_with_name_given(self):
        await self._harness_users.new_user("NamedPerson")
        self.assertIsNotNone(self._system_state.users.find_by_username("NamedPerson"))

    # TODO This is getting scrapped later for snowflake ids, but for exploration this is the right design.
    async def test_should_make_new_users_and_add_to_system_state_with_incrementing_ids(self):
        await self._harness_users.new_user("Name123")
        await self._harness_users.new_user("Name456")
        added_user_one = self._system_state.users.find_by_username("Name123")
        added_user_two = self._system_state.users.find_by_username("Name456")
        self.assertEqual(1, added_user_one.id)
        self.assertEqual(2, added_user_two.id)
