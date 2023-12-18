from dataclasses import dataclass
import re

@dataclass
class Issn:
    """International Standard Serial Number (ISSN) representation.
    
    The ISSN is an eight-digit serial number used to uniquely identify a serial publication, such 
    as journals, magazines, newspapers, anual publications etc.
    """

    def __init__(self, issn_code: str):
        self.validate_issn(issn_code)
        self.issn = issn_code

    def validate_issn(self, code: str) -> None:
        if not re.match(r'^\d{4}-\d{3}[\dX]$', code):
            raise ValueError(f'The following string is not a valid ISSN: \"{code}\"')
        
        code_without_hiphen = code.replace('-', '')
        digits = (int(i) for i in code_without_hiphen[:7])
        validator_digit = int(10 if code_without_hiphen[7] == 'X' else code_without_hiphen[7])

        digits_positional_sum = 0
        for digit, position in zip(digits, range(8, 1, -1)):
            aux = digit * position
            digits_positional_sum += aux
        
        calculated_validator_digit = 11 - digits_positional_sum % 11 if digits_positional_sum % 11 > 0 else 0
        if validator_digit != calculated_validator_digit:
            raise ValueError(f'The following format is correct but the value is invalid: \"{code}\"')

    def __str__(self):
        return self.issn
