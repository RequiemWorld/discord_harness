_GUILD_TEXT = 0

def make_create_channel_for_text(id_: int, name: str, guild_id: int) -> dict:
    return {"id": id_, "type": _GUILD_TEXT, "name": name, "guild_id": guild_id}