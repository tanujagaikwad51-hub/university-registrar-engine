
from dataclasses import dataclass

from .exceptions import InvalidStudentError


@dataclass
class Person:
    name: str
    email: str

    def __post_init__(self):
        self.name = self.name.strip()
        self.email = self.email.strip()

        if not self.name:
            raise InvalidStudentError("Name cannot be empty.")

        if "@" not in self.email or "." not in self.email:
            raise InvalidStudentError("A valid email address is required.")

    def get_details(self) -> dict:
        return {
            "name": self.name,
            "email": self.email,
        }


@dataclass
class Student(Person):
    student_id: str
    course: str

    def __post_init__(self):
        super().__post_init__()
        self.student_id = self.student_id.strip()
        self.course = self.course.strip()

        if not self.student_id:
            raise InvalidStudentError("Student ID cannot be empty.")

        if not self.course:
            raise InvalidStudentError("Course cannot be empty.")

    def get_details(self) -> dict:
        details = super().get_details()
        details.update({
            "student_id": self.student_id,
            "course": self.course,
        })
        return details