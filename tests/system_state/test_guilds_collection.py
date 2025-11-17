# Possibly using the word "collection", loosely here.
import unittest
from discord_harness.backend import Guild
from discord_harness.backend import Guilds


def _make_guild(id_: int, name: str = "Name123" , owner_id = 566777) -> Guild:
    return Guild(id_, name, owner_id)


class TestAddingNewGuild(unittest.TestCase):
    def setUp(self):
        self._guilds = Guilds()

    def test_should_be_able_to_see_guild_in_guilds_after_adding(self):
        new_guild = Guild(124, "name", 555)
        self._guilds.add_new_guild(new_guild)
        self.assertIn(new_guild, self._guilds.get_all_guilds())


class TestGettingAllGuilds(unittest.TestCase):
    def setUp(self):
        self._guilds = Guilds()

    def test_should_get_empty_list_back_when_no_guilds_have_been_added(self):
        self.assertEqual([], self._guilds.get_all_guilds())

    def test_should_get_list_of_only_guild_added_after_one_has_been_added(self):
        guild_one = _make_guild(id_=1)
        self._guilds.add_new_guild(guild_one)
        self.assertEqual([guild_one], self._guilds.get_all_guilds())

    def test_should_get_list_of_the_multiple_guilds_added_when_some_have_been_added(self):
        guild_one = _make_guild(id_=1)
        guild_two = _make_guild(id_=2)
        guild_three = _make_guild(id_=3)
        self._guilds.add_new_guild(guild_one)
        self._guilds.add_new_guild(guild_two)
        self._guilds.add_new_guild(guild_three)
        self.assertEqual([guild_one, guild_two, guild_three], self._guilds.get_all_guilds())

    def test_should_get_copy_of_list_of_added_guilds_and_not_original(self):
        # The guilds inside the list should be mutable, the list for the system state, not.
        arbitrary_guild = _make_guild(277)
        self._guilds.get_all_guilds().append(arbitrary_guild)
        self.assertNotIn(arbitrary_guild, self._guilds.get_all_guilds())


class TestGettingGuildsContainingMemberWithId(unittest.TestCase):
    def setUp(self):
        self._guilds = Guilds()

    def test_should_be_able_to_find_only_guild_containing_member_when_they_are_in_one(self):
        guild = _make_guild(1)
        guild.members.append(200)
        self._guilds.add_new_guild(guild)
        self.assertEqual([guild], self._guilds.get_guilds_by_member_id(200))

    def test_should_be_unable_to_find_anything_when_there_are_no_guilds_to_begin_with(self):
        self.assertEqual([], self._guilds.get_guilds_by_member_id(400))

    def test_should_be_unable_to_find_anything_when_there_are_guilds_but_none_containing_member(self):
        self._guilds.add_new_guild(_make_guild(1))
        self._guilds.add_new_guild(_make_guild(2))
        self._guilds.add_new_guild(_make_guild(3))
        self.assertEqual([], self._guilds.get_guilds_by_member_id(400))

    def test_should_be_unable_to_find_anything_when_there_is_a_guild_with_a_member_but_not_with_given_id(self):
        guild = _make_guild(1)
        guild.members.append(50)
        self._guilds.add_new_guild(guild)
        self.assertEqual([], self._guilds.get_guilds_by_member_id(25))
