# Dependency Rationale

The runtime depends only on the Python standard library. This keeps the project free to run locally, easy to audit, and independent from external package services once Python is available.

The local API uses `http.server`, persistence uses JSON files, configuration uses a small YAML-compatible parser for the included examples, and tests use the standard library test runner.

Development can still use optional tools if a contributor chooses, but the repository does not require them.
