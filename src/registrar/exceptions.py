
class RegistrarError(Exception):
    """Base exception for registrar errors."""


class InvalidStudentError(RegistrarError):
    """Raised when student data is invalid."""


class StudentNotFoundError(RegistrarError):
    """Raised when a student does not exist."""


class DuplicateStudentError(RegistrarError):
    """Raised when a student ID already exists."""


class PersistenceError(RegistrarError):
    """Raised when saving or loading data fails."""