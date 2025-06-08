import re

patterns = [ r"kill myself", r"end my life", r"suicide", r"self harm" ]

compiled = [re.compile(p, re.IGNORECASE) for p in patterns]

def is_safe(text): 
    return not any(p.search(text) for p in compiled)