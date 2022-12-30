import logging
import logging.handlers

import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")
    
    async def on_message(self, message):
        if message.author == self.user:
            return
        print(f"Message from {message.author}: {message.content}")


def run_bot(args):
    if len(args) < 2:
        raise Exception("No file path provided for token!")
    
    token = None
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

    client = MyClient(intents=intents)
    client.run(token, log_handler=None)
