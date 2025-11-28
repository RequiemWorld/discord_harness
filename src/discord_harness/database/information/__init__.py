from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ReadyInfo:
    userid: int
    username: str
    unavailable_guild_ids: list[int]


@dataclass(frozen=True, slots=True)
class GuildCreateInfo:
    guild_id: int
    guild_name: str
