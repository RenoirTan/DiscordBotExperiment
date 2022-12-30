import logging
import logging.handlers
import os

import discord
from discord.ext import commands

from discordbot.utils import COMMAND_PREFIX, register_commands

class MyClient(commands.Bot):
    async def on_ready(self):
        print(f"Logged on as {self.user}")
    
    async def on_message(self, message):
        await super().on_message(message) # pass it onto commands.Bot command redirection thing
        if message.author == self.user:
            return
        print(f"Message from {message.author}: {message.content}")


@commands.command()
async def hello(ctx: commands.Context):
    print(f"{ctx.author.name} says hello", flush=True) # flush=True to make pylance shut up


COMMAND_LIST = [hello]
"""List of commands our bot uses."""


def run_bot(args):
    token = None
    if len(args) < 2:
        token = os.environ["DISCORD_TOKEN"]
    else:
        with open(args[1], "r") as f:
            line = f.readline()
            if not line:
                raise Exception("Token file is empty")
            else:
                token = line.strip()

    intents = discord.Intents.default()
    intents.message_content = True

    logger = logging.getLogger("discord")
    logger.setLevel(logging.DEBUG)
    logging.getLogger("discord.http").setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=32 << 20, # 32 MiB
        backupCount=5
    )
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}",
        "%Y-%m-%d %H:%M:%S",
        style="{"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    client = MyClient(command_prefix=COMMAND_PREFIX, intents=intents)
    register_commands(client, COMMAND_LIST)
    client.run(token, log_handler=None)
