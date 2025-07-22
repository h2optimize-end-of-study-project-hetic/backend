from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    STAFF = "staff"
    TECHNICIAN = "technician"
    INTERN = "intern"
    GUEST = "guest"


role: Role
