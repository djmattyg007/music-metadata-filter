import pytest

from music_metadata_filter.filter import MetadataFilter
from music_metadata_filter.filters import make_youtube_filter, make_remastered_filter, make_spotify_filter, make_amazon_filter, make_tidal_filter


@pytest.mark.parametrize("filter_factory", (make_youtube_filter, make_remastered_filter, make_spotify_filter, make_amazon_filter, make_tidal_filter))
def test_creating_predefined_filters(filter_factory):
    assert isinstance(filter_factory(), MetadataFilter)
