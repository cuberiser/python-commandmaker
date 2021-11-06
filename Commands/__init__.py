from typing import Callable, Sequence
from .errors import *
from .core import Command


__version__ = "0.0.3"
__author__ = "Cube Riser"


class CommandMaker:
    """
    This is our base command maker class from which we make commands.
    You can either inherit from this or make an instance to create commands.
    """

    def __init__(self, name: str, prefix: str | Callable, *, case_insensitive: bool, **kwargs):
        self._cs = case_insensitive
        self.prefix = prefix
        self.__name__ = name
        self._commands: dict[str, Command] = {}
        self._aliases: dict[str, Command] = {}
        for kwarg in kwargs:
            self.__setattr__(kwarg, kwargs[kwarg])

    def command(self, *, name: str = None, aliases: Sequence[str] = [], description: str="No description"):
        if self.get_command(name):
            raise CommandCreateError(
                "Already an existing command or alias {cmd}".format(cmd=name)
            )
        for alias in aliases:
            if self.get_command(alias):
                raise CommandCreateError(
                    "Already an existing command or alias {cmd}".format(cmd=alias)
                )

        def _wrapper(func: Callable):
            cmd = Command(name, aliases, func, description=description)
            self._commands[name or func.__name__] = cmd
            for a in aliases:
                self._aliases[str(a)] = cmd

        return _wrapper

    def get_command(self, command_name: str):
        return self._commands.get(command_name) or self._aliases.get(command_name)

    def _get_prefix(self) -> str:
        if callable(self.prefix):
            return self.prefix(self)
        return str(self.prefix)

    @property
    def commands(self):
        for command in self._commands.values():
            yield command

    def run(self):
        print(
            f"Welcome to {self.__name__}'s commands, my prefix right now is {self._get_prefix()}"
        )
        while True:
            command = input(">>> ") if not self._cs else input(">>> ").lower()
            if command.startswith(self._get_prefix()):
                command = command[len(self._get_prefix()):]
                cmd = self.get_command(command.split(" ")[0])
                if cmd:
                    try:
                        cmd.invoke(" ".join(command.split(" ")[1:]))
                    except ValueError as e:
                        print("A value error occured", e)
                    except BadArgument as ba:
                        print("Bad argument:", ba)
                    except TypeError as te:
                        print("A type error occured:", te)
                else:
                    print("command not found")
            elif command == "help":
                for command in self._commands.values():
                    print(command.name, command.signature, "\n", command.description)
            elif command == "exit":
                break
            elif command == 'prefix':
                print("My current prefix is", self._get_prefix())
