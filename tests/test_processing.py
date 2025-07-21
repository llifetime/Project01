import pytest
from src.processing import filter_by_state


@pytest.fixture
def sample_data():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-10-01"},
        {"id": 2, "state": "PENDING", "date": "2023-10-03"},
        {"id": 3, "state": "EXECUTED", "date": "2023-10-02"},
        {"id": 4, "state": "FAILED", "date": "2023-10-04"},
        {"id": 5, "state": "", "date": "invalid-date"},
        {"id": 6, "date": "2023-10-05"},  # Нет статуса
    ]


@pytest.mark.parametrize("state, expected", [
    ("EXECUTED", [1, 3]),
    ("PENDING", [2]),
    ("FAILED", [4]),
    ("UNKNOWN", []),
    ("", [5]),
    (None, [6]),
])
def test_filter_by_state(sample_data, state, expected):
    result = filter_by_state(sample_data, state)
    assert [x["id"] for x in result] == expected
