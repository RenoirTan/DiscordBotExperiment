import logging
import logging.handlers
import os
import typing as t

import discord
from discord.ext import commands

from discordbot.utils import COMMAND_PREFIX, register_commands


__ALL__ = ["MyClient", "COMMAND_LIST", "run_bot", "hello"]


class MyClient(commands.Bot):
    """
    Object oriented programming much wow.
    """
    
    # When the bot has successfully started
    async def on_ready(self):
        print(f"Logged on as {self.user}")
    
    # When the bot sees a message in a server (from whatever channel)
    async def on_message(self, message: discord.Message):
        
        # check if the message was sent by us (the bot)
        # if so, we should quickly return so that we don't end up replying to
        # ourselves
        if message.author == self.user:
            return
        
        # print the message to console for logging purposes of course
        print(f"Message from {message.author}: {message.content}")
        
        # pass the message onto commands.Bot's on_message so that it can
        # redirect it to the correct command
        await super().on_message(message)


@commands.command()
async def hello(ctx: commands.Context):
    """
    When someone sends '=hello' in chat, print '[user] says hello' to console
    """
    print(f"{ctx.author.name} says hello", flush=True) # flush=True to make pylance shut up


COMMAND_LIST: t.List[commands.Command] = [hello]
"""List of commands our bot uses."""


def run_bot(args: t.List[str]):
    """
    One function to get the bot running. Similar to int main(int, char**) in C.
    """
    token: t.Optional[str] = None
    if len(args) < 2:
        token = os.environ["DISCORD_TOKEN"]
    else:
        with open(args[1], "r") as f:
            line = f.readline()
            if not line:
                raise Exception("Token file is empty")
            else:
                token = line.strip()

    # Intents on discord are like permissions on your smartphone
    # Here we want to be able to read what a message says
    # so we set intents.message_content = True
    intents = discord.Intents.default()
    intents.message_content = True

    # Setup for logging
    # Stolen from `https://discordpy.readthedocs.io/en/stable/logging.html`
    # Logs will be dumped to ./discord.log
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

    # Get our bot object
    client = MyClient(command_prefix=COMMAND_PREFIX, intents=intents)
    # Add the commands we have defined previously
    register_commands(client, COMMAND_LIST)
    # Run our bot
    client.run(token, log_handler=None)
