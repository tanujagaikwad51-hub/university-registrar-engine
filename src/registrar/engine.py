
from .exceptions import DuplicateStudentError, StudentNotFoundError
from .models import Student


class RegistrarEngine:
    """Manage student records safely."""

    def __init__(self):
        self.__students = {}

    def add_student(self, student: Student) -> None:
        if not isinstance(student, Student):
            raise TypeError("Only Student objects can be added.")

        student_id = student.student_id

        if student_id in self.__students:
            raise DuplicateStudentError(
                f"Student ID '{student_id}' already exists."
            )

        self.__students[student_id] = student

    def get_student(self, student_id: str) -> Student:
        student = self.__students.get(student_id)

        if student is None:
            raise StudentNotFoundError(
                f"Student ID '{student_id}' was not found."
            )

        return student

    def remove_student(self, student_id: str) -> Student:
        student = self.get_student(student_id)
        del self.__students[student_id]
        return student

    def list_students(self) -> list[Student]:
        return list(self.__students.values())

    def count_students(self) -> int:
        return len(self.__students)

    def save_json(self, path) -> None:
        from .storage import Storage
        Storage.save_json(self.list_students(), path)

    def save_csv(self, path) -> None:
        from .storage import Storage
        Storage.save_csv(self.list_students(), path)

    def load_records(self, path, file_format: str) -> None:
        from .storage import Storage

        if file_format.lower() == "json":
            records = Storage.load_json(path)
        elif file_format.lower() == "csv":
            records = Storage.load_csv(path)
        else:
            raise ValueError("Format must be 'json' or 'csv'.")

        new_students = {}
        for record in records:
            student = Student(
                name=record["name"],
                email=record["email"],
                student_id=record["student_id"],
                course=record["course"],
            )

            if student.student_id in new_students:
                raise DuplicateStudentError(
                    f"Duplicate student ID '{student.student_id}' in file."
                )

            new_students[student.student_id] = student

        self.__students.update(new_students)