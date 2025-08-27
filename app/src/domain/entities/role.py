from enum import Enum

class Role(str, Enum):
    admin = "admin"
    staff = "staff"
    technician = "technician"
    intern = "intern"
    guest = "guest"