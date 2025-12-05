from . import DatabaseTestFixture


class TestNewUserMethod(DatabaseTestFixture):

    def test_should_create_user_in_state_with_name_given(self):
        self._user_operations.new_user("NewUserName555")
        self.assertIsNotNone(self._state.users.find_by_username("NewUserName555"))

    def test_should_create_user_in_state_with_next_id_provided(self):
        self.override_system_state_next_id_indefinitely(2125)
        self._user_operations.new_user("AnotherUser")
        self.assertEqual(2125, self._state.users.find_by_username("AnotherUser").id)