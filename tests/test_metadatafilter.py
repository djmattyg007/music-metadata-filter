from unittest.mock import Mock

import pytest

from music_metadata_filter.filter import MetadataFilter


def dummy_fn(x):
    return x


def run_filter(metadata_filter: MetadataFilter, *fns: Mock):
    for field in metadata_filter.get_fields():
        filtered_text = metadata_filter.filter_field(field, "Test")
        assert filtered_text == "Test"

    for fn in fns:
        fn.assert_called()


def test_canfilter():
    metadata_filter = MetadataFilter({"foo": dummy_fn})
    assert metadata_filter.can_filter_field("foo")
    assert not metadata_filter.can_filter_field("bar")

    metadata_filter.filter_field("bar", "dummy")
    assert not metadata_filter.can_filter_field("bar")


def test_empty_getfields():
    metadata_filter = MetadataFilter({})
    assert tuple(sorted(metadata_filter.get_fields())) == tuple()


def test_getfields():
    metadata_filter = MetadataFilter({"foo": dummy_fn, "bar": dummy_fn})
    assert tuple(sorted(metadata_filter.get_fields())) == ("bar", "foo")


def test_append_different_field():
    fn1 = Mock(wraps=dummy_fn)
    fn2 = Mock(wraps=dummy_fn)

    metadata_filter = MetadataFilter({"foo": fn1})
    run_filter(metadata_filter, fn1)
    assert fn1.call_count == 1

    append_result = metadata_filter.append({"bar": fn2})
    assert append_result is metadata_filter

    run_filter(metadata_filter, fn1, fn2)
    assert fn1.call_count == 2
    assert fn2.call_count == 1


def test_append_same_field():
    fn1 = Mock(wraps=dummy_fn)
    fn2 = Mock(wraps=dummy_fn)

    metadata_filter = MetadataFilter({"foo": fn1})
    run_filter(metadata_filter, fn1)
    assert fn1.call_count == 1

    append_result = metadata_filter.append({"foo": fn2})
    assert append_result is metadata_filter

    run_filter(metadata_filter, fn1, fn2)
    assert fn1.call_count == 2
    assert fn2.call_count == 1


def test_extend_different_field():
    fn1 = Mock(wraps=dummy_fn)
    fn2 = Mock(wraps=dummy_fn)

    metadata_filter1 = MetadataFilter({"foo": fn1})
    run_filter(metadata_filter1, fn1)
    assert fn1.call_count == 1

    metadata_filter2 = MetadataFilter({"bar": fn2})
    extend_result = metadata_filter1.extend(metadata_filter2)
    assert extend_result is metadata_filter1

    run_filter(metadata_filter1, fn1, fn2)
    assert fn1.call_count == 2
    assert fn2.call_count == 1


def test_extend_same_field():
    fn1 = Mock(wraps=dummy_fn)
    fn2 = Mock(wraps=dummy_fn)

    metadata_filter1 = MetadataFilter({"foo": fn1})
    run_filter(metadata_filter1, fn1)
    assert fn1.call_count == 1

    metadata_filter2 = MetadataFilter({"foo": fn2})
    extend_result = metadata_filter1.extend(metadata_filter2)
    assert extend_result is metadata_filter1

    run_filter(metadata_filter1, fn1, fn2)
    assert fn1.call_count == 2
    assert fn2.call_count == 1


def test_filtering_strings():
    metadata_filter = MetadataFilter(
        {
            "artist": [
                lambda text: f"{text}1",
                lambda text: f"{text}2",
            ],
        }
    )

    assert metadata_filter.filter_field("artist", "Text") == "Text12"


@pytest.mark.parametrize(
    "input_str",
    (
        "",
        None,
    ),
)
def test_filtering_empty_strings(input_str):
    should_not_be_called = Mock(side_effect=Exception("This function should not be called."))
    metadata_filter = MetadataFilter({"artist": should_not_be_called})
    assert metadata_filter.filter_field("artist", input_str) == input_str


def test_invalid_filter_function():
    with pytest.raises(TypeError, match="Invalid filter function: expected callable, got 'str'"):
        MetadataFilter({"track": "not_callable"})
