import unittest
from discord_harness.backend import Guild
from discord_harness.backend import GuildChannel


class TestGuildChannelConstruction(unittest.TestCase):
    def setUp(self):
        self._empty_channel = GuildChannel(id_=5556, name="channel-name")

    def test_should_have_id_passed_to_constructor(self):
        self.assertEqual(5556, self._empty_channel.id)

    def test_should_have_name_passed_to_constructor(self):
        self.assertEqual("channel-name", self._empty_channel.name)


class EmptyGuildTestFixture(unittest.TestCase):
    def setUp(self):
        self._empty_guild = Guild(123, "NameGuild", 456)


class TestGuildEntityConstruction(EmptyGuildTestFixture):

    def test_should_have_name_id_to_constructor(self):
        self.assertEqual(123, self._empty_guild.id)

    def test_should_have_name_passed_to_constructor(self):
        self.assertEqual("NameGuild", self._empty_guild.name)

    def test_should_have_owner_id_passed_to_constructor(self):
        self.assertEqual(456, self._empty_guild.owner_id)

    def test_should_contain_no_members_by_default(self):
        self.assertEqual([], self._empty_guild.members)

    def test_should_contain_no_channels_by_default(self):
        self.assertEqual([], self._empty_guild.channels)


class TestAddingMembersToGuild(EmptyGuildTestFixture):

    def test_should_be_able_to_add_member_id_to_guild_and_see_it_after(self):
        self._empty_guild.members.append(5000)
        self.assertIn(5000, self._empty_guild.members)


class TestAddingChannelsToGuild(EmptyGuildTestFixture):
    def test_should_be_able_to_add_channel_to_guild_and_see_it_after(self):
        channel = GuildChannel(id_=8888, name="name123")
        self._empty_guild.channels.append(channel)
        self.assertIn(channel, self._empty_guild.channels)