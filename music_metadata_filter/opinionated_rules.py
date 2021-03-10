import re

from .rules import FilterRule


SUFFIX_FILTER_RULES = (
    # "- X Remix" -> "(X Remix)" and similar
    FilterRule(
        source=re.compile(r"""-\s(.+?)\s((Re)?mix|edit|dub|mix|vip|version)$""", flags=re.IGNORECASE),
        target=r"""(\1 \2)""",
        count=1,
    ),
    FilterRule(
        source=re.compile(r"""-\s(Live|Remix|VIP|Instrumental)$""", flags=re.IGNORECASE),
        target=r"""(\1)""",
        count=1,
    ),
)


__all__ = [
    "SUFFIX_FILTER_RULES",
]
