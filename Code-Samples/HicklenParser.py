# Jesse Hicklen
# Assignment 3 : Parser
# CS-414
#


#EBNF Grammar (start symbol = <command>)
#
#<command>       ::= <ls-command> | <cd-command> | <cat-command> | <print-command> | <exec-command>
#
#<ls-command>    ::= "ls" [ <path> ]
#<cd-command>    ::= "cd" [ <path> ]
#<cat-command>   ::= "cat" <filename>
#<print-command> ::= "print" <filename>
#<exec-command>  ::= "exec" <filename>
#
#<path>          ::= "\" | <folder> { "\" <folder> }
#<folder>        ::= <folder-name>
#<folder-name>   ::= <letter> { <letter> }   -- 1..8 letters (A-Z, a-z)
#
#<filename>      ::= <name8> "." <ext3>
#<name8>         ::= <letter> <letter> <letter> <letter> <letter> <letter> <letter> <letter>
#<ext3>          ::= <letter> <letter> <letter>
#
#<letter>        ::= "A".."Z" | "a".."z"


from dataclasses import dataclass
from typing import List, Optional
from HicklenTokenizer import Token, tokenize

# AST Nodes 
@dataclass
class ASTNode: pass

@dataclass
class LSNode(ASTNode):
    path: Optional[List[str]]

@dataclass
class CDNode(ASTNode):
    path: Optional[List[str]]

@dataclass
class CatNode(ASTNode):
    filename: str

@dataclass
class PrintNode(ASTNode):
    filename: str

@dataclass
class ExecNode(ASTNode):
    filename: str

# ----- Parser -----
class ParseError(Exception): pass

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.i = 0

    def peek(self) -> Token:
        return self.tokens[self.i]

    def advance(self) -> Token:
        tok = self.tokens[self.i]
        self.i += 1
        return tok

    def expect(self, ttype: str) -> Token:
        tok = self.peek()
        if tok.type == ttype:
            return self.advance()
        raise ParseError(f"Expected {ttype}, got {tok.type} ({tok.text})")

    def parse(self) -> ASTNode:
        tok = self.peek()
        if tok.type != "COMMAND":
            raise ParseError(f"Expected a command, got {tok}")
        cmd = tok.text
        self.advance()

        if cmd == "ls":
            if self.peek().type in ("BACKSLASH", "IDENT"):
                path = self.parse_path()
                self.expect("EOF")
                return LSNode(path)
            self.expect("EOF")
            return LSNode(None)

        if cmd == "cd":
            if self.peek().type in ("BACKSLASH", "IDENT"):
                path = self.parse_path()
                self.expect("EOF")
                return CDNode(path)
            self.expect("EOF")
            return CDNode([])

        if cmd in ("cat", "print", "exec"):
            if self.peek().type == "FILENAME":
                fn = self.advance().text
                self.expect("EOF")
                if cmd == "cat": return CatNode(fn)
                if cmd == "print": return PrintNode(fn)
                if cmd == "exec": return ExecNode(fn)
            raise ParseError(f"{cmd} requires an 8.3 filename")

        raise ParseError(f"Unknown command {cmd}")

    def parse_path(self) -> List[str]:
        parts = []
        if self.peek().type == "BACKSLASH":
            self.advance()
            if self.peek().type == "EOF":
                return []
            while True:
                parts.append(self.expect("IDENT").text)
                if self.peek().type == "BACKSLASH":
                    self.advance()
                else:
                    break
            return parts
        while True:
            parts.append(self.expect("IDENT").text)
            if self.peek().type == "BACKSLASH":
                self.advance()
            else:
                break
        return parts
