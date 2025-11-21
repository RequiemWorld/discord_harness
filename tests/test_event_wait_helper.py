import asyncio
import unittest
from . import EventWaitHelper



class TestEventWaitHelperTriggerWaiting(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self._asyncio_event = asyncio.Event()
        self._wait_helper = EventWaitHelper(self._asyncio_event)

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


class TestEventWaitHelperConstruction(unittest.TestCase):
    def setUp(self):
        self._wait_helper = EventWaitHelper(asyncio.Event())

    def test_should_have_none_for_args_by_default(self):
        self.assertIsNone(self._wait_helper.args)
