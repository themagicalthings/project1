import pytest
from project1 import redactor
def test_redact_address():
    text = "I am from New York, and my friend is from Paris."
    expected_output = "I am from ████████, and my friend is from █████."
    assert redactor.redact_address(text) == expected_output

