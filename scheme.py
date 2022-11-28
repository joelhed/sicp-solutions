#!/usr/bin/env python3
"""A Scheme interpreter.

This uses R7RS (https://small.r7rs.org/attachment/r7rs.pdf) loosely as a reference, but
does not strive for strict adherence.
"""
from enum import Enum, auto
from typing import List, Tuple, Union, Iterator, Any
import argparse
import logging
import sys


log = logging.getLogger("scheme")

SPECIAL_VALID_IDENT_CHARS = "!$%&*+-./:<=>?@^_~"


## Type aliases
Ident = str
Expr = List[Union[Ident, "Expr"]]


class TokenType(Enum):
    LPAREN = auto()
    RPAREN = auto()
    IDENT = auto()
    NUMBER = auto()


Token = Tuple[TokenType, Any]


def tokenize(s: str) -> Iterator[Token]:
    """Iterate over the tokens of the given string."""
    i = 0
    while i < len(s):
        if s[i].isspace():
            pass
            i += 1

        elif s[i] == "(":
            yield (TokenType.LPAREN, None)
            i += 1

        elif s[i] == ")":
            yield (TokenType.RPAREN, None)
            i += 1

        elif s[i].isalpha() or s[i] in SPECIAL_VALID_IDENT_CHARS:
            # According to R7RS, a single '.' is not an identifier.
            # I will have to figure that out...
            chars = []
            while i < len(s) and (s[i].isalnum() or s[i] in SPECIAL_VALID_IDENT_CHARS):
                chars.append(s[i])
                i += 1
            yield (TokenType.IDENT, "".join(chars))

        else:
            raise ValueError(f"unrecognized char {s[i]}")


def parse_expr(s: str) -> Expr:
    """Parse the passed Scheme expression string and return an expression."""
    # We're not dealing with potentially multi-expression strings right now.

    tokens = tokenize(s)

    return list(tokens)


def run_repl():
    """Start a read-eval-print-loop on stdin."""
    log.info("running repl")
    while True:
        try:
            line = input("scheme> ")
        except (KeyboardInterrupt, EOFError):
            break

        print(parse_expr(line))


def run_file(f):
    """Run the file object passed as a Scheme script."""
    log.info("running file")

    raise NotImplementedError("running files is not yet implemented")


def cli():
    """Run the command-line interface to the interpreter."""
    parser = argparse.ArgumentParser(
        description=__doc__,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
    )
    parser.add_argument(
        "program_file",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
    )
    args = parser.parse_args()

    loglevel = "DEBUG" if args.verbose else "WARNING"
    logging.basicConfig(level=getattr(logging, loglevel))

    if not args.program_file.isatty():
        run_file(args.program_file)
    elif args.program_file == sys.stdin:
        run_repl()
    else:
        log.error("Running a REPL from something other than stdin is not supported.")


if __name__ == "__main__":
    cli()

