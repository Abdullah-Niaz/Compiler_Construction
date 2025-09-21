import re

token_specification = [
    ("NUMBER",   r'\d+(\.\d*)?'),   # Integer or decimal number
    ("ASSIGN",   r'='),             # Assignment operator
    ("END",      r';'),             # Statement terminator
    ("ID",       r'[A-Za-z_]\w*'),  # Identifiers
    ("OP",       r'[+\-*/]'),       # Arithmetic operators
    ("NEWLINE",  r'\n'),            # Line endings
    ("SKIP",     r'[ \t]+'),        # Skip spaces and tabs
    ("MISMATCH", r'.'),             # Any other character
]


tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
get_token = re.compile(tok_regex).match

def lexical_analyzer(code):
    line_num = 1
    pos = line_start = 0
    tokens = []
    mo = get_token(code)
    
    while mo:
        kind = mo.lastgroup
        value = mo.group()
        if kind == "NUMBER":
            value = float(value) if '.' in value else int(value)
            tokens.append((kind, value))
        elif kind == "ID":
            if value in {"if", "else", "while", "for"}:  # Keywords
                kind = "KEYWORD"
            tokens.append((kind, value))
        elif kind == "NEWLINE":
            line_start = pos
            line_num += 1
        elif kind == "SKIP":
            pass
        elif kind == "MISMATCH":
            raise RuntimeError(f"Unexpected character {value!r} on line {line_num}")
        else:
            tokens.append((kind, value))
        
        pos = mo.end()
        mo = get_token(code, pos)
    
    return tokens

code = """x = 10;
y = x + 5;
if y > 10
    y = y - 1;
"""
print(lexical_analyzer(code))
