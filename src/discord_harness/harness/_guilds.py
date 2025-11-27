from ._errors import NoSuchUserError
from ._errors import NoSuchGuildError
from discord_harness import GuildJoinRequest
from discord_harness import GuildCreationRequest
from discord_harness import DiscordBackendGuilds
from discord_harness import DiscordBackendLookup
from discord_harness import TextChannelCreationRequest


class HarnessGuilds:
    def __init__(self, guilds: DiscordBackendGuilds, lookup: DiscordBackendLookup):
        self._guilds = guilds
        self._lookup = lookup

    async def new_guild(self, guild_name: str, owner_name: str) -> None:
        """
        :raises NoSuchUserError: When the there is no user in the system with the given owner name.
        """
        # Maybe the backend should be giving this error under the same condition instead
        if not await self._lookup.lookup_user_existence_by_name(owner_name):
            raise NoSuchUserError(f"no user with the name {owner_name} could be found in system")
        guild_creation_request = GuildCreationRequest(guild_name=guild_name, guild_owner_name=owner_name)
        await self._guilds.create_guild(guild_creation_request)

    # I don't like the look of guild_name, and then username even though username is one word.
    async def join_guild(self, guild_name: str, user_name: str) -> None:
        """
        :param guild_name: Name of the guild that the user will be added to.
        :param user_name: Name of the user that will be added to the guild.
        :raises NoSuchUserError: When name of guild exists, but name of user doesn't.
        :raises NoSuchGuildError: When name of guild exists, regardless to the existence of the user.
        """
        # TODO figure out broadly what to do regarding multiple guilds with the same name
        guild_with_name_exists = await self._lookup.lookup_guild_existence_by_name(guild_name)
        if not guild_with_name_exists:
            raise NoSuchGuildError(f"no guild with the name {guild_name} could be found")
        user_with_name_exists = await self._lookup.lookup_user_existence_by_name(user_name)
        if not user_with_name_exists:
            raise NoSuchUserError(f"no user with the username {user_name} could be found")
        guild_join_request = GuildJoinRequest(guild_name, user_name)
        # Maybe change above error handling/make the backend raise the same errors instead.
        await self._guilds.join_guild(guild_join_request)

    async def new_channel(self, guild_name: str, channel_name: str) -> None:
        """
        Effectively creates a public channel in the given guild name.

        :param guild_name: Name of the guild the channel should be created in.
        :param channel_name: Name of the channel to create in the guild.
        """
        new_channel_request = TextChannelCreationRequest(guild_name=guild_name, channel_name=channel_name)
        await self._guilds.create_text_channel(new_channel_request)
