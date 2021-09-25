from typing import Union

import diskord
from diskord.ext import commands

from ._errors import NotDKC

# Constants
DKC_GUILD_ID = 887217168276656188
ROLES = {
    'lib_updates_stable': 887758497322762261,
    'lib_updates_dev': 887758408944586763,
    'guild_news': 888090832748576818,
    'tester': 888820705578344468,
}

class DKC(commands.Cog):
    """
    A cog that contains commands made only for Diskord's official server. These commands
    cannot be used outside DKC server.
    """
    def __init__(self, bot: diskord.Bot):
        self.bot = bot

    def _check_dkc(self, ctx: Union[diskord.InteractionContext, commands.Context]):
        # this will be changed into a real check once checks
        # are supported on application commands.
        dkc = ctx.guild.id == DKC_GUILD_ID
        if not dkc:
            raise NotDKC('This command is not available outside Diskord official server.')

        return dkc

    @diskord.slash_command(guild_ids=[DKC_GUILD_ID])
    async def notifications(self, ctx: diskord.InteractionContext):
        """Manage the notifications you want to recieve."""
        pass

    @notifications.sub_command()
    @diskord.slash_option(
        'to', arg='notification_type', description='The notification to subscribe to', choices=[
            diskord.OptionChoice(name='Library Updates (Stable)', value='lib_updates_stable'),
            diskord.OptionChoice(name='Library Updates (Development)', value='lib_updates_dev'),
            diskord.OptionChoice(name='Server News', value='guild_news'),
            diskord.OptionChoice(name='Tester', value='tester'),
        ])
    async def subscribe(self, ctx: diskord.InteractionContext, notification_type: str):
        """Subscribe to a notification."""
        role = ctx.guild.get_role(ROLES[notification_type])
        await ctx.author.add_roles(role)

        embed = diskord.Embed(
            title=f':white_check_mark: Added notification role: **{role.name}**',
            description='You will now recieve notifications when there is a relevant event to this role',
            color=diskord.Color.green(),
            )

        await ctx.send(embed=embed, ephemeral=True)

    @notifications.sub_command()
    @diskord.slash_option(
        'to', arg='notification_type', description='The notification to unsubscribe to', choices=[
            diskord.OptionChoice(name='Library Updates (Stable)', value='lib_updates_stable'),
            diskord.OptionChoice(name='Library Updates (Development)', value='lib_updates_dev'),
            diskord.OptionChoice(name='Tester', value='tester'),
        ])
    async def unsubscribe(self, ctx: diskord.InteractionContext, notification_type: str):
        """Unsubscribe to a notification."""
        role = ctx.guild.get_role(ROLES[notification_type])
        await ctx.author.remove_roles(role)

        embed = diskord.Embed(
            title=f':eject: Removed notification role: **{role.name}**',
            description='You will not recieve notifications regarding this role anymore.',
            color=diskord.Color.blue(),
            )

        await ctx.send(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(DKC(bot))
    print('[cogs.dkc]: Loaded')

