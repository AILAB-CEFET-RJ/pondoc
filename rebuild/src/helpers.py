import re

def number_to_column_label(number: int) -> str:
    result = ''
    while number > 0:
        number, remainder = divmod(number - 1, 26)
        result = chr(65 + remainder) + result
    return result

def create_authorship_regex(full_name: str) -> re.Pattern:
    return re.compile(f'^({full_name[0]}\.|{full_name.split()[0]}).*{full_name.split()[-1]}$')
