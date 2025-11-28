from unittest import TestCase
from discord_harness.database import User


class TestUserEntityConstruction(TestCase):
    def setUp(self):
        self._user = User(id_=555, username="RabbitCarrot")

    def test_should_have_id_passed_in_constructor(self):
        self.assertEqual(555, self._user.id)

    def test_should_have_username_passed_in_constructor(self):
        self.assertEqual("RabbitCarrot", self._user.username)
