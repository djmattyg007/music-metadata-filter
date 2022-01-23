import re
from functools import reduce
from typing import Callable, Iterable

from .rules import (
    CLEAN_EXPLICIT_FILTER_RULES,
    FEATURE_FILTER_RULES,
    LIVE_FILTER_RULES,
    NORMALIZE_FEATURE_FILTER_RULES,
    PARODY_FILTER_RULES,
    REISSUE_FILTER_RULES,
    REMASTERED_FILTER_RULES,
    SUFFIX_FILTER_RULES,
    TRIM_SYMBOLS_FILTER_RULES,
    VERSION_FILTER_RULES,
    YOUTUBE_TRACK_FILTER_RULES,
    FilterRule,
)


__all__ = (
    "album_artist_from_artist",
    "filter_with_filter_rules",
    "fix_track_suffix",
    "normalize_feature",
    "remove_zero_width",
    "replace_nbsp",
    "remove_clean_explicit",
    "remove_live",
    "remove_reissue",
    "remove_remastered",
    "remove_version",
    "remove_parody",
    "remove_feature",
    "youtube",
)


FilterFunction = Callable[[str], str]


def album_artist_from_artist(text: str, /) -> str:
    """Generate Album Artist from Artist when "feat. Artist B" is present."""

    if " feat. " in text:
        return text.split(" feat. ")[0]
    return text


def filter_with_filter_rules(text: str, filter_rules: Iterable[FilterRule], /) -> str:
    """Replace text in the given string according to given filter rules."""

    def reducer(text: str, filter_rule: FilterRule) -> str:
        return filter_rule.source.sub(
            filter_rule.target,
            text,
            count=filter_rule.count,
        )

    return reduce(reducer, filter_rules, text)


def fix_track_suffix(text: str, /) -> str:
    """Replace "Title - X Remix" suffix with "Title (X Remix) and similar"."""

    return filter_with_filter_rules(text, SUFFIX_FILTER_RULES)


def normalize_feature(text: str, /) -> str:
    """Generate normalized "feat. Artist B" text from [feat. Artist B] style."""

    return filter_with_filter_rules(text, NORMALIZE_FEATURE_FILTER_RULES)


def remove_clean_explicit(text: str, /) -> str:
    """Remove "Explicit" and "Clean"-like strings from the text."""

    return filter_with_filter_rules(text, CLEAN_EXPLICIT_FILTER_RULES)


def remove_feature(text: str, /) -> str:
    """Remove "feat"-like strings from the text."""

    return filter_with_filter_rules(text, FEATURE_FILTER_RULES)


def remove_live(text: str, /) -> str:
    """Remove "Live..."-like strings from the text."""

    return filter_with_filter_rules(text, LIVE_FILTER_RULES)


def remove_parody(text: str, /) -> str:
    """Remove "(Parody of "X" by Y)"-like strings from the text."""

    return filter_with_filter_rules(text, PARODY_FILTER_RULES)


def remove_reissue(text: str, /) -> str:
    """Remove "Re-issue"-like strings from the text."""

    return filter_with_filter_rules(text, REISSUE_FILTER_RULES)


def remove_remastered(text: str, /) -> str:
    """Remove "Remastered..."-like strings from the text."""

    return filter_with_filter_rules(text, REMASTERED_FILTER_RULES)


def remove_version(text: str, /) -> str:
    """Remove "(Single|Album|Mono version}"-like strings from the text."""

    return filter_with_filter_rules(text, VERSION_FILTER_RULES)


def remove_zero_width(text: str, /) -> str:
    """Remove zero-width characters from given string."""

    return re.sub("[\u200B-\u200D\uFEFF]", "", text)


def replace_nbsp(text: str, /) -> str:
    """Replace all non-breaking space symbols with a space symbol."""

    return text.replace("\u00a0", "\u0020")


def youtube(text: str, /) -> str:
    return filter_with_filter_rules(
        text,
        (
            *YOUTUBE_TRACK_FILTER_RULES,
            *TRIM_SYMBOLS_FILTER_RULES,
        ),
    )
