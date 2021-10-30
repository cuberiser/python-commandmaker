from .errors import *
from typing import Callable, Sequence
from inspect import signature
import asyncio


class CustomConverter:
    """
    Our custom converter class which others need to inherit from.
    ```
    MAKE SURE TO DEFINE __new__ IN THIS!
    ```
    """

    def __init__(self, arg: str):
        self.arg = arg

    def __new__(cls, arg: str): # Make sure to define this in your own converter
        raise NotImplementedError(
            "The subclasses for converters need to define __new__ and return the values"
        )


class Command:
    """
    Our base command class from which commands are formed.
    """

    def __init__(
            self, name: str, aliases: Sequence[str], func: Callable, *, usage: str = None, description: str
    ):
        self.args: list[str] = [
            i.strip() for i in str(signature(func))[1:-1].split(", ")
        ]
        self.func = func
        self.name = name or self.func.__name__
        self.aliases = aliases
        self.signature = "[" + "] [".join(self.args) + "]"
        self.usage = usage or self.signature
        self.description = description
        for idx, arg in enumerate(self.args):
            if ":" in arg:
                self.args[idx] = (arg.split)(":")[0].strip()
            elif "=" in arg:
                self.args[idx] = arg.split("=")[0].strip()

        for idx, arg in enumerate(self.args):
            pass

    def invoke(self, command_str: str):
        command_li: list[str] = command_str.split(" ")
        for idx, arg in enumerate(command_li):
            if not arg:
                continue

            if any("*" in arg for arg in self.args):
                _type = str
            else:
                _type = self.func.__annotations__.get(self.args[idx]) or str
            try:
                command_li[idx] = _type(arg)
            except ValueError as ba:
                raise BadArgument(*ba.args)
            if "" in command_li:
                command_li.remove("")
        while "" in command_li:
            command_li.remove("")
        if asyncio.iscoroutinefunction(self.func):
            asyncio.run(self.func(*command_li))
        else:
            self.func(*command_li)
