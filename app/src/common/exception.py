class CustomError(Exception):
    pass


class NotFoundError(CustomError):
    """
    Exception raised when a requested resource is not found

    Attributes:
        resource (str): The name of the resource (Tag, User, Room)
        value (str | int): The value of the missing resource
        key (str): The name of the key to compare ("source_address")
    """

    def __init__(self, resource: str, value: str | int, key: str | int = "ID"):
        super().__init__(f"{resource} with {key} '{value}' not found")
        self.resource = resource
        self.key = key
        self.value = value


class VerifyUserError(CustomError):
    """
    Exception raised when a requested resource is not found

    Attributes:
        message (msg): détail
    """

    def __init__(self, msg : str):
        super().__init__(f"{msg}")
        self.msg = msg
  


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
        super().__init__(f"Failed to create {resource}")
        self.resource = resource
        self.reason = reason


class UpdateFailedError(CustomError):
    """
    Exception raised when a resource update fails unexpectedly.

    Attributes:
        resource (str): The name of the resource
        reason (str): Optional detail about why the update failed
    """

    def __init__(self, resource: str, reason: str = "Unknown error"):
        super().__init__(f"Failed to update {resource}")
        self.resource = resource
        self.reason = reason


class DeletionFailedError(CustomError):
    """
    Exception raised when a resource deletion fails unexpectedly.

    Attributes:
        resource (str): The name of the resource
        reason (str): Optional detail about why the deletion failed
    """

    def __init__(self, resource: str, reason: str = "Unknown error"):
        super().__init__(f"Failed to delete {resource}")
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
        super().__init__(f"Failed to decode {resource}")
        self.resource = resource
        self.reason = reason


class ForeignKeyConstraintError(CustomError):
    """
    Exception raised when trying to violates foreign key constraint
    """

    def __init__(self, resource: str, constraint_name: str | None = None, table_name: str | None = None):
        msg = f"Failed to execute request on {resource}"
        if constraint_name:
            msg += f", foreign key constraint violated : {constraint_name} from table {table_name}"
        super().__init__(msg)
        self.resource = resource
        self.constraint_name = constraint_name


class CheckConstraintError(CustomError):
    """
    Exception raised when trying to violates defined constraint
    """

    def __init__(self, resource: str, constraint_name: str | None = None, table_name: str | None = None):
        msg = f"Failed to execute request on {resource}"
        if constraint_name:
            msg += f", Violates check constraint : {constraint_name} from table {table_name}"
        super().__init__(msg)
        self.resource = resource
        self.constraint_name = constraint_name
