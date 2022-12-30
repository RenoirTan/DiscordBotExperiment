import typing as t

from discord.ext  import commands


__ALL__ = ["COMMAND_PREFIX", "register_commands"]


COMMAND_PREFIX: str = "="
"""Default command prefix."""


def register_commands(bot: commands.Bot, commands: t.Iterable[commands.Command]) -> commands.Bot:
    for command in commands:
        bot.add_command(command)
    return bot
