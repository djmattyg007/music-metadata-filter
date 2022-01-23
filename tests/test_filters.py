import json
import sys
from pathlib import Path
from typing import Iterable, TypedDict

import pytest

from music_metadata_filter.filter import MetadataFilter
from music_metadata_filter.filters import (
    make_amazon_filter,
    make_remastered_filter,
    make_spotify_filter,
    make_tidal_filter,
    make_youtube_filter,
)


fixtures_path_base = Path(__file__).parent / "fixtures" / "filters"


class FilterTestCase(TypedDict):
    description: str
    fieldName: str
    fieldValue: str
    expectedValue: str


def load_fixtures(name: str) -> Iterable[FilterTestCase]:
    fixtures_path = fixtures_path_base / f"{name}.json"
    with fixtures_path.open(mode="r") as f:
        return json.load(f)


def run_filter_test(metadata_filter: MetadataFilter, test_case: FilterTestCase):
    result = metadata_filter.filter_field(test_case["fieldName"], test_case["fieldValue"])
    assert result == test_case["expectedValue"]


@pytest.fixture
def spotify_filter() -> MetadataFilter:
    return make_spotify_filter()


@pytest.mark.parametrize(
    "filter_factory",
    (
        make_youtube_filter,
        make_remastered_filter,
        make_spotify_filter,
        make_amazon_filter,
        make_tidal_filter,
    ),
)
def test_creating_predefined_filters(filter_factory):
    assert isinstance(filter_factory(), MetadataFilter)


@pytest.mark.parametrize("test_case", load_fixtures("spotify"))
def test_spotify_filter(spotify_filter: MetadataFilter, test_case: FilterTestCase):
    run_filter_test(spotify_filter, test_case)
