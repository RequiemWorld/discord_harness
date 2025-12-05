import unittest
from discord_harness.database import Guild
from discord_harness.database import SystemState
from discord_harness.database import SystemStateGatewayInformationPuller


class TestGuildCreateInfoPullingMethod(unittest.TestCase):
    def setUp(self):
        self._state = SystemState()
        self._puller = SystemStateGatewayInformationPuller(self._state)

    def test_should_return_none_when_no_guild_with_given_id_exists(self):
        self.assertIsNone(self._puller.pull_guild_create_info_for_guild(5001))


class TestGuildCreatePullInfoCorrectness(unittest.TestCase):
    def setUp(self):
        self._state = SystemState()
        self._puller = SystemStateGatewayInformationPuller(self._state)
        always_existing_guild = Guild(id_=999444555, name="SomeGuild", owner_id=111444555)
        self._state.guilds.add_new_guild(always_existing_guild)
        self._pull_result = self._puller.pull_guild_create_info_for_guild(999444555)

    def test_should_return_result_with_right_guild_id(self):
        self.assertEqual(999444555, self._pull_result.guild_id)

    def test_should_return_result_with_right_guild_name(self):
        self.assertEqual("SomeGuild", self._pull_result.guild_name)
