# Jesse Hicklen
# Assignment 3 : Parser Main
# CS-414
#

from HicklenTokenizer import tokenize
from HicklenParser import Parser, ParseError

def run(line: str):
    print(f"\nInput: {line}")
    tokens = tokenize(line)
    print("Tokens:", tokens)
    try:
        parser = Parser(tokens)
        ast = parser.parse()
        print("AST:", ast)
    except ParseError as e:
        print("ParseError:", e)

if __name__ == "__main__":
    tests = [
        "ls",
        "ls \\",
        "ls folder",
        "cd",
        "cd mydocs",
        "cat ABCDEFGH.TXT",
        "print ABCDEFGH.PRN",
        "exec ABCDEFGH.EXE",
        "ls folder\\sub",
        "exec badname.exe"   # should fail
    ]
    for t in tests:
        run(t)
