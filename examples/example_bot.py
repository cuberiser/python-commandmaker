import os
import Commands
from Commands import CommandMaker
from Commands.core import CustomConverter
import json


def get_prefix(_):
    if "prefixes.json" in os.listdir():
        with open("prefixes.json", "r") as f:
            prefix: dict = json.load(f)
        return prefix.get("prefix") or _.default_prefix
    return str(_.default_prefix)


engine = CommandMaker("A bot", get_prefix, case_insensitive=True, default_prefix=".")


class PositiveNumber(CustomConverter, int):    
    def __new__(cls, arg):
        arg = int(arg)
        if arg < 0:
            raise Commands.BadArgument("Argument needs to be an integer")
        return int(arg)


@engine.command(name="factorial", aliases=["fctrl"])
def factorial(num: PositiveNumber = 5):
    one: int = 1
    for i in range(2, num+1):
        one *= i
    print(one)


@engine.command(name="two args")
def two_args(first, second):
    print("first arg was", first, "and second arg was", second)


engine.run()
