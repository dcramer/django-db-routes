import pytest

from django.test import TestCase
from tests.models import DummyModel


class SimpleTest(TestCase):
    def test_creation(self):
        with pytest.raises(ValueError):
            instance = DummyModel.objects.create()

        instance = DummyModel.objects.create(group_id=1)
        assert instance.id
