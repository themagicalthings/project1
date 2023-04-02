import pytest
from project1 import redactor
def test_redact_genders():
    text = "John is a man. He is talking to his sister, Jane, who is a woman."
    expected_output = "John is a █. He is talking to his █, Jane, who is a █."
    assert redactor.redact_genders(text) == expected_output

