import pytest
from project1 import redactor
def test_redact_dates():
    text = "I was born on January 1, 2000. We met on December 25, 2015."
    expected_output = "I was born on ███████████████. We met on █████████████████."
