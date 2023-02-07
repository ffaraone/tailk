import re

from rich.highlighter import RegexHighlighter

from tailk.constants import DEFAULT_HIGHLIGHT_PATTERNS, RESERVED_GROUP_NAMES


class TailKHighlighter(RegexHighlighter):
    base_style = 'tailk.'
    def __init__(self, highlights=None):
        super().__init__()
        self.highlights = (
            DEFAULT_HIGHLIGHT_PATTERNS
            + self.process_highlight_patterns(highlights)
        )

    def process_highlight_patterns(self, highlights):
        patterns = []
        seen_groups = []
        idx = 0
        for pattern in highlights or []:
            compiled = re.compile(pattern)
            named_groups = set(compiled.groupindex.keys())
            if set(seen_groups) & set(named_groups):
                raise Exception(
                    'capturing group names cannot be repeated: '
                    f'{set(seen_groups) & set(named_groups)}'
                )
            if  RESERVED_GROUP_NAMES & named_groups:
                raise Exception(
                    'invalid capturing group names: '
                    f'{RESERVED_GROUP_NAMES & set(named_groups)}'
                )

            if named_groups:
                seen_groups.extend(named_groups)
                patterns.append(pattern)
                continue

            patterns.append(f'(?P<p{idx}>{pattern})')
            idx += 1
        return patterns
            


