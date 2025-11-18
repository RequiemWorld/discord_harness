from unittest import TestCase
from discord_harness.backend import User
from discord_harness.backend import Users


class TestAddingNewUsers(TestCase):
    def setUp(self):
        self._users = Users()

    def test_should_be_able_to_add_new_user_and_find_them_in_collection(self):
        user = User(id_=888, username="abcd")
        # We don't need to see the entire collection, and the only method we'll need soon is this one.
        # So the implementation of this test is to just find the user in the collection by username.
        self._users.add_new_user(user)
        self.assertIs(user, self._users.find_by_username("abcd"))


class TestFindingUsersByName(TestCase):
    def setUp(self):
        self._users = Users()

    def test_should_return_none_when_there_is_no_user_with_name_in_collection(self):
        self.assertIsNone(self._users.find_by_username("ArbitraryName"))

    def test_should_be_able_to_find_user_with_given_username_when_there_is_one_in_collection(self):
        user = User(id_=111, username="xyz")
        self.assertEqual("xyz", user.username)


class TestFindingIdByUsername(TestCase):
    def setUp(self):
        self._users = Users()

    def test_should_find_nothing_when_no_user_with_name_exists(self):
        self.assertIsNone(self._users.find_id_for_username("NonExistentName"))

    def test_should_find_id_of_account_when_user_with_name_exists(self):
        user = User(id_=555, username="NonExistentName")
        self._users.add_new_user(user)
        self.assertEqual(555, self._users.find_id_for_username("NonExistentName"))

