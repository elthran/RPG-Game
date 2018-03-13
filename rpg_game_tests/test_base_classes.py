import pytest
import pdb

from . import GenericTestCase
from base_classes import ObjectV2, attribute_mapped_collection_object_v2


class TestObjectV2:
    def test_set_get_by_attribute_or_dict_key(self):
        obj = ObjectV2('name')
        obj.foo = 5

        assert obj.foo == obj['foo']

        obj['bar'] = 5
        assert obj['bar'] == obj.bar

    def test_key_error_on_missing_attribute(self):
        obj = ObjectV2('name')
        with pytest.raises(KeyError):
            bar = obj.foo

        with pytest.raises(KeyError):
            bar = obj['foo']

    def test__iter__(self):
        obj = ObjectV2('name')
        obj.foo = 5
        obj.bar = 3

        assert [x for x in obj] == sorted([3, 5])

    def test_sorted_items(self):
        obj = ObjectV2('name')
        obj.foo = 5
        obj.bar = 3

        assert [(k, v) for k, v in obj.sorted_items()] == [('bar', 3), ('foo', 5)]


class TestAttributeMappedCollectionObjectV2(GenericTestCase):
    def test_non_overlaping_keyfunc(self):
        ObjectV2Name = attribute_mapped_collection_object_v2('name')
        ObjectV2Type = attribute_mapped_collection_object_v2('type')

        assert ObjectV2Name().keyfunc != ObjectV2Name().keyfunc
