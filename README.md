

\# University Registrar Engine



An object-oriented Python application for managing university student records.



\## Features



\- Object-oriented design using inheritance and polymorphism

\- Encapsulated student record management

\- Custom exceptions for invalid and duplicate records

\- Add, find, list, and remove students

\- JSON and CSV data persistence

\- Automated unit tests using pytest

\- 100% test coverage in the current test suite



\## Project Structure



```text

university-registrar-engine/

├── src/

│   └── registrar/

│       ├── \_\_init\_\_.py

│       ├── engine.py

│       ├── exceptions.py

│       ├── models.py

│       └── storage.py

├── tests/

│   └── test\_core.py

└── pyproject.toml

```



\## Setup



```bash

python -m venv .venv

```



Windows:



```cmd

.venv\\Scripts\\activate

```



Install the project and testing tools:



```bash

python -m pip install -e .

python -m pip install pytest pytest-cov

```



\## Run Tests



```bash

pytest

```



\## Check Test Coverage



```bash

pytest --cov=registrar --cov-report=term-missing

```



\## Concepts Demonstrated



\- Inheritance: `Student` inherits from `Person`.

\- Polymorphism: `get\_details()` provides class-specific details.

\- Encapsulation: `RegistrarEngine` keeps its student dictionary private.

\- Custom exceptions: invalid input, missing students, duplicate IDs, and persistence errors.

\- File handling: JSON and CSV save/load operations.

