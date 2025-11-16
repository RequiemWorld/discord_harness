

def make_ready_payload(username: str, guild_ids: list[int]) -> dict:
    """
    Makes the payload the client should receive after connecting to the gateway,
    with a list of each 'unavailable guild' id the bot is in, and default values for everything else.
    """
    user_data = {
        "id": 555222333,
        "username": username,
        "discriminator": "5001",
        "avatar": "6209f9e346b1ba4f4ca6d373bafb860b",
    }
    unavailable_guilds = []
    for guild_id in guild_ids:
        # "guilds are the guilds of which your bot is a member. They start out as unavailable when you connect to the gateway. As they become available, your bot will be notified via Guild Create events."
        unavailable_guilds.append({"id": guild_id, "unavailable": True})
    return {"guilds": unavailable_guilds, "user": user_data}