
# B4 - Testarea detectorului de brute force

from collections import Counter
import pytest
from detector import suspecti


def test_pragul_taie():
    c = Counter({"a": 13, "b": 2})

    assert suspecti(c, 10) == [("a", 13)]


def test_prag_invalid():
    with pytest.raises(ValueError):
        suspecti({}, 0)
