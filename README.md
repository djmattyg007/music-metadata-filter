# music-metadata-filter [![Test][workflowbadge]][workflow] [![PYPI][pypibadge]][PyPI]

A module for cleaning up artist, album and song names.

## Installation

The music-metadata-filter library can be found on [PyPI], and is installable with pip:

```sh
pip install music-metadata-filter
```

## Usage

### Basic example

```python
from music_metadata_filter.functions import remove_remastered

print(remove_remastered("Track Title 1 - Remastered 2015"))
# outputs "Track Title 1 "
print(remove_remastered("Track Title 2 (2011 Remaster)"))
# outputs "Track Title 2 "
```

### Single filter functions

You can call filter functions for basic, one-line filter functionality.
These filter functions are intended to be used on a single field, such as
an artist, album or track.

However, it is possible (not officially supported) to use some of these on
combined fields ("Artist - Song", "Artist - Album"), as in the third example below.

```python
import music_metadata_filter.functions as functions

print(functions.remove_remastered("Jane Doe (Remastered)"))
# outputs "Jane Doe "
print(functions.remove_version("Get Lucky (Album Version)"))
# outputs "Get Lucky "
print(functions.youtube("Car Bomb - Scattered Sprites (Official Music Video)"))
# outputs "Car Bomb - Scattered Sprites"
```

See [functions.py](music_metadata_filter/functions.py) for more details.

### Multiple filters

You can also use multiple filters on a string at once by creating a
`MetadataFilter` object which combines multiple functions from above,
or by using one of the predefined [filter objects](#predefined-filters).

First, create a filter set. This is a set of rules for artists, albums, tracks,
and albumArtists.

```python
import music_metadata_filter.functions as functions
from music_metadata_filter.filter import FilterSet

filter_set: FilterSet = {
    "track": (
        functions.remove_remastered,
        functions.fix_track_suffix,
        functions.remove_live,
        functions.remove_version,
    ),
    "album": (
        functions.remove_remastered,
        functions.fix_track_suffix,
        functions.remove_live,
    ),
}
```

Then, construct a `MetadataFilter` using this filter set.

```python
from music_metadata_filter.filter import MetadataFilter

filter = MetadataFilter(filter_set)
print(filter.filter_field("album", "Nevermind (Remastered)"))
# outputs "Nevermind "
print(filter.filter_field("track", "In Bloom - Nevermind Version"))
# outputs "In Bloom (Nevermind Version)"
print(filter.filter_field("track", "Won't Get Fooled Again - Album Version"))
# outputs "Won't Get Fooled Again "
```

### Predefined filters

There are also predefined filters available for easy access. For example,
the above filter set is actually the predefined Spotify filter:

```python
from music_metadata_filter.filters import make_spotify_filter

filter = make_spotify_filter()
```

See [filters.py](music_metadata_filter/filters.py) for more details.

### Extending filters

Finally, you can take existing `MetadataFilter` objects and extend them with another filter.
This is done by providing the `.extend()` method with another `MetadataFilter` object.

```python
from music_metadata_filter.filters import make_spotify_filter, make_amazon_filter

filter = make_spotify_filter()
filter.extend(make_amazon_filter())

print(filter.filter_field("track", "Seasons in the Abyss (Album Version)"))
# outputs "Seasons in the Abyss "
```

As an alternative, you can use the `.append()` method to apply a filter set to
an existing `MetadataFilter` object.

```python
filter = make_spotify_filter()
filter.append({"album": lambda x: f"{x} Album"})
```

Since these methods return a `MetadataFilter` instance, you can chain method calls.

```python
filter = make_spotify_filter().append({
    "artist": lambda x: f"{x} The Artist",
})
```

## Development

```sh
# Initialise a virtualenv
> python3 -m venv .
> source bin/activate

# Install dev dependencies
> pip install -r requirements-dev.txt

# Run tests
> pytest

# Run black formatter
> black music_metadata_filter tests

# Run flake8 linter
> flake8 music_metadata_filter tests

# Run mypy type checker
> mypy music_metadata_filter tests

# Regenerate regular expressions and test fixtures from upstream
> ./regen.sh
```

## License

Licensed under the [MIT License](LICENSE.md).

## Acknowledgements

This library is a (mostly) direct port of the original JS library
[metadata-filter](https://github.com/web-scrobbler/metadata-filter).
Some of the code in this library, including regular expressions and test fixtures,
are taken directly from the upstream repository.

I can't thank the web-scrobbler team enough for creating such a fantastic
piece of software, and for collaborating with me in the creation of this
port to Python.

<!-- Badges -->

[pypibadge]: https://img.shields.io/pypi/v/music-metadata-filter
[workflowbadge]: https://img.shields.io/github/workflow/status/djmattyg007/music-metadata-filter/Test?label=test

<!-- Related pages -->

[PyPI]: https://pypi.org/project/music-metadata-filter
[workflow]: https://github.com/djmattyg007/music-metadata-filter/actions?query=workflow%3ATest
