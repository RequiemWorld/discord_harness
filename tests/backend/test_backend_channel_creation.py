from . import BackendPiecesTestFixture
from discord_harness.backend.interface import TextChannelCreationRequest


class TestBackendGuildsGuildTextChannelCreationSystemState(BackendPiecesTestFixture):

    async def test_should_create_text_channel_with_given_name_in_the_guild_with_matching_name(self):
        await self.create_user_and_guild(username="SomebodySomewhere", guild_name="SomeGuildSomewhere")
        creation_request = TextChannelCreationRequest(guild_name="SomeGuildSomewhere", channel_name="my-channel555")
        await self._backend_guilds.create_text_channel(creation_request)
        # There are only text channels at this time.
        self.assertGuildWithNameHasChannelWithName("my-channel555", "SomeGuildSomewhere")