import pytest
from rest_framework.test import APIClient
from model_bakery import baker


@pytest.fixture
def api_client():
    """Фикстура для клиента API."""
    return APIClient()


@pytest.fixture
def course_factory():
    """Фабрика для создания курсов."""
    def factory(*args, **kwargs):
        return baker.make('students.Course', *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    """Фабрика для создания студентов."""
    def factory(*args, **kwargs):
        return baker.make('students.Student', *args, **kwargs)
    return factory
