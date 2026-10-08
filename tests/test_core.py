
import pytest

from registrar.engine import RegistrarEngine
from registrar.exceptions import (
    DuplicateStudentError,
    InvalidStudentError,
    PersistenceError,
    StudentNotFoundError,
)
from registrar.models import Person, Student
from registrar.storage import Storage


def make_student(student_id="S001", name="Asha"):
    return Student(
        name=name,
        email="asha@example.com",
        student_id=student_id,
        course="Computer Science",
    )


def test_person_and_student_details():
    person = Person(" Asha ", "asha@example.com")
    student = make_student()

    assert person.get_details()["name"] == "Asha"
    assert student.get_details()["student_id"] == "S001"
    assert student.get_details()["course"] == "Computer Science"


def test_invalid_person_and_student():
    with pytest.raises(InvalidStudentError):
        Person("", "asha@example.com")

    with pytest.raises(InvalidStudentError):
        Person("Asha", "invalid-email")

    with pytest.raises(InvalidStudentError):
        Student("Asha", "asha@example.com", "", "Science")

    with pytest.raises(InvalidStudentError):
        Student("Asha", "asha@example.com", "S002", "")


def test_engine_add_get_remove():
    engine = RegistrarEngine()
    student = make_student()

    engine.add_student(student)

    assert engine.count_students() == 1
    assert engine.get_student("S001") is student
    assert engine.list_students() == [student]
    assert engine.remove_student("S001") is student
    assert engine.count_students() == 0


def test_duplicate_and_missing_students():
    engine = RegistrarEngine()
    engine.add_student(make_student())

    with pytest.raises(DuplicateStudentError):
        engine.add_student(make_student())

    with pytest.raises(StudentNotFoundError):
        engine.get_student("missing")

    with pytest.raises(StudentNotFoundError):
        engine.remove_student("missing")

    with pytest.raises(TypeError):
        engine.add_student("not a student")


def test_json_save_and_load(tmp_path):
    path = tmp_path / "students.json"
    engine = RegistrarEngine()
    engine.add_student(make_student())

    engine.save_json(path)
    records = Storage.load_json(path)

    assert records[0]["student_id"] == "S001"

    loaded = RegistrarEngine()
    loaded.load_records(path, "json")
    assert loaded.get_student("S001").name == "Asha"


def test_csv_save_and_load(tmp_path):
    path = tmp_path / "students.csv"
    engine = RegistrarEngine()
    engine.add_student(make_student())

    engine.save_csv(path)
    records = Storage.load_csv(path)

    assert records[0]["student_id"] == "S001"

    loaded = RegistrarEngine()
    loaded.load_records(path, "csv")
    assert loaded.count_students() == 1


def test_storage_errors(tmp_path):
    with pytest.raises(PersistenceError):
        Storage.load_json(tmp_path / "missing.json")

    with pytest.raises(PersistenceError):
        Storage.load_csv(tmp_path / "missing.csv")

    bad_json = tmp_path / "bad.json"
    bad_json.write_text("{broken", encoding="utf-8")

    with pytest.raises(PersistenceError):
        Storage.load_json(bad_json)

    not_a_list = tmp_path / "object.json"
    not_a_list.write_text('{"student": 1}', encoding="utf-8")

    with pytest.raises(PersistenceError):
        Storage.load_json(not_a_list)

    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("wrong,headers\nx,y\n", encoding="utf-8")

    with pytest.raises(PersistenceError):
        Storage.load_csv(bad_csv)


def test_load_rejects_duplicates_and_bad_format(tmp_path):
    path = tmp_path / "duplicates.json"
    path.write_text(
        '[{"name":"A","email":"a@example.com","student_id":"S1","course":"CS"},'
        '{"name":"B","email":"b@example.com","student_id":"S1","course":"Math"}]',
        encoding="utf-8",
    )

    with pytest.raises(DuplicateStudentError):
        RegistrarEngine().load_records(path, "json")

    with pytest.raises(ValueError):
        RegistrarEngine().load_records(path, "xml")


def test_load_rejects_invalid_student_data(tmp_path):
    path = tmp_path / "invalid.json"
    path.write_text(
        '[{"name":"","email":"a@example.com","student_id":"S1","course":"CS"}]',
        encoding="utf-8",
    )

    with pytest.raises(InvalidStudentError):
        RegistrarEngine().load_records(path, "json")


def test_save_errors(tmp_path):
    engine = RegistrarEngine()
    engine.add_student(make_student())

    # A directory path cannot be opened as a file.
    with pytest.raises(PersistenceError):
        Storage.save_json(engine.list_students(), tmp_path)

    with pytest.raises(PersistenceError):
        Storage.save_csv(engine.list_students(), tmp_path)