---
trigger: always_on
---

# 1. Environment & Tools

## Package Manager
- All operations must strictly use **uv**.

## Installation
- Use: `uv add <package>`

## Command Execution
- Use: `uv run python manage.py <command>`

## Testing
- Use `pytest`.Before executing the test, you must ensure that the relevant dependencies and configuration files are installed.

## API Style
- RESTful

---

# 2. Architectural Standards

## Structure
- Strictly follow the **View / Service / Serializer** three-layer architecture.

## View
- Responsible only for **request parsing** and **response returning**.
- Must inherit from **Django Rest Framework (DRF)** class-based views.

## Service
- Contains the **core business logic**.
- Must be implemented as a **Class**.
- Prefer using `@staticmethod` for **stateless logic**.

## Serializer
- Responsible for **data validation** and **serialization transformation**.

## Design Principle
- Follow **Object-Oriented (OO)** principles.
- When handling complex logic (e.g., multiple decompression algorithms or file classification rules), evaluate and apply appropriate **Design Patterns**.