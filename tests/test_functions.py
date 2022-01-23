import json
from pathlib import Path
from typing import Iterable, TypedDict

import pytest

from music_metadata_filter.functions import (
    FilterFunction,
    album_artist_from_artist,
    fix_track_suffix,
    normalize_feature,
    remove_clean_explicit,
    remove_feature,
    remove_live,
    remove_parody,
    remove_reissue,
    remove_remastered,
    remove_version,
    remove_zero_width,
    replace_nbsp,
    youtube,
)


fixtures_path_base = Path(__file__).parent / "fixtures" / "functions"


# https://github.com/PyCQA/pep8-naming/pull/189
class FunctionTestCase(TypedDict):
    description: str
    funcParameter: str  # noqa: N815
    expectedValue: str  # noqa: N815


def load_fixtures(name: str) -> Iterable[FunctionTestCase]:
    fixtures_path = fixtures_path_base / f"{name}.json"
    with fixtures_path.open(mode="r") as f:
        return json.load(f)


def run_function_test(filter_func: FilterFunction, test_case: FunctionTestCase):
    result = filter_func(test_case["funcParameter"])
    assert result == test_case["expectedValue"]


@pytest.mark.parametrize("test_case", load_fixtures("album-artist-from-artist"))
def test_album_artist_from_artist(test_case: FunctionTestCase):
    run_function_test(album_artist_from_artist, test_case)


@pytest.mark.parametrize("test_case", load_fixtures("fix-track-suffix"))
def test_fix_track_suffix(test_case: FunctionTestCase):
    run_function_test(fix_track_suffix, test_case)


@pytest.mark.parametrize("test_case", load_fixtures("normalize-feature"))
def test_normalize_feature(test_case: FunctionTestCase):
    run_function_test(normalize_feature, test_case)


@pytest.mark.parametrize("test_case", load_fixtures("remove-clean-explicit"))
def test_remove_clean_explicit(test_case: FunctionTestCase):
    run_function_test(remove_clean_explicit, test_case)


@pytest.mark.parametrize("test_case", load_fixtures("remove-feature"))
def test_remove_feature(test_case: FunctionTestCase):
    run_function_test(remove_feature, test_case)


@pytest.mark.parametrize("test_case", load_fixtures("remove-live"))
def test_remove_live(test_case: FunctionTestCase):
    run_function_test(remove_live, test_case)


@pytest.mark.parametrize("test_case", load_fixtures("remove-parody"))
def test_remove_parody(test_case: FunctionTestCase):
    run_function_test(remove_parody, test_case)


@pytest.mark.parametrize("test_case", load_fixtures("remove-reissue"))
def test_remove_reissue(test_case: FunctionTestCase):
    run_function_test(remove_reissue, test_case)


@pytest.mark.parametrize("test_case", load_fixtures("remove-remastered"))
def test_remove_remastered(test_case: FunctionTestCase):
    run_function_test(remove_remastered, test_case)


@pytest.mark.parametrize("test_case", load_fixtures("remove-version"))
def test_remove_version(test_case: FunctionTestCase):
    run_function_test(remove_version, test_case)


@pytest.mark.parametrize("test_case", load_fixtures("remove-zero-width"))
def test_remove_zero_width(test_case: FunctionTestCase):
    run_function_test(remove_zero_width, test_case)


@pytest.mark.parametrize("test_case", load_fixtures("replace-nbsp"))
def test_replace_nbsp(test_case: FunctionTestCase):
    run_function_test(replace_nbsp, test_case)


@pytest.mark.parametrize("test_case", load_fixtures("youtube"))
def test_youtube(test_case: FunctionTestCase):
    run_function_test(youtube, test_case)
