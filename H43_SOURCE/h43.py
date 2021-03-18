import json
import discord
import sys
from os import path
from discord.ext import commands
from extras.help import HelpCommand
from configparser import ConfigParser


extensions = ['exploit', 'admin_ext', 'error_handler']


def extras_path(relative_path):

    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        from sys import _MEIPASS as base_path
    except ImportError:
        base_path = path.dirname(path.abspath(__file__))

    return path.join(base_path, 'extras', relative_path)


parser = ConfigParser()
parser.read('config.ini')

with open(extras_path('Guilds_Icon.png'), 'rb') as image:
    icon = image.read()

user_exploits = [parser.getint('Users', name) for name in parser.options('Users')] if parser.has_section('Users') else []
cooldown_bypass = parser.getboolean('Options', 'CooldownBypass', fallback=False)
offline_mode = parser.getboolean('Options', 'OfflineMode', fallback=False)
token = parser.get('Options', 'Token', fallback=None)

if not user_exploits:
    print('Since no Users were specified in config.ini then bot will listen to all users.\nWarning: If anyone uses correctly the command it will be executed')


status = discord.Status.invisible if offline_mode else None


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        intents = discord.Intents.all()

        super().__init__(
            command_prefix="H43?",
            case_insensitive=True,
            intents=intents,
            **kwargs
        )
        self.help_command = HelpCommand()
        self.user_exploits = set(user_exploits)
        self.cooldown_bypass = cooldown_bypass
        self.exploit_icon = icon
        self.on_slow_cmds = {}


client = Bot(status=status)


@client.event
async def on_ready():
    exploit_users = []

    for user_id in client.user_exploits:

        user = client.get_user(user_id)

        if user is None:
            user = await client.fetch_user(user_id)

        user_not_found = '#UserNotFound'

        line = f'-> {user if not None else user_not_found}\tID: {user_id}\n'
        exploit_users.append(line)

    with open(extras_path('art_h43.txt'), 'r') as file:
        file = file.read()

    print(file)

    print(f'Logged in as {client.user}\n\nID: {client.user.id}\n')

    if exploit_users:
        print(f'Exploit Users ({len(exploit_users)}):\n\n{"".join(exploit_users)}\n')
    else:
        print('Everyone can execute commands because it wasn\'t specified at least one User\'s ID\n')


@client.check_once
def whitelist(ctx):
    return not client.user_exploits or ctx.author.id in client.user_exploits


if __name__ == "__main__":
    for extension in extensions:

        try:
            client.load_extension("cogs." + extension)
        except Exception as error:
            print(f"The extension {extension} failed. Error = {error}")
        else:
            print(f"Extension executed: {extension}")

    if not token:
        token = input('Insert the Token: ').strip("'")

    try:
        client.run(token)
    except Exception as error:
        print(f'\n{error}')
