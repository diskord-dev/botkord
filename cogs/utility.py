import diskord
from diskord.ext import commands
from typing import Union

# Constants
DKC_GUILD_ID = 887217168276656188

class Utility(commands.Cog):
    """
    A cog that contains commands made to make the life easier.
    """
    def __init__(self, bot: diskord.Bot):
        self.bot = bot

    @diskord.slash_command()
    @diskord.slash_option('id', description='The ID of issue')
    @diskord.slash_option('repo', description='The repo to get the issue from.',
        choices=[
            diskord.OptionChoice(name='diskord', value='diskord'),
            diskord.OptionChoice(name='diskord.github.io', value='diskord.github.io'),
            diskord.OptionChoice(name='guide', value='guide'),
            diskord.OptionChoice(name='botkord', value='botkord')
        ]
    )
    @diskord.slash_option('private', description='Whether to send private (ephemeral) response or not.')
    async def issue(self, ctx: diskord.InteractionContext, id: int, repo: str = 'diskord', private: bool = False):
        """Quickly get link to a GitHub issue or a PR on repos of diskord-dev organization."""
        await ctx.send(f'https://github.com/diskord-dev/{repo}/issues/{id}', ephemeral=private)

    @diskord.slash_command()
    async def getinfo(self, ctx: diskord.InteractionContext):
        """Get info about a user, guild or other entities."""
        pass

    @getinfo.sub_command()
    @diskord.slash_option('user', arg='user_value', description='The user to get info of.')
    @diskord.slash_option('private', description='Whether to respond privately.')
    async def user(self,
        ctx: diskord.InteractionContext,
        user_value: Union[diskord.Member, diskord.User],
        private: bool = False,
        ):
        """Get info about a user."""
        # all my hopes are with you in reading this code. Sorry for spaghetti.
        embed = diskord.Embed(title=':information_source: Information for %s' % str(user_value))
        embed.add_field(name='ID', value=user_value.id, inline=False)
        embed.add_field(name='Registered at', inline=False, value='<t:{0}:R> @ <t:{0}>'.format(round(user_value.created_at.timestamp())))
        embed.add_field(name='Joined at', inline=False, value='<t:{0}:R> @ <t:{0}>'.format(round(user_value.joined_at.timestamp())))
        embed.add_field(name='URLs (if available)', inline=False, value=f'- [Avatar]({getattr(user_value.avatar, "url", user_value.default_avatar.url)})\n- [Banner]({getattr(user_value.banner, "url", None)})')
        embed.set_thumbnail(url=getattr(user_value.avatar, 'url', user_value.default_avatar.url))
        embed.color = user_value.color

        await ctx.send(embed=embed, ephemeral=private)

    @diskord.slash_command()
    @diskord.slash_option('command', arg='command_name', description='The command to get info about.')
    @diskord.slash_option('private', description='Show help privately as ephemeral message.')
    async def help(self, ctx, command_name: str, private: bool = False):
        """Get info about a specific command."""
        command = None
        for cmd in self.bot.application_commands.values():
            if cmd.name == command_name:
                command = cmd
                break

        if command is None:
            await ctx.send(':x: Command not found.')

        embed = diskord.Embed(title=':information_source: `{}`'.format(command_name))
        embed.description = command.description

        if command.children:
            embed.add_field(name='Subcommands/Groups', value='\n'.join(f'`{child.name}`' for child in command.children))
        else:
            options = '\n'.join([f'`{opt.name}`{" (required)" if opt.required else ""}: {opt.description}' for opt in command.options])
            if command.options:
                embed.add_field(name='Options', value=options)

        await ctx.send(embed=embed, ephemeral=private)

def setup(bot):
    bot.add_cog(Utility(bot))
    print('[cogs.utility]: Loaded')

