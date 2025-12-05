from . import DatabaseTestFixture


class TestCreateGuildMethod(DatabaseTestFixture):

    def test_should_create_guild_with_next_id_supplied_by_state(self):
        self.override_system_state_next_id_indefinitely(2005)
        self._user_operations.new_user("APerson")
        self._guild_operations.create_guild(guild_name="AGuild", owner_name="APerson")
        id_of_created_guild = self._state.guilds.find_guild_by_name("AGuild").id
        self.assertEqual(2005, id_of_created_guild)

    def test_should_create_guild_with_given_name_as_name_on_guild(self):
        self._user_operations.new_user("SomebodySomewhere")
        self._guild_operations.create_guild(guild_name="MyGuildName", owner_name="SomebodySomewhere")
        self.assertEqual("MyGuildName", self._state.guilds.find_guild_by_name("MyGuildName").name)

    def test_should_create_guild_with_id_of_given_user_as_owner_id(self):
        self._user_operations.new_user("SomeoneElse")
        id_of_new_user = self._state.users.find_id_for_username("SomeoneElse")
        self._guild_operations.create_guild(guild_name="Guild123", owner_name="SomeoneElse")
        self.assertEqual(id_of_new_user, self._state.guilds.find_guild_by_name("Guild123").owner_id)

class TestCreateGuildMethodErroring(DatabaseTestFixture):

    def test_should_raise_value_error_when_user_with_owner_name_does_not_exist(self):
        with self.assertRaises(ValueError):
            self._guild_operations.create_guild("ValidGuildName", "NonExistentOwner")
