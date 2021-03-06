"""
Check https://pypi.org/project/python-commandmaker, https://github.com/cuberiser/python-commandmaker for more info
"""
from typing import Callable, Sequence
from .errors import *
from .core import Command
import sys


__version__ = "0.0.5"
__author__ = "Cube Riser"


class CommandMaker:
    """
    This is our base command maker class from which we make commands.
    You can either inherit from this or make an instance to create commands.
    """

    def __init__(
        self, name: str, prefix: str | Callable, *, case_insensitive: bool, **kwargs
    ):
        self._cs = case_insensitive
        self._prefix = prefix
        self.__name__ = name
        self._commands: dict[str, Command] = {}
        self._aliases: dict[str, Command] = {}
        for kwarg in kwargs:
            self.__setattr__(kwarg, kwargs[kwarg])

    def command(
        self,
        *,
        name: str = "",
        aliases: Sequence[str] = [],
        description: str = "",
        override=False,
    ):
        if not override:
            if self.get_command(name):
                raise CommandCreateError(f"Already an existing command or alias {name}")
            for alias in aliases:
                if self.get_command(alias):
                    raise CommandCreateError(
                        f"Already an existing command or alias {alias}"
                    )

        def _wrapper(func: Callable):
            cmd = Command(
                name,
                aliases,
                func,
                description=description or func.__doc__ or "No description",
            )
            self._commands[name or func.__name__] = cmd
            for a in aliases:
                self._aliases[str(a)] = cmd
            if override:
                print(
                    f"WARNING: Overriding a command might have unintentional effects in some commands\ncommand:{name or func.__name__}",
                    file=sys.stderr,
                )
            if description:
                print(
                    f"WARNING: Description kwarg is deprecated, use docstrings instead\ncommand: {name or func.__name__}",
                    file=sys.stderr,
                )

        return _wrapper

    def get_command(self, command_name: str):
        return self._commands.get(command_name) or self._aliases.get(command_name)

    @property
    def prefix(self) -> str:
        if callable(self._prefix):
            return self._prefix(self)
        return str(self._prefix)

    @property
    def commands(self):
        for command in self._commands.values():
            yield command

    def run(self):
        print(
            f"Welcome to {self.__name__}'s commands, my prefix right now is {self.prefix}"
        )
        while True:
            command = input(">>> ") if not self._cs else input(">>> ").lower()
            if command.startswith(self.prefix):
                command = command[len(self.prefix) :]
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
            elif command == "prefix":
                print("My current prefix is", self.prefix)
