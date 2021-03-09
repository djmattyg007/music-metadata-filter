import pytest
from unittest.mock import Mock

from music_metadata_filter.filter import MetadataFilter


def dummy_fn(x):
    return x


def run_filter(filter: MetadataFilter, *fns: Mock):
    for field in filter.get_fields():
        filtered_text = filter.filter_field(field, "Test")
        assert filtered_text == "Test"

    for fn in fns:
        fn.assert_called()


def test_canfilter():
    filter = MetadataFilter({"foo": dummy_fn})
    assert filter.can_filter_field("foo")
    assert not filter.can_filter_field("bar")


def test_empty_getfields():
    filter = MetadataFilter({})
    assert tuple(sorted(filter.get_fields())) == tuple()


def test_getfields():
    filter = MetadataFilter({"foo": dummy_fn, "bar": dummy_fn})
    assert tuple(sorted(filter.get_fields())) == ("bar", "foo")


def test_append_different_field():
    fn1 = Mock(wraps=dummy_fn)
    fn2 = Mock(wraps=dummy_fn)

    filter = MetadataFilter({"foo": fn1})
    run_filter(filter, fn1)
    assert fn1.call_count == 1

    append_result = filter.append({"bar": fn2})
    assert append_result is filter

    run_filter(filter, fn1, fn2)
    assert fn1.call_count == 2
    assert fn2.call_count == 1


def test_append_same_field():
    fn1 = Mock(wraps=dummy_fn)
    fn2 = Mock(wraps=dummy_fn)

    filter = MetadataFilter({"foo": fn1})
    run_filter(filter, fn1)
    assert fn1.call_count == 1

    append_result = filter.append({"foo": fn2})
    assert append_result is filter

    run_filter(filter, fn1, fn2)
    assert fn1.call_count == 2
    assert fn2.call_count == 1


def test_extend_different_field():
    fn1 = Mock(wraps=dummy_fn)
    fn2 = Mock(wraps=dummy_fn)

    filter1 = MetadataFilter({"foo": fn1})
    run_filter(filter1, fn1)
    assert fn1.call_count == 1

    filter2 = MetadataFilter({"bar": fn2})
    extend_result = filter1.extend(filter2)
    assert extend_result is filter1

    run_filter(filter1, fn1, fn2)
    assert fn1.call_count == 2
    assert fn2.call_count == 1


def test_extend_same_field():
    fn1 = Mock(wraps=dummy_fn)
    fn2 = Mock(wraps=dummy_fn)

    filter1 = MetadataFilter({"foo": fn1})
    run_filter(filter1, fn1)
    assert fn1.call_count == 1

    filter2 = MetadataFilter({"foo": fn2})
    extend_result = filter1.extend(filter2)
    assert extend_result is filter1

    run_filter(filter1, fn1, fn2)
    assert fn1.call_count == 2
    assert fn2.call_count == 1


def test_filtering_strings():
    filter = MetadataFilter(
        {
            "artist": [
                lambda text: f"{text}1",
                lambda text: f"{text}2",
            ],
        }
    )

    assert filter.filter_field("artist", "Text") == "Text12"


@pytest.mark.parametrize(
    "input_str",
    (
        "",
        None,
    ),
)
def test_filtering_empty_strings(input_str):
    should_not_be_called = Mock(side_effect=Exception("This function should not be called."))
    filter = MetadataFilter({"artist": should_not_be_called})
    assert filter.filter_field("artist", input_str) == input_str
