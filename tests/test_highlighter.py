import pytest

from tailk.constants import DEFAULT_HIGHLIGHT_PATTERNS
from tailk.highlighter import TailKHighlighter



def test_default_only():
    highligher = TailKHighlighter()
    assert highligher.highlights == DEFAULT_HIGHLIGHT_PATTERNS


def test_with_named_group():
    extra = [
        r'(?P<test>TEST)',
    ]
    highligher = TailKHighlighter(extra)
    assert highligher.highlights == DEFAULT_HIGHLIGHT_PATTERNS + extra


def test_without_named_group():
    extra = [
        r'(A|B)',
    ]
    highligher = TailKHighlighter(extra)
    assert highligher.highlights == DEFAULT_HIGHLIGHT_PATTERNS + [ r'(?P<p0>(A|B))']


def test_group_exists():
    extra = [
        r'(?P<test>TEST)',
        r'(?P<test>TEST)',
    ]

    with pytest.raises(Exception) as cv:
        TailKHighlighter(extra)

    assert str(cv.value).startswith('capturing group names cannot be repeated')


def test_reserved_names():
    extra = [
        r'(?P<p0>TEST)',
    ]

    with pytest.raises(Exception) as cv:
        TailKHighlighter(extra)

    assert str(cv.value).startswith('invalid capturing group names')
