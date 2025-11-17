# Possibly using the word "collection", loosely here.
import unittest
from discord_harness.backend import Guilds


class TestGettingAllGuilds(unittest.TestCase):
    def setUp(self):
        self._guilds = Guilds()

    def test_should_get_empty_list_back_when_no_guilds_have_been_added(self):
        self.assertEqual([], self._guilds.get_all_guilds())