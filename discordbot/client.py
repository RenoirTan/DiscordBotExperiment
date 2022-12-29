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
    
    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    token = None
    with open(args[1], "r") as f:
        line = f.readline()
        if not line:
            raise Exception("Token file is empty")
        else:
            token = line.strip()
    client.run(token)
