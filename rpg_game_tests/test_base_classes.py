import pytest

from . import GenericTestCase
from models.base_classes import DictHybrid, attribute_mapped_dict_hybrid


class TestDictHybrid:
    def test_set_get_by_attribute_or_dict_key(self):
        obj = DictHybrid()
        obj.foo = 5

        assert obj.foo == obj['foo']

        obj['bar'] = 5
        assert obj['bar'] == obj.bar

    def test_key_error_on_missing_attribute(self):
        obj = DictHybrid()
        with pytest.raises(KeyError):
            bar = obj.foo

        with pytest.raises(KeyError):
            bar = obj['foo']

    def test__iter__(self):
        obj = DictHybrid()
        obj.foo = 5
        obj.bar = 3

        assert [x for x in obj] == sorted([3, 5])

    def test_sorted_items(self):
        obj = DictHybrid()
        obj.foo = 5
        obj.bar = 3

        assert [(k, v) for k, v in obj.sorted_items()] == [('bar', 3), ('foo', 5)]


class TestAttributeMappedCollectionDictHybrid(GenericTestCase):
    def test_non_overlaping_keyfunc(self):
        DictHybridName = attribute_mapped_dict_hybrid('name')
        DictHybridType = attribute_mapped_dict_hybrid('type')

        assert DictHybridName().keyfunc != DictHybridName().keyfunc
