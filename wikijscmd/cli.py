#!/usr/bin/env python3

import sys
import argparse

from wikijscmd.config import config
from wikijscmd.commands import create, edit, single, tree, today, move, fill_in_pages

def cli():
    parser = argparse.ArgumentParser("wikijscmd")
    parser.set_defaults(command=None)
    subparsers = parser.add_subparsers()

    parser_create = subparsers.add_parser("create", help="create a page")
    parser_create.add_argument("path", type=str, help="the path of the new page")
    parser_create.add_argument("title", type=str, help="the title of the new page")
    parser_create.add_argument("content", nargs="?", type=str, help="optional page content")
    parser_create.set_defaults(command=create)

    parser_tree = subparsers.add_parser("tree", help="search in the page tree")
    parser_tree.add_argument("regex", type=str, help="optional regex to search paths with")
    parser_tree.set_defaults(command=tree)

    parser_single = subparsers.add_parser("single", help="view a single page")
    parser_single.add_argument("path", type=str, help="the path of the page to view")
    parser_single.set_defaults(command=single)

    parser_edit = subparsers.add_parser("edit", help="edit a page")
    parser_edit.add_argument("path", type=str, help="the path of the page to edit")
    parser_edit.set_defaults(command=edit)

    parser_today = subparsers.add_parser("today", help="create/edit the journal page for today")
    parser_today.set_defaults(command=today)

    parser_move = subparsers.add_parser("move", help="move a page")
    parser_move.add_argument("source", type=str, help="the path of the page to move")
    parser_move.add_argument("dest", type=str, help="the destination path")
    parser_move.set_defaults(command=move)

    parser_journal = subparsers.add_parser("journal", help="create journal pages")
    parser_journal.set_defaults(command=fill_in_pages)

    args = vars(parser.parse_args())
    callback = args["command"]
    if callback is None:
        parser.print_help()
    else:
        del args["command"]
        callback(**args)

if __name__ == "__main__":
    main()
