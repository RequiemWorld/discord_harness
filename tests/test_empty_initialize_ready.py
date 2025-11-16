import asyncio
import discord
import unittest
from discord_harness import Harness


async def _wait_for_asyncio_event_or_timeout(event: asyncio.Event, timeout: float) -> None:
    """
    :raises TimeoutError: When the event hasn't been triggered in time.
    """
    wait_with_timeout = asyncio.wait_for(event.wait(), timeout)
    await wait_with_timeout


class TestOnReadyEventAfterSimpleInitialization(unittest.IsolatedAsyncioTestCase):

    async def test_should_await_on_ready_handler_at_some_point_after_initializing_when_added_to_no_guilds(self):
        # We don't have any guilds, we barely have any user logic. But if we await initialize,
        # then at some point our on_ready handler should be awaited.
        client = discord.Client(intents=discord.Intents.default())
        trigger = asyncio.Event()
        @client.event
        async def on_ready() -> None:
            trigger.set()
        harness = Harness()
        await harness.users.new_user("November")
        await harness.initialize(client, "November")
        # discord.py tends to take 2 seconds to trigger on ready, even when there are no guilds.
        await _wait_for_asyncio_event_or_timeout(trigger, 5)
