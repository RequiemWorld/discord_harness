import unittest
from discord_harness.payloads import make_ready_payload


def _make_payload(guilds: list[int] | None = None, username: str | None = None) -> dict:
    guilds = guilds if guilds is not None else []
    username = "DefaultName1234" if username is None else username
    return make_ready_payload(guild_ids=guilds, username=username)


class TestGatewayReadyPayloadCreationGuildData(unittest.TestCase):
    """
    The ready event data should contain a list of data for "unavailable guilds",
    that is a list of ids of guilds to be streamed in to the client, and a {unavailable: true}.
    """
    # "guilds are the guilds of which your bot is a member. They start out as unavailable when you connect to the gateway. As they become available, your bot will be notified via Guild Create events."
    def test_should_have_empty_list_for_guilds_when_no_guild_ids_provided(self):
        payload = _make_payload(guilds=[])
        self.assertEqual([], payload["guilds"])
        self.assertIsInstance(payload["guilds"], list)

    def test_should_have_guilds_in_list_containing_their_ids_when_ids_provided(self):
        # https://discord.com:2087/developers/docs/events/gateway-events#ready
        # A list of unavailable guild objects, they'll have the id under the "id" key
        payload = _make_payload(guilds=[9, 15])
        self.assertEqual(9, payload["guilds"][0]["id"])
        self.assertEqual(15, payload["guilds"][1]["id"])

    def test_should_have_guilds_in_list_containing_unavailable_set_to_true_when_ids_provided(self):
        # https://discord.com:2087/developers/docs/events/gateway-events#ready
        # A list of unavailable guild objects, they'll have the true under the "unavailable" key
        # Each guild the client will see come in through GUILD_CREATE events is placed here.
        payload = _make_payload(guilds=[25, 30])
        self.assertTrue(payload["guilds"][0]["unavailable"])
        self.assertTrue(payload["guilds"][1]["unavailable"])


class TestGatewayReadyPayloadCreationUserData(unittest.TestCase):

    def test_should_fill_in_id_field_with_fixed_value_of_555222333(self):
        # We aren't doing anything with this yet, so we're giving it a fixed number to fill in.
        user_data = _make_payload()["user"]
        # Not even bothering to try to give this a valid snowflake ID to start.
        self.assertEqual(555222333, user_data["id"])

    def test_should_fill_in_username_field_with_value_given_in_function_call(self):
        # "the user's username, not unique across the platform", bots still use discriminators.
        user_data = _make_payload(username="MyName123")["user"]
        self.assertEqual("MyName123", user_data["username"])

    def test_should_fill_in_discriminator_field_with_string_value_of_5001(self):
        # bots still use discriminators
        user_data = _make_payload()["user"]
        self.assertEqual("5001", user_data["discriminator"])

    def test_should_fill_in_avatar_with_arbitrary_16_byte_hexadecimal_value(self):
        # >>> secrets.token_hex(16)
        # '6209f9e346b1ba4f4ca6d373bafb860b'
        # It shouldn't matter what value this is, but it MUST be present for discord.py to work with it.
        user_data = _make_payload()["user"]
        self.assertEqual("6209f9e346b1ba4f4ca6d373bafb860b", user_data["avatar"])