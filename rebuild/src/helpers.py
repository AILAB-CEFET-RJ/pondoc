import re
from typing import Any, Dict, List

def create_authorship_regex_dict(entities: List[Any]) -> Dict[re.Pattern, Any]:
    result = {}
    for entity in entities:
        compiled_regex = create_authorship_regex(entity.full_name)
        entity.authorship_regex = compiled_regex
        result[compiled_regex] = entity
    return result

def create_authorship_regex(full_name: str) -> re.Pattern:
    return re.compile(f'^({full_name[0]}\.|{full_name.split()[0]}).*{full_name.split()[-1]}$')
