import unittest
from discord_harness.database import User
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


# FIXME These are somewhat difficult to write and not well factored. Codebase needs restructuring and fixing ASAP.
class TestReadyInfoPullMethod(unittest.TestCase):
    def setUp(self):
        self._state = SystemState()
        self._puller = SystemStateGatewayInformationPuller(self._state)
        always_existing_user = User(id_=444888, username="SomeName")
        self._state.users.add_new_user(always_existing_user)

    def test_should_raise_value_error_when_user_with_id_does_not_exist(self):
        with self.assertRaises(ValueError):
            self._puller.pull_ready_info_for_user(user_id=222333)

    def test_should_return_result_with_empty_unavailable_guild_ids_list_when_user_not_in_any(self):
        ready_info = self._puller.pull_ready_info_for_user(444888)
        self.assertEqual([], ready_info.unavailable_guild_ids)

    def test_should_return_result_with_unavailable_guild_ids_containing_every_guild_user_is_in(self):
        guild_one = Guild(id_=1234, name="Guild1", owner_id=999)
        guild_two = Guild(id_=5678, name="Guild2", owner_id=999)
        guild_one.members.append(444888)
        guild_two.members.append(444888)
        self._state.guilds.add_new_guild(guild_one)
        self._state.guilds.add_new_guild(guild_two)
        self.assertEqual({1234, 5678}, set(self._puller.pull_ready_info_for_user(444888).unavailable_guild_ids))

    def test_should_return_result_with_right_userid(self):
        self.assertEqual(444888, self._puller.pull_ready_info_for_user(444888).userid)

    def test_should_return_result_with_right_username(self):
        self.assertEqual("SomeName", self._puller.pull_ready_info_for_user(444888).username)

