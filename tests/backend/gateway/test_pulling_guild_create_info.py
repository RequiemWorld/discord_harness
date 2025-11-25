from .. import BackendPiecesTestFixture


class TestPullingGuildCreateInfoBasicInformationByGuildId(BackendPiecesTestFixture):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        # As of November 23rd 2025 there is no code on this backend to join a user to a guild,
        # but the intended behavior of creating a guild is to have the owner already added to it.
        await self.create_user_and_guild(username="OwnerOfGuild", guild_name="OwnedGuild")
        self._id_of_guild_new_user_is_in = self._system_state.guilds.find_guild_by_name("OwnedGuild").id
        self._create_info = await self._backend_gateway.get_guild_create(self._id_of_guild_new_user_is_in)

    async def test_should_see_guild_id_in_guild_create_info(self):
        self.assertEqual(self._id_of_guild_new_user_is_in, self._create_info.guild_id)

    async def test_should_see_guild_name_in_guild_create_info(self):
        self.assertEqual("OwnedGuild", self._create_info.guild_name)
