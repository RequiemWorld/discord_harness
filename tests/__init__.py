import discord
import asyncio


class EventWaitHelper:
    """
    A helper class for adding an event handler to a bot dynamically,
    and waiting for an event to be triggered, or timing out. No cleanup.
    """
    def __init__(self, asyncio_event: asyncio.Event):
        """
        Use the with_client method, leave construction to internal use.

        :param asyncio_event: The asyncio event that will be set when the handler function is called.
        """
        self._asyncio_event = asyncio_event

    @classmethod
    def using_client(cls, client: discord.Client, event_name: str) -> "EventWaitHelper":
        """
        :param event_name: Name the event as the function would typically be called e.g. on_ready, on_message, etc.
        """
        asyncio_event = asyncio.Event()
        async def my_handler(*args, **kwargs) -> None:
            asyncio_event.set()
        my_handler.__name__ = event_name
        client.event(my_handler)
        return EventWaitHelper(asyncio_event)

    @staticmethod
    async def _wait_for_asyncio_event_or_timeout(event: asyncio.Event, timeout: float) -> None:
        """
        :raises TimeoutError: When the event hasn't been triggered in time.
        """
        wait_with_timeout = asyncio.wait_for(event.wait(), timeout)
        await wait_with_timeout

    async def wait_for_trigger(self, timeout: int | float) -> None:
        """
        :raises TimeoutError: When the event isn't triggered/handled in time.
        """
        await self._wait_for_asyncio_event_or_timeout(self._asyncio_event, timeout)
