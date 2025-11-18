from . import HarnessPiecesTestFixture


class TestNewGuildMethod(HarnessPiecesTestFixture):

    async def test_should_raise_value_error_when_no_user_with_owner_name_exists(self):
        with self.assertRaises(ValueError):
            await self._harness_guilds.new_guild("GuildedName", "Username123")

    async def test_should_make_guild_with_given_name_in_system_state(self):
        await self._harness_users.new_user("SomeUser")
        await self._harness_guilds.new_guild(guild_name="NameOfGuild", owner_name="SomeUser")
        self.assertEqual("NameOfGuild", self._system_state.guilds.get_all_guilds()[0].name)

    async def test_should_have_owner_as_member_after_guild_has_been_made(self):
        await self._harness_users.new_user("Name555")
        await self._harness_guilds.new_guild(guild_name="NameOfGuild", owner_name="Name555")
        expected_owner_id = self._system_state.users.find_by_username("Name555").id
        self.assertIn(expected_owner_id, self._system_state.guilds.get_all_guilds()[0].members)
