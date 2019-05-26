import discord
from discord.ext import commands

bot_creator_id = 321346463148015626
art_creator_id = 253679155651018764
paypal_link = 'https://paypal.me/h43'
github_link = 'https://github.com/Fytex/H43'
discord_link = 'https://discord.gg/aA4Fjev'


class HelpCommand(commands.MinimalHelpCommand):

    async def prepare_help_command(self, ctx, command):

        if ctx.guild is not None:  # Delete help command in guild

            delete_msg_perm = ctx.channel.permissions_for(ctx.me).manage_messages

            if delete_msg_perm:
                try:  # Message could be instant deleted by another bot.
                    await ctx.message.delete()
                except Exception:
                    pass

        if command is None:

            bot_creator = await ctx.bot.fetch_user(bot_creator_id)
            art_creator = await ctx.bot.fetch_user(art_creator_id)

            donate_msg = f'''
            Honestly, if you could donate me something for this open source project (bot), I would really appreciate that
            \nBot Creator: Fytex -> {bot_creator}
            \nArt Creator: BolachaTM -> {art_creator}\t[Instagram](https://www.instagram.com/amskun/)
            \n[Donate Me]({paypal_link})
            \n[GitHub Repo]({github_link})
            \n[Discord Server]({discord_link})
            '''

            donate_embed = discord.Embed(title='Info', colour=discord.Colour.green())
            donate_embed.set_thumbnail(
                url='https://avatars1.githubusercontent.com/u/25065248?s=400&u=cfb97be8f4eef00e3f11ed883cd8b2b5f98d1ed9&v=4')
            donate_embed.add_field(name='-'*160, value=donate_msg)
            donate_embed.set_footer(text='H43 created by: Fytex')

            self.dm_embed = discord.Embed(title='Commands to use in DM',
                                          colour=discord.Colour.blue())
            self.guild_embed = discord.Embed(
                title='Commands to use in Servers', colour=discord.Colour.red())

            self.donate_embed = donate_embed

    def get_destination(self):
        '''
        Destination to send the help message
        '''
        return self.context.author

    def get_cmd_help(self, cmd):
        '''
        This is not a discord.py method
        '''
        aliases = ' , '.join(cmd.aliases)

        msg = f'**{cmd.qualified_name.capitalize()}**```\n{cmd.brief}\nAliases: {aliases if aliases else None}```'

        return msg

    async def send_cog_help(self, cog):
        pass

    async def send_command_help(self, cmd):
        destination = self.get_destination()

        msg = self.get_cmd_help(cmd)

        await destination.send(msg)

    async def send_group_help(self, group):
        destination = self.get_destination()

        cmds = []

        for cmd in group.commands:

            line = self.get_cmd_help(cmd)

            cmds.append(line)

        msg = '\n'.join(cmds)

        await destination.send(msg)

    async def send_bot_help(self, mapping):
        destination = self.get_destination()
        embeds = [self.dm_embed, self.guild_embed, self.donate_embed]
        cogs = {'Exploit': self.guild_embed, 'Admin_ext': self.dm_embed}

        for cog, cmds in mapping.items():

            if cog is None:
                continue

            embed = cogs.get(cog.qualified_name, None)

            if embed is None:
                continue

            for cmd in cmds:
                embed.add_field(name=cmd.qualified_name.capitalize(), value=cmd.brief)

        for embed in embeds:
            await destination.send(embed=embed)
