from . import BackendPiecesTestFixture
from discord_harness.backend.interface import GuildCreationRequest


class TestBackendGuildsGuildCreationSystemState(BackendPiecesTestFixture):

    async def test_should_create_guild_in_system_state_with_name_specified_in_request(self):
        await self.create_user("NonSense")
        creation_request = GuildCreationRequest(guild_name="My Guild Name", guild_owner_name="NonSense")
        await self._backend_guilds.create_guild(creation_request)
        self.assertIsNotNone(self._system_state.guilds.find_guild_by_name("My Guild Name"))

    async def test_should_create_guild_in_system_state_with_id_given_by_call_to_next_id(self):
        await self.create_user("WhateverName")
        creation_request = GuildCreationRequest(guild_name="Whatever Guild Name", guild_owner_name="WhateverName")
        self.override_next_id_indefinitely(9991)
        await self._backend_guilds.create_guild(creation_request)
        guild_with_name = self._system_state.guilds.find_guild_by_name("Whatever Guild Name")
        self.assertEqual(9991, guild_with_name.id)

    async def test_should_create_guild_in_system_state_with_owner_id_for_given_username(self):
        # This should be fine in the future, usernames for non-bot users should be unique.
        await self.create_user("MyName")
        creation_request = GuildCreationRequest(guild_name="AnotherGuild", guild_owner_name="MyName")
        await self._backend_guilds.create_guild(creation_request)
        created_user_id = self._system_state.users.find_id_for_username("MyName")
        created_guild_owner_id = self._system_state.guilds.find_guild_by_name("AnotherGuild").owner_id
        self.assertEqual(created_user_id, created_guild_owner_id)
