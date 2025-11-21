import unittest
from discord_harness.payloads import make_create_channel_for_text


def _make_create_text_channel(id_: int = 555, name: str = "ddeeff", guild_id=2222) -> dict:
    return make_create_channel_for_text(id_=id_, name=name, guild_id=guild_id)


class TestMakingCreateTextChannelPayload(unittest.TestCase):
    def test_should_make_payload_with_given_channel_id(self):
        self.assertEqual(8811, _make_create_text_channel(id_=8811)["id"])

    def test_should_make_payload_with_given_channel_name(self):
        self.assertEqual("Popsicle", _make_create_text_channel(name="Popsicle")["name"])

    def test_should_make_payload_with_given_guild_id(self):
        self.assertEqual(9899, _make_create_text_channel(guild_id=9899)["guild_id"])

    # https://discord.com/developers/docs/resources/channel#channel-object-channel-types
    def test_should_have_right_type_number_for_text_channels(self):
        # GUILD_TEXT	0	a text channel within a server
        self.assertEqual(0, _make_create_text_channel()["type"])
