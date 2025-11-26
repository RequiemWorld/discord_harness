from . import BackendPiecesTestFixture


class TestUserExistenceLookupWithUserName(BackendPiecesTestFixture):

    async def test_should_return_false_when_no_user_with_given_username_is_in_system(self):
        lookup_result = await self._backend_lookup.lookup_user_existence_by_name("NonExistent555")
        self.assertIs(False, lookup_result)

    async def test_should_return_true_when_user_with_given_username_is_in_system(self):
        await self.create_user("ExistingUser777")
        lookup_result = await self._backend_lookup.lookup_user_existence_by_name("ExistingUser777")
        self.assertIs(True, lookup_result)


class TestGuildExistenceLookupWithGuildName(BackendPiecesTestFixture):
    async def test_should_return_false_when_no_guild_with_given_name_is_in_system(self):
        lookup_result = await self._backend_lookup.lookup_guild_existence_by_name("GuildName")
        self.assertIs(False, lookup_result)

    async def test_should_return_true_when_guild_with_given_name_is_in_system(self):
        await self.create_user_and_guild(username="ArbitraryName", guild_name="MyGuildName")
        lookup_result = await self._backend_lookup.lookup_guild_existence_by_name("MyGuildName")
        self.assertIs(True, lookup_result)