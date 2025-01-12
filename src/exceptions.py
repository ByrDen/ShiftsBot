class RepositoryError(Exception):
    pass


class ItemNotFound(RepositoryError):
    pass


class UserNotFound(ItemNotFound):
    pass


class ShiftNotFound(ItemNotFound):
    pass


class LimitsNotFound(ItemNotFound):
    pass


class DuplicateEntryError(RepositoryError):
    pass


class Unauthorized(Exception):
    pass


class UnknownError(RepositoryError):
    pass

