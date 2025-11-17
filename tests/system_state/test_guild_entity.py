import unittest
from discord_harness.backend import Guild


class TestGuildEntityConstruction(unittest.TestCase):
    def setUp(self):
        self._empty_guild = Guild(123, "NameGuild", 456)

    def test_should_have_name_id_to_constructor(self):
        self.assertEqual(123, self._empty_guild.id)

    def test_should_have_name_passed_to_constructor(self):
        self.assertEqual("NameGuild", self._empty_guild.name)

    def test_should_have_owner_id_passed_to_constructor(self):
        self.assertEqual(456, self._empty_guild.owner_id)

    def test_should_contain_no_members_by_default(self):
        self.assertEqual([], self._empty_guild.members)


class TestAddingMembersToGuild(unittest.TestCase):
    def setUp(self):
        self._empty_guild = Guild(123, "NameGuild", 456)

    def test_should_be_able_to_add_member_id_to_guild_and_see_it_after(self):
        self._empty_guild.members.append(5000)
        self.assertIn(5000, self._empty_guild.members)