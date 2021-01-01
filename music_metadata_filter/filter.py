from collections import defaultdict
from collections.abc import Iterable
from functools import reduce
from typing import List, Mapping, MutableMapping, Union
from typing import Iterable as IterableType

from .functions import FilterFunction


__all__ = (
    "FilterFunction",
    "FilterFunctions",
    "FilterSet",
    "MetadataFilter",
)


FilterFunctions = IterableType[FilterFunction]
FilterSet = Mapping[str, Union[FilterFunction, FilterFunctions]]


def make_iterable(obj) -> Iterable:
    if isinstance(obj, Iterable):
        return obj
    return (obj,)


class MetadataFilter(object):
    def __init__(self, filter_set: FilterSet):
        self._merged_filter_set: MutableMapping[str, List[FilterFunction]] = defaultdict(lambda: [])
        self._append_filters(filter_set)

    def append(self, filter_set: FilterSet) -> "MetadataFilter":
        self._append_filters(filter_set)
        return self

    def extend(self, filter: "MetadataFilter") -> "MetadataFilter":
        self._append_filters(filter._merged_filter_set)
        return self

    def can_filter_field(self, field: str) -> bool:
        return field in self._merged_filter_set

    def get_fields(self) -> IterableType[str]:
        return self._merged_filter_set.keys()

    def filter_field(self, field: str, field_value: str) -> str:
        return self._filter_text(field_value, self._merged_filter_set[field])

    def _filter_text(self, text: str, filters: FilterFunctions) -> str:
        if not text:
            return text

        return reduce(lambda text, filter: filter(text), filters, text)

    def _append_filters(self, filter_set: FilterSet):
        for field, filters in filter_set.items():
            iterable_filters: FilterFunctions = make_iterable(filters)

            for filter in iterable_filters:
                if not callable(filter):
                    raise TypeError(
                        f"Invalid filter function: expected callable, got '{type(filter).__name__}'"
                    )
            self._merged_filter_set[field].extend(iterable_filters)
