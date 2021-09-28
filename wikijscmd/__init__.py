from wikijscmd import cli
from wikijscmd import ncurses

def main():
    cli.cli()

def tui():
    try:
        ncurses.wrapper(m)
    except Exception as e:
        raise e
