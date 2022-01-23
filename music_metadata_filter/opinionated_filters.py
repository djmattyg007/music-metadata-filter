from .filter import MetadataFilter
from .functions import remove_parody, remove_reissue, remove_remastered, remove_version
from .opinionated_functions import fix_track_suffix


def make_spotify_filter() -> MetadataFilter:
    """
    Get a filter with an opinionated list of Spotify-related filter functions.
    Does not match upstream.
    """

    return MetadataFilter(
        {
            "track": (remove_remastered, remove_parody, fix_track_suffix, remove_version),
            "album": (
                remove_remastered,
                fix_track_suffix,
                remove_reissue,
                remove_version,
            ),
        }
    )
