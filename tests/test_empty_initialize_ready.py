import discord
import unittest
from discord_harness import Harness
from tests import EventWaitHelper


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
