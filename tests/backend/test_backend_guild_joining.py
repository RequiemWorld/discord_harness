from . import BackendPiecesTestFixture
from discord_harness.backend.interface import GuildJoinRequest


class TestBackendGuildsGuildJoiningSystemState(BackendPiecesTestFixture):
    async def test_should_place_member_in_guild_in_system_state_after_joining(self):
        await self.create_user_and_guild(username="SomeOtherUser", guild_name="OurTargetGuild")
        await self.create_user("OurUser")
        our_new_user_id = self._system_state.users.find_id_for_username("OurUser")
        guild_join_request = GuildJoinRequest(guild_name="OurTargetGuild", user_name="OurUser")
        await self._backend_guilds.join_guild(guild_join_request)
        self.assertGuildWithNameHasMemberWithId(our_new_user_id, "OurTargetGuild")
