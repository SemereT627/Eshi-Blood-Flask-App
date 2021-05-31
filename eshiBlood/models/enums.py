import enum


class Gender(enum.Enum):
    Male = "Male"
    Female = "Female"


class MartialStatus(enum.Enum):
    Single = "Single"
    Married = "Married"


class Status(enum.Enum):
    Active = "Active"
    Pending = "Pending"
    Closed = "Closed"


class WeekDay(enum.Enum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"

class Role(enum.Enum):
    SuperAdmin = "SuperAdmin"
    Admin = "Admin"
    Donor = "Donor"
    Nurse = "Nurse"
