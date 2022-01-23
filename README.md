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
# outputs "Track Title 1"
print(remove_remastered("Track Title 2 (2011 Remaster)"))
# outputs "Track Title 2"
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
# outputs "Jane Doe"
print(functions.remove_version("Get Lucky (Album Version)"))
# outputs "Get Lucky"
print(functions.youtube("Car Bomb - Scattered Sprites (Official Music Video)"))
# outputs "Car Bomb - Scattered Sprites"
```

See [functions.py](music_metadata_filter/functions.py) for more details.

### Combine filter functions

You can also use multiple filter functions on a string at once by creating a
`MetadataFilter` object which combines multiple functions from above,
or by using one of the predefined [filter objects](#predefined-filters).

First, create a filter set. This is a set of filter functions for different
fields.

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

metadata_filter = MetadataFilter(filter_set)

print(metadata_filter.filter_field("album", "Nevermind (Remastered)"))
# outputs "Nevermind"
print(metadata_filter.filter_field("track", "In Bloom - Nevermind Version"))
# outputs "In Bloom (Nevermind Version)"
print(metadata_filter.filter_field("track", "Won't Get Fooled Again - Album Version"))
# outputs "Won't Get Fooled Again"
```

### Predefined filters

There are also predefined filters available for easy access. For example,
the above filter set is actually the predefined Spotify filter:

```python
from music_metadata_filter.filters import make_spotify_filter

metadata_filter = make_spotify_filter()
```

See [filters.py](music_metadata_filter/filters.py) for more details.

### Extending filters

Finally, you can take existing `MetadataFilter` objects and extend them with another filter.
This is done by providing the `.extend()` method with another `MetadataFilter` object.

```python
from music_metadata_filter.filters import make_spotify_filter, make_amazon_filter

metadata_filter = make_spotify_filter()
metadata_filter.extend(make_amazon_filter())

print(metadata_filter.filter_field("track", "Seasons in the Abyss (Album Version)"))
# outputs "Seasons in the Abyss"
```

As an alternative, you can use the `.append()` method to apply a filter set to
an existing `MetadataFilter` object.

```python
metadata_filter = make_spotify_filter()
metadata_filter.append({"album": lambda x: f"{x} Album"})
```

Since these methods return a `MetadataFilter` instance, you can chain method calls.

```python
metadata_filter = make_spotify_filter().append({
    "artist": lambda x: f"{x} The Artist",
})
```

### Opinionated filters

As discussed below, this library aims to be a direct port from another language. However, as is to
be expected, I don't agree 100% with every choice made by the upstream maintainers. In order to
make updates easier and ensure compatibility with upstream, my opinions are therefore separated out
into a dedicated set of modules labelled with "opinionated".

Right now, there isn't much that differs. The primary differences are that "Live" should not be
stripped from Spotify metadata, and that "Live" suffixes should be normalised by the "fix suffix"
ruleset (like "Instrumental" and "Remix").

```python
from music_metadata_filter.opinionated_filters import make_spotify_filter

metadata_filter = make_spotify_filter()

print(metadata_filter.filter_field("track", "Track Title - Live / Remastered"))
# outputs "Track Title (Live)"
```

## Development

This project uses [invoke] as a task runner.

```sh
# Initialise a virtualenv
> python3 -m venv venv --prompt music-metadata-filter
> source bin/activate

# Install dev dependencies
> pip install -r requirements-dev.txt

# Run tests
> inv test

# Run black and isort formatters
> inv reformat

# Run flake8 linter
> inv lint

# Run mypy type checker
> inv type-check

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
[invoke]: https://github.com/pyinvoke/invoke
