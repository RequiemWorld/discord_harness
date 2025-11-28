import unittest
from discord_harness.database import Guild
from discord_harness.database import GuildChannel
from discord_harness.database import GuildMessage


class EmptyGuildChannelTestFixture(unittest.TestCase):
    def setUp(self):
        self._empty_channel = GuildChannel(id_=5556, name="channel-name")


class TestGuildMessageConstruction(unittest.TestCase):
    def setUp(self):
        self._arbitrary_message = GuildMessage(id_=1234, author_id=111222, content="Hello World")
    def test_should_have_id_passed_to_constructor(self):
        self.assertEqual(1234, self._arbitrary_message.id)

    def test_should_have_author_id_passed_to_constructor(self):
        self.assertEqual(111222, self._arbitrary_message.author_id)

    def test_should_have_content_passed_to_constructor(self):
        self.assertEqual("Hello World", self._arbitrary_message.content)


class TestGuildChannelConstruction(EmptyGuildChannelTestFixture):

    def test_should_have_id_passed_to_constructor(self):
        self.assertEqual(5556, self._empty_channel.id)

    def test_should_have_name_passed_to_constructor(self):
        self.assertEqual("channel-name", self._empty_channel.name)

    def test_should_contain_no_messages_by_default(self):
        self.assertEqual([], self._empty_channel.messages)

class TestAddingMessagesToGuildChannel(EmptyGuildChannelTestFixture):

    def test_should_be_able_to_add_message_to_channel_and_see_it_after(self):
        new_message = GuildMessage(id_=12345, author_id=222, content="Goodbye World")
        self._empty_channel.messages.append(new_message)
        self.assertIn(new_message, self._empty_channel.messages)


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

class TestFindingChannelInGuildByName(EmptyGuildTestFixture):

    def test_should_not_find_a_channel_when_none_with_given_name_are_present(self):
        self.assertIsNone(self._empty_guild.find_channel_by_name(name="NoExistence"))

    def test_should_find_channel_with_given_name_when_exactly_one_is_present(self):
        channel = GuildChannel(id_=4, name="channel-name")
        self._empty_guild.channels.append(channel)
        self.assertIs(channel, self._empty_guild.find_channel_by_name("channel-name"))