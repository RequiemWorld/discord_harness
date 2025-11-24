from .. import BackendPiecesTestFixture


class TestPullingReadyInfoUnavailableGuilds(BackendPiecesTestFixture):

    async def test_should_see_no_guilds_in_unavailable_guilds_when_none_exist(self):
        await self.create_user("MyBotName")
        userid = self._system_state.users.find_id_for_username("MyBotName")
        ready_info = await self._backend_gateway.get_ready_info(userid)
        self.assertEqual([], ready_info.unavailable_guild_ids)

    async def test_should_see_no_guilds_in_unavailable_guilds_when_not_in_any(self):
        await self.create_user_and_guild(username="SomeUser", guild_name="SomeGuild")
        await self.create_user("MyBotName")
        userid = self._system_state.users.find_id_for_username("MyBotName")
        ready_info = await self._backend_gateway.get_ready_info(userid)
        self.assertEqual([], ready_info.unavailable_guild_ids)

    async def test_should_see_unavailable_guild_entry_for_each_guild_user_is_in(self):
        # There's no functionality on this new backend yet to join a guild, but when a user
        # creates one they'll be placed in it automatically and see it in this information the same.
        # ~ November 23rd 2025
        await self.create_user("SomeUser")
        await self.create_guild(guild_name="SomeGuild1", username="SomeUser")
        await self.create_guild(guild_name="SomeGuild2", username="SomeUser")
        created_user_id = self._system_state.users.find_id_for_username("SomeUser")
        created_guild_id_1 = self._system_state.guilds.find_guild_by_name("SomeGuild1").id
        created_guild_id_2 = self._system_state.guilds.find_guild_by_name("SomeGuild2").id
        ready_info = await self._backend_gateway.get_ready_info(userid=created_user_id)
        self.assertIn(created_guild_id_1, ready_info.unavailable_guild_ids)
        self.assertIn(created_guild_id_2, ready_info.unavailable_guild_ids)

class TestPullingReadyInfoUserInformation(BackendPiecesTestFixture):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        await self.create_user_and_guild("AGuild", "AUser")
        await self.create_user("NameBotMy")
        self._userid = self._system_state.users.find_id_for_username("NameBotMy")
        self._ready_info = await self._backend_gateway.get_ready_info(self._userid)

    async def test_should_see_username_of_account_in_ready_info(self):
        self.assertEqual("NameBotMy", self._ready_info.username)

    async def test_should_see_userid_of_account_in_ready_info(self):
        self.assertEqual(self._userid, self._ready_info.userid)

