# A Python package for creating discord bot like commands

This package aims to create discord bot
like commands for the python console.
This packages syntax for creating commands is very similar to
discord.py. Also inspired by TheGenocide/PyCommands.
You can read the examples to see how to create a bot with it
This package is solely written in python 3.10
and thus requires it.

You can install it by doing `pip install python-commandmaker`
You can submit pull requests to improve any code as the project
is completely open source

**A quick example** - 
```py
import Commands

bot = Commands.CommandMaker("An example bot", ".",
                            case_insensitive=False)


@bot.command()
def some_command(command_args):
    print(command_args)


bot.run()
```
