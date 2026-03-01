"""Module not found exception."""


class ModuleNotFoundException(Exception):
    """Raised when a course module cannot be found by the given identifier.

    Attributes:
        module_id: The identifier that produced no result.
    """

    def __init__(self, module_id: str) -> None:
        """Initialise the exception with the missing module ID.

        Args:
            module_id: The ULID that was not found.
        """
        self.module_id = module_id
        super().__init__(f"Module '{module_id}' not found.")
