# Contributing to AI Tech Consultant

Thank you for your interest in contributing to the **AI Tech Consultant** capstone project.

## Architecture Guidelines

1. **Language Discipline:**
   - **Task 1 (Knowledge Brain):** Modern async Python 3.10+ with type hints, FastAPI, and SQLite.
   - **Task 2 (Inbox Agent):** Strict TypeScript, Node.js, and Zod validation.
   - **Task 3 (Meeting to Scope):** Modern Python 3.10+, multi-agent orchestration, and Pydantic schemas.
   - *Never mix languages within a task.*

2. **Cross-Service Consumption:**
   - Tasks 2 and 3 must strictly consume Task 1 through its HTTP REST API (`/query`, `/escalations`).
   - Do not import Task 1 internals directly into Task 2 or Task 3.

3. **Evaluation Standards:**
   - Every feature must maintain or improve the 66-case benchmark suite.
   - Run all evaluation suites before submitting a pull request:
     ```bash
     python -m evaluation.run_evals # in task1
     npm test                       # in task2
     python -m evaluation.run_evals # in task3
     ```
