import asyncio
import unittest
import discord
from . import EventWaitHelper



class TestEventWaitHelperTriggerWaiting(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self._asyncio_event = asyncio.Event()
        async def _arbitrary_coroutine():
            pass

        self._wait_helper = EventWaitHelper(self._asyncio_event, _arbitrary_coroutine)

    async def test_should_return_normally_when_event_triggered_prior(self):
        self._asyncio_event.set()
        await self._wait_helper.wait_for_trigger(0.005)

    async def test_should_timeout_when_the_event_is_not_triggered_in_time(self):
        with self.assertRaises(TimeoutError):
            await self._wait_helper.wait_for_trigger(0.005)

    async def test_should_return_normally_when_event_is_triggered_in_time(self):
        async def _trigger_event() -> None:
            self._asyncio_event.set()
        # The coroutine to wait for the trigger should be awaited, then after the one to trigger the event.
        # this is what should happen under real conditions.
        waiting_awaitable = self._wait_helper.wait_for_trigger(0.005)
        await asyncio.gather(*[waiting_awaitable, _trigger_event()])


class TestEventWaitHelperConstruction(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        async def _arbitrary_handling_thing() -> None:
            pass
        self._wait_helper = EventWaitHelper(asyncio.Event(), _arbitrary_handling_thing)
        self._arbitrary_handling_thing = _arbitrary_handling_thing

    def test_should_have_none_for_args_by_default(self):
        self.assertIsNone(self._wait_helper.args)

    def test_should_have_coroutine_given_for_handler_property(self):
        self.assertIs(self._arbitrary_handling_thing, self._wait_helper.handler)


class TestEventWaitHelperDiscordClientUsageIntegration(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        client = discord.Client(intents=discord.Intents.default())
        self._wait_helper = EventWaitHelper.using_client(client, "on_ready")

    async def test_should_see_arguments_passed_to_event_handler_when_done_once(self):
        await self._wait_helper.handler("aa", "b")
        self.assertEqual(("aa", "b"), self._wait_helper.args)