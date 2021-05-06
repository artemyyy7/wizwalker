class WizWalkerError(Exception):
    """
    Base wizwalker exception, all exceptions raised should inherit from this
    """


class ClientClosedError(WizWalkerError):
    """
    Raised when trying to do an action that requires a running client
    """

    def __init__(self):
        super().__init__("Client must be running to preform this action.")


class HookNotActive(WizWalkerError):
    """
    Raised when doing something that requires a hook to be active
    but it is not

    Attributes:
        hook_name: Name of the hook that is not active
    """

    def __init__(self, hook_name: str):
        super().__init__(f"{hook_name} is not active.")
        self.hook_name = hook_name


class HookAlreadyActivated(WizWalkerError):
    """
    Raised when trying to activate an active hook

    Attributes:
        hook_name: Name of the hook that is already active
    """

    def __init__(self, hook_name: str):
        super().__init__(f"{hook_name} was already activated.")
        self.hook_name = hook_name


class WizWalkerMemoryError(WizWalkerError):
    """
    Raised to error with reading/writing memory
    """


class PatternMultipleResults(WizWalkerMemoryError):
    """
    Raised when a pattern has more than one result
    """


class PatternFailed(WizWalkerMemoryError):
    """
    Raised when the pattern scan fails
    """

    def __init__(self, pattern):
        super().__init__(
            f"Pattern {pattern} failed. You most likely need to restart the client."
        )


class MemoryReadError(WizWalkerMemoryError):
    """
    Raised when we couldn't read some memory
    """

    def __init__(self, address: int):
        super().__init__(f"Unable to read memory at address {address}.")


class MemoryWriteError(WizWalkerMemoryError):
    """
    Raised when we couldn't write to some memory
    """

    def __init__(self, address: int):
        super().__init__(f"Unable to write memory at address {address}.")


class ReadingEnumFailed(WizWalkerMemoryError):
    """
    Raised when the value passed to an enum is not valid
    """

    def __init__(self, enum, value):
        super().__init__(f"Error reading enum: {value} is not a vaid {enum}.")


class HookNotReady(WizWalkerMemoryError):
    """
    Raised when trying to use a value from a hook before hook has run

    Attributes:
        hook_name: Name of the hook that is not ready
    """

    def __init__(self, hook_name: str):
        super().__init__(f"{hook_name} has not run yet and is not ready.")


class WizWalkerCombatError(WizWalkerError):
    """
    Raised for errors relating to combat
    """


class NotInCombat(WizWalkerCombatError):
    """
    Raised when trying to do an action that requires the client
    to be in combat
    """


class NotEnoughPips(WizWalkerCombatError):
    """
    Raised when trying to use a card that costs more pips then
    are available

    Attributes:
        missing: The amount of missing pips
    """

    def __init__(self, missing: int):
        super().__init__(f"Missing {missing} pips needed.")
        self.missing = missing


class NotEnoughMana(WizWalkerCombatError):
    """
    Raised when trying to use a card that cost more mana than
    is available

    Attributes:
        missing: The amount of missing mana
    """

    def __init__(self, missing: int):
        super().__init__(f"Missing {missing} mana needed.")
        self.missing = missing


class CardAlreadyEnchanted(WizWalkerError):
    """
    Raised when trying to enchant an already enchanted card
    """

    def __init__(self):
        super().__init__("That card is already enchanted.")


class HotkeyAlreadyRegistered(WizWalkerError):
    def __init__(self, key: str):
        super().__init__(f"{key} already registered")