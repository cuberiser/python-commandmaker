class CommandError(Exception):
    """
    Our command Invoking error that each error needs to derive from.
    """

    pass


class CommandInvokeError(CommandError):
    """
    An exception raised on errors in invoking of a command.
    """

    pass


class BadArgument(CommandInvokeError):
    """
    An exception raised on a bad provided argument.
    """

    pass


class CommandCreateError(CommandError):
    """
    An exception which is triggered on an error in creation of a command.
    """

    pass
