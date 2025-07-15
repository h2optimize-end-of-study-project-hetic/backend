class CustomError(Exception):
    pass

class NotFoundError(CustomError):
    """
    Exception raised when a requested resource is not found

    Attributes:
        resource (str): The name of the resource (Tag, User, Room)
        identifier (str | int): The ID of the missing resource
    """

    def __init__(self, resource: str, identifier: str | int):
        super().__init__(f"{resource} with ID '{identifier}' not found")
        self.resource = resource
        self.identifier = identifier


class AlreadyExistsError(CustomError):
    """
    Exception raised when trying to create a resource that already exists

    Attributes:
        resource (str): The name of the resource (Tag, User)
        field (str): The unique field that causes the conflict ("source_address")
        value (str): The conflicting value
    """

    def __init__(self, resource: str, field: str, value: str):
        super().__init__(f"{resource} with {field} '{value}' already exists")
        self.resource = resource
        self.field = field
        self.value = value


class CreationFailedError(CustomError):
    """
    Exception raised when a resource creation fails unexpectedly

    Attributes:
        resource (str): The name of the resource
        reason (str): Optional detail about why the creation failed
    """

    def __init__(self, resource: str, reason: str = "Unknown error"):
        super().__init__(f"Failed to create {resource}: {reason}")
        self.resource = resource
        self.reason = reason


class DecodedFailedError(CustomError):
    """
    Exception raised when decoding a resource fails.

    Attributes:
        resource (str): The name of the resource being decoded
        reason (str): Optional detail about why the decoding failed.
    """

    def __init__(self, resource: str, reason: str = "Unknown decoding error"):
        super().__init__(f"Failed to decode {resource}: {reason}")
        self.resource = resource
        self.reason = reason
