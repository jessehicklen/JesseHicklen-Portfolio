# Jesse Hicklen
# Assignment 3 : Tokenizer
# CS-414
#

import re
from dataclasses import dataclass
from typing import List

@dataclass
class Token:
    type: str
    text: str

    def __repr__(self):
        return f"Token({self.type!r}, {self.text!r})"

COMMANDS = {"ls", "cd", "cat", "print", "exec"}

def tokenize(line: str) -> List[Token]:
    tokens: List[Token] = []
    i, n = 0, len(line)

    while i < n:
        c = line[i]
        if c.isspace():
            i += 1
            continue
        if c == "\\":
            tokens.append(Token("BACKSLASH", "\\"))
            i += 1
            continue
        if c == ".":
            tokens.append(Token("DOT", "."))
            i += 1
            continue
        if c.isalpha():
            start = i
            while i < n and line[i].isalpha():
                i += 1
            word = line[start:i]

            # check for filename (8.3)
            if i < n and line[i] == ".":
                j = i + 1
                ext = ""
                while j < n and line[j].isalpha():
                    ext += line[j]
                    j += 1
                if len(word) == 8 and len(ext) == 3:
                    tokens.append(Token("FILENAME", word + "." + ext))
                    i = j
                    continue
            # otherwise check command vs ident
            if word.lower() in COMMANDS:
                tokens.append(Token("COMMAND", word.lower()))
            else:
                tokens.append(Token("IDENT", word))
            continue

        tokens.append(Token("ERROR", c))
        i += 1

    tokens.append(Token("EOF", ""))
    return tokens
