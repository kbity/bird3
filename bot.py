import os, sys, discord, random, datetime, traceback, mcv, asyncio
from discord import app_commands

version = "3.0.0.0a (b2fl v2.1.0)"

say_whitelist = [422195092225261568]

with open("config.mcv") as conf:
    cfg = mcv.load(conf.read())

with open("emojis.mcv") as conf:
    emoj = mcv.load(conf.read())

intents = discord.Intents.default()
intents.message_content = True

class birdbot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = birdbot()

directory = os.fsencode("cmds/") # load scripts
for fil in os.listdir(directory):
    filename = os.fsdecode(fil)
    exec(open("cmds/"+filename).read())

evalfunc = None # this is important  i think
async def command_ev(message):
    to_execute = message.content.splitlines()[1:] # discard first line
    to_exec = []
    for h in to_execute:
        if h.startswith("`"):
            continue
        else:
            to_exec.append(f"    {h}\n")

    toexec = "global evalfunc\nasync def evalfunc(message):\n"+"".join(to_exec)
    print(toexec)
    exec(toexec)
    try:
        await evalfunc(message)
    except Exception as e:
        fuck = ''.join(traceback.format_exception(None, e, e.__traceback__))
        await message.reply(f"```\n{fuck[:1980]}\n```")

@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user} ({bot.user.id})")
    status = f"In {str(len(bot.guilds))} servers | bird {version}"
    await bot.change_presence(activity=discord.CustomActivity(name=status))

@bot.event
async def on_message(message: discord.Message):
    if str(message.author.id) == cfg["BotDev"]: # Developer commands
        if message.content.startswith("bird!eval"):
            await command_ev(message)
        if message.content == ("bird!restart"):
            await message.reply("restarting bot...")
            os.execv(sys.executable, ['python'] + sys.argv)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
    print(f"Unhandled app command error in {interaction.command}: {error!r}")
    try:
        await interaction.response.send_message("Something went wrong.", ephemeral=True)
    except Exception as e:
        h = await interaction.channel.send(f"Something went wrong.\n{e}")
        await asyncio.sleep(5)
        await h.delete()

def leftpad(inpt: str, size: int, char: str = " "):
    while len(inpt) < size:
        inpt = char+inpt
    return inpt

if __name__ == "__main__":
    bot.run(cfg["LoginToken"])

# credit to https://codezup.com/python-discord-bot-tutorial/ for the basis for the bot