import pytest
from project1 import redactor
def test_redact_names():
    text = "John Doe is a software engineer at XYZ Corporation."
    expected_output = "████████ is a software engineer at ███████████████."
    assert redactor.redact_names(text) == expected_output

