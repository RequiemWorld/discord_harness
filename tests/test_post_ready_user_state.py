import unittest
import discord
from discord_harness import Harness
from . import EventWaitHelper


class TestClientStateUserInfoAfterOnReady(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = discord.Client(intents=discord.Intents.default())
        self.harness = Harness()
        self._ready_event_wait_helper = EventWaitHelper.using_client(self.client, "on_ready")

    async def test_should_see_right_username_on_client_after_ready_event_from_initializing(self):
        await self.harness.users.new_user("DecemberSnow")
        await self.harness.initialize(self.client, "DecemberSnow")
        await self._ready_event_wait_helper.wait_for_trigger(3)
        self.assertEqual("DecemberSnow", self.client.user.name)

    async def test_should_see_right_discord_id_on_client_after_ready_event_from_initializing(self):
        # We're not doing anything with it yet, so we'll just expect 555222333 for now.
        await self.harness.users.new_user("OctoberLeaves")
        await self.harness.initialize(self.client, "OctoberLeaves")
        await self._ready_event_wait_helper.wait_for_trigger(3)
        self.assertEqual(555222333, self.client.user.id)

    async def test_should_see_self_as_on_a_bot_account_after_ready_event_from_initializing(self):
        await self.harness.users.new_user("MyName12345")
        await self.harness.initialize(self.client, "MyName12345")
        await self._ready_event_wait_helper.wait_for_trigger(3)
        self.assertTrue(self.client.user.bot)
