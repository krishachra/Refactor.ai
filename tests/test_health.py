"""
Smoke tests — stdlib and globally available packages only.
For full integration tests: activate venv, pip install -r backend/requirements.txt
"""
import sys
import os


def test_python_version():
    """Python 3.11+ is required."""
    assert sys.version_info >= (3, 11), f"Python 3.11+ required, got {sys.version}"


def test_core_packages():
    """Verify packages pre-installed in the global environment."""
    import pydantic
    import httpx
    import pytest
    assert True, "Core packages import successfully"


def test_backend_source_exists():
    """Backend source file is present."""
    backend_main = os.path.join(
        os.path.dirname(__file__), '..', 'backend', 'main.py'
    )
    assert os.path.exists(backend_main), "backend/main.py must exist"


def test_env_example_exists():
    """Ensure .env.example is committed (never .env)."""
    project_root = os.path.join(os.path.dirname(__file__), '..')
    assert os.path.exists(os.path.join(project_root, '.env.example')), \
        ".env.example must exist"
    assert not os.path.exists(os.path.join(project_root, '.env')), \
        ".env must NOT be committed — gitignore it"


def test_gitignore_covers_env():
    """Verify .gitignore explicitly excludes .env."""
    gitignore_path = os.path.join(os.path.dirname(__file__), '..', '.gitignore')
    with open(gitignore_path) as f:
        content = f.read()
    assert '.env' in content, ".gitignore must contain .env"
