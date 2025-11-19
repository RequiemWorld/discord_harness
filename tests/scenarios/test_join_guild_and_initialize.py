import discord
import unittest
from discord_harness import Harness
from .. import EventWaitHelper


class TestSeeingJoinedGuildInfoAfterInitialize(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = discord.Client(intents=discord.Intents.default())
        self.harness = Harness()
        self._ready_event_wait_helper = EventWaitHelper.using_client(self.client, "on_ready")

    async def test_should_see_names_of_joined_guilds_in_list_after_ready_event_handled(self):
        await self.harness.users.new_user(name="User1")
        await self.harness.guilds.new_guild(guild_name="Guild 1", owner_name="User1")
        await self.harness.guilds.new_guild(guild_name="Guild 2", owner_name="User1")
        await self.harness.users.new_user(name="MyBotName")
        await self.harness.guilds.join_guild("Guild 1", "MyBotName")
        await self.harness.guilds.join_guild("Guild 2", "MyBotName")
        await self.harness.initialize(self.client, "MyBotName")
        await self._ready_event_wait_helper.wait_for_trigger(3)
        self.assertEqual("Guild 1", self.client.guilds[0].name)
        self.assertEqual("Guild 2", self.client.guilds[1].name)