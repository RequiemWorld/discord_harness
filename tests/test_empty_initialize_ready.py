import discord
import unittest
from discord_harness import Harness
from . import EventWaitHelper


class TestOnReadyEventAfterSimpleInitialization(unittest.IsolatedAsyncioTestCase):

    async def test_should_await_on_ready_handler_at_some_point_after_initializing_when_added_to_no_guilds(self):
        # We don't have any guilds, we barely have any user logic. But if we await initialize,
        # then at some point our on_ready handler should be awaited.
        client = discord.Client(intents=discord.Intents.default())
        wait_helper = EventWaitHelper.using_client(client, event_name="on_ready")
        harness = Harness()
        await harness.users.new_user("November")
        await harness.initialize(client, "November")
        # discord.py tends to take 2 seconds to trigger on ready, even when there are no guilds.
        await wait_helper.wait_for_trigger(3)

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

