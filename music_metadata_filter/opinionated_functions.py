from .functions import filter_with_filter_rules
from .opinionated_rules import SUFFIX_FILTER_RULES


def fix_track_suffix(text: str, /) -> str:
    """Replace "Title - X Remix" suffix with "Title (X Remix) and similar"."""

    return filter_with_filter_rules(text, SUFFIX_FILTER_RULES)
