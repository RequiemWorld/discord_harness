from . import HarnessPiecesTestFixture
from discord_harness import NoSuchUserError
from discord_harness import NoSuchGuildError


class TestNewGuildMethod(HarnessPiecesTestFixture):

    async def test_should_raise_no_such_user_error_when_no_user_with_owner_name_exists(self):
        with self.assertRaises(NoSuchUserError):
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


class TestJoinGuildMethodErrors(HarnessPiecesTestFixture):
    async def test_should_raise_no_such_guild_error_regardless_to_a_user_with_name_existing_or_not(self):
        await self._harness_users.new_user("ExistingUser")
        with self.assertRaises(NoSuchGuildError):
            await self._harness_guilds.join_guild(guild_name="NotExistingGuild", user_name="ExistingUser")
        with self.assertRaises(NoSuchGuildError):
            await self._harness_guilds.join_guild(guild_name="NotExistingGuild", user_name="NotExistingUser")

    async def test_should_raise_no_such_user_error_when_no_user_with_given_user_name_exists_but_guild_does(self):
        await self._harness_users.new_user("NecessaryOwner")
        # ^ unrelated to our other check, just needed for creating a guild
        await self._harness_guilds.new_guild("GuildName", "NecessaryOwner")
        with self.assertRaises(NoSuchUserError):
            await self._harness_guilds.join_guild(guild_name="GuildName", user_name="NonExistent")


class TestJoinGuildMethodSystemState(HarnessPiecesTestFixture):
    async def test_should_add_member_to_guild_after_joining_them_to_it_with_harness(self):
        await self._harness_users.new_user("NecessaryOwner")
        await self._harness_guilds.new_guild("NecessaryGuild", "NecessaryOwner")
        await self._harness_users.new_user("BotUser123")
        await self._harness_guilds.join_guild("NecessaryGuild", "BotUser123")
        id_of_bot = self._system_state.users.find_id_for_username("BotUser123")
        guild_member_id_list = self._system_state.guilds.find_guild_by_name("NecessaryGuild").members
        self.assertIn(id_of_bot, guild_member_id_list)


class TestCreateChannelMethodSystemState(HarnessPiecesTestFixture):

    async def test_should_make_new_channel_in_guild_after_creating_one_for_it_in_harness(self):
        await self.create_user_and_guild(new_user_name="WhoCares", new_guild_name="ArbitraryGuild")
        await self._harness_guilds.new_channel("ArbitraryGuild", "my-channel123")
        guild_from_state = self._system_state.guilds.find_guild_by_name("ArbitraryGuild")
        self.assertIsNotNone(guild_from_state.find_channel_by_name("my-channel123"))
