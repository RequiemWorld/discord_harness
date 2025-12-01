import unittest
from unittest.mock import create_autospec
from discord_harness.database import MockGatewayInformationPuller
from discord_harness.database.information import GuildCreateInfo


class TestSettingGuildCreateInfoResults(unittest.TestCase):
    def setUp(self):
        self._info_puller = MockGatewayInformationPuller()

    def test_should_be_able_to_set_result_for_getting_guild_create_info_for_guild_with_id(self):
        fake_guild_info = create_autospec(GuildCreateInfo)
        self._info_puller.set_result_for_guild_id(guild_id=888999, result=fake_guild_info)
        self.assertIs(fake_guild_info, self._info_puller.pull_guild_create_info_for_guild(888999))

    def test_should_get_none_as_result_when_no_result_has_been_setup_for_given_guild_id(self):
        self.assertIsNone(self._info_puller.pull_guild_create_info_for_guild(12345))

    def test_should_be_able_to_get_right_result_when_some_are_set_for_multiple_guild_ids(self):
        fake_guild_info_1 = create_autospec(GuildCreateInfo)
        fake_guild_info_2 = create_autospec(GuildCreateInfo)
        self._info_puller.set_result_for_guild_id(guild_id=1111, result=fake_guild_info_1)
        self._info_puller.set_result_for_guild_id(guild_id=9999, result=fake_guild_info_2)
        self.assertIs(fake_guild_info_1, self._info_puller.pull_guild_create_info_for_guild(1111))
        self.assertIs(fake_guild_info_2, self._info_puller.pull_guild_create_info_for_guild(9999))

    def test_should_still_get_none_for_ones_with_nothing_setup_when_some_are_set_for_multiple_guild_ids(self):
        fake_guild_info_1 = create_autospec(GuildCreateInfo)
        fake_guild_info_2 = create_autospec(GuildCreateInfo)
        self._info_puller.set_result_for_guild_id(guild_id=4444, result=fake_guild_info_1)
        self._info_puller.set_result_for_guild_id(guild_id=5555, result=fake_guild_info_2)
        self.assertIsNone(self._info_puller.pull_guild_create_info_for_guild(9999))