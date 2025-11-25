from .. import BackendPiecesTestFixture


class TestGetGuildCreatesSingleAndMultipleEntries(BackendPiecesTestFixture):

    async def test_should_return_list_containing_single_entry_for_only_guild_user_is_in(self):
        await self.create_user_and_guild(username="NewUserName", guild_name="NewGuildName")
        id_of_created_user = self._system_state.users.find_id_for_username("NewUserName")
        id_of_created_guild = self._system_state.guilds.find_guild_by_name("NewGuildName").id
        guild_create_entries = await self._backend_gateway.get_guild_creates(id_of_created_user)
        first_and_only_entry = guild_create_entries[0]
        self.assertEqual(id_of_created_guild, first_and_only_entry.guild_id)
        self.assertEqual("NewGuildName", first_and_only_entry.guild_name)

    async def test_should_return_list_containing_an_entry_for_each_guild_user_is_in(self):
        await self.create_user("Name123")
        await self.create_guild(guild_name="Guild1", username="Name123")
        await self.create_guild(guild_name="Guild2", username="Name123")
        id_of_created_user = self._system_state.users.find_id_for_username("Name123")
        id_of_first_created_guild = self._system_state.guilds.find_guild_by_name("Guild1").id
        id_of_second_created_guild = self._system_state.guilds.find_guild_by_name("Guild2").id
        two_information_entries = await self._backend_gateway.get_guild_creates(id_of_created_user)
        self.assertEqual(id_of_first_created_guild, two_information_entries[0].guild_id)
        self.assertEqual(id_of_second_created_guild, two_information_entries[1].guild_id)


class TestGetGuildCreatesBasicEntryInformationPresence(BackendPiecesTestFixture):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        new_user_name = "SomeoneSomewhere"
        guild_name_one = "SomeGuildName1"
        guild_name_two = "SomeGuildName2"
        await self.create_user(new_user_name)
        await self.create_guild(guild_name=guild_name_one, username=new_user_name)
        await self.create_guild(guild_name=guild_name_two, username=new_user_name)
        self._id_of_created_user = self._system_state.users.find_id_for_username(new_user_name)
        self._guild_1_id = self._system_state.guilds.find_guild_by_name(guild_name_one).id
        self._guild_2_id = self._system_state.guilds.find_guild_by_name(guild_name_two).id
        self._guild_name_1 = guild_name_one
        self._guild_name_2 = guild_name_two
        guild_create_info_entries = await self._backend_gateway.get_guild_creates(self._id_of_created_user)
        self._guild_create_entry_1 = guild_create_info_entries[0]
        self._guild_create_entry_2 = guild_create_info_entries[1]

    async def test_should_see_ids_of_the_guilds_in_the_entries(self):
        self.assertEqual(self._guild_1_id, self._guild_create_entry_1.guild_id)
        self.assertEqual(self._guild_2_id, self._guild_create_entry_2.guild_id)

    async def test_should_see_names_of_the_guilds_in_the_entries(self):
        self.assertEqual(self._guild_name_1, self._guild_create_entry_1.guild_name)
        self.assertEqual(self._guild_name_2, self._guild_create_entry_2.guild_name)

