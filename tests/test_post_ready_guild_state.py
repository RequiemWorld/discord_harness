import unittest
import discord
from discord_harness import Harness
from . import EventWaitHelper


class TestClientStateGuildInfoAfterOnReady(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = discord.Client(intents=discord.Intents.default())
        self.harness = Harness()
        self._ready_event_wait_helper = EventWaitHelper.using_client(self.client, "on_ready")
        await self.harness.users.new_user("Name123")
        await self.harness.initialize(self.client, "Name123")
        await self._ready_event_wait_helper.wait_for_trigger(3)

    async def test_should_see_no_guilds_on_client_after_ready_event_from_initializing_when_not_in_any(self):
        self.assertEqual(0, len(self.client.guilds))
