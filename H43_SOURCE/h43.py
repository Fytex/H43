import json
import discord
from discord.ext import commands
from extras.help import HelpCommand


extensions = ['exploit', 'admin_ext', 'error_handler']


class FileError(Exception):
    pass


with open('config.json') as file:
    config = json.load(file)

with open(r'extras\Guilds_Icon.png', 'rb') as image:
    icon = image.read()

user_exploits = config.get('exploit_users', None)
cooldown_bypass = config.get('cooldown_bypass', None)
offline_mode = config.get('offline_mode', None)
token = config.get('token', None)

if None in [user_exploits, cooldown_bypass, offline_mode, token]:
    raise FileError('config.json syntax is wrong.')

if not all(isinstance(x, int) for x in user_exploits):
    raise FileError('IDs must be numbers only.')

if not all(isinstance(x, bool) for x in [cooldown_bypass, offline_mode]):
    raise FileError(
        'cooldown_bypass and offline_mode can either be true or false (lower case letters)')

if len(user_exploits) < 1:
    raise FileError(
        'You need to provide one ID at least so bot can be useful.')

status = discord.Status.invisible if offline_mode else None


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix="H43?",
            case_insensitive=True,
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

        line = f'->{user if not None else user_not_found}\tID: {user_id}\n'
        exploit_users.append(line)

    with open(r'extras\art_h43.txt', 'r') as file:
        file = file.read()

    print(file)

    print(
        f"Logged in as {client.user}\n\nID: {client.user.id}\n\nExploit Users ({len(exploit_users)}):\n\n{''.join(exploit_users)}\n")


@client.check_once
def whitelist(ctx):
    return ctx.author.id in client.user_exploits


if __name__ == "__main__":
    for extension in extensions:

        try:
            client.load_extension("cogs." + extension)
        except Exception as error:
            print(f"The extension {extension} failed. Error = {error}")
        else:
            print(f"Extension executed: {extension}")

    if not token:
        token = input('Introduza a Token: ').strip("'")

    try:
        client.run(token)
    except Exception as error:
        print(f'\n{error}')
