from diskord.ext.commands import CommandError

class NotDKC(CommandError):
    """Raised when a command is used that is not available outside DKC server"""
    pass
