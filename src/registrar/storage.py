
import csv
import json
from pathlib import Path

from .exceptions import PersistenceError


class Storage:
    """Save and load student records using JSON or CSV."""

    FIELDS = ["name", "email", "student_id", "course"]

    @staticmethod
    def save_json(students, path):
        try:
            file_path = Path(path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            data = [student.get_details() for student in students]

            with file_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

        except (OSError, TypeError, ValueError) as exc:
            raise PersistenceError(f"Could not save JSON: {exc}") from exc

    @staticmethod
    def load_json(path):
        try:
            with Path(path).open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise PersistenceError("JSON must contain a list of students.")

            return data

        except PersistenceError:
            raise
        except (OSError, json.JSONDecodeError) as exc:
            raise PersistenceError(f"Could not load JSON: {exc}") from exc

    @staticmethod
    def save_csv(students, path):
        try:
            file_path = Path(path)
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with file_path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=Storage.FIELDS)
                writer.writeheader()

                for student in students:
                    writer.writerow(student.get_details())

        except (OSError, TypeError, ValueError) as exc:
            raise PersistenceError(f"Could not save CSV: {exc}") from exc

    @staticmethod
    def load_csv(path):
        try:
            with Path(path).open("r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                if reader.fieldnames != Storage.FIELDS:
                    raise PersistenceError("CSV headers do not match expected fields.")

                return list(reader)

        except PersistenceError:
            raise
        except OSError as exc:
            raise PersistenceError(f"Could not load CSV: {exc}") from exc