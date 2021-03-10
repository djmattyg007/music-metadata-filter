from html import unescape

from .filter import MetadataFilter
from .functions import (
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
    youtube,
)


__all__ = (
    "make_youtube_filter",
    "make_remastered_filter",
    "make_spotify_filter",
    "make_amazon_filter",
    "make_tidal_filter",
)


def make_youtube_filter() -> MetadataFilter:
    """Get a filter with YouTube-related filter functions."""

    return MetadataFilter({"track": youtube})


def make_remastered_filter() -> MetadataFilter:
    """Get a filter that removes "Remastered"-like suffixes."""

    return MetadataFilter(
        {
            "track": remove_remastered,
            "album": remove_remastered,
        }
    )


def make_spotify_filter() -> MetadataFilter:
    """Get a filter with Spotify-related filter functions."""

    return MetadataFilter(
        {
            "track": (remove_remastered, remove_parody, fix_track_suffix, remove_live),
            "album": (
                remove_remastered,
                fix_track_suffix,
                remove_live,
                remove_reissue,
                remove_version,
            ),
        }
    )


def make_amazon_filter() -> MetadataFilter:
    """Get a filter with Amazon-related filter functions."""

    return MetadataFilter(
        {
            "artist": (normalize_feature,),
            "track": (
                remove_clean_explicit,
                remove_feature,
                remove_remastered,
                fix_track_suffix,
                remove_version,
                remove_live,
            ),
            "album": (
                unescape,
                remove_clean_explicit,
                remove_remastered,
                fix_track_suffix,
                remove_version,
                remove_live,
            ),
            "albumArtist": (
                normalize_feature,
                album_artist_from_artist,
            ),
        }
    )


def make_tidal_filter() -> MetadataFilter:
    """Get a filter with Tidal-related filter functions."""

    return MetadataFilter(
        {
            "track": (remove_remastered, fix_track_suffix, remove_version, remove_live),
            "album": (remove_remastered, fix_track_suffix, remove_version, remove_live),
        }
    )
