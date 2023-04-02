import pytest
from project1 import redactor
def test_redact_phones():
    text = "You can contact me at 123-456-7890 or 098-765-4321."
    expected_output = "You can contact me at █ or █."
    assert redactor.redact_phones(text) == expected_output

