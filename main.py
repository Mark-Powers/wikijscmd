#!/usr/bin/python3
import sys
import os
import subprocess
import re
import datetime
import argparse

from config import config
import graphql_queries

def print_item(item):
    trimmmed_path = item["path"][:17]+"..." if len(item["path"]) > 20 else item["path"]
    print("| %6s | %20s | %44s |" % (item["id"], trimmmed_path, item["title"]) )

def today(args):
    today = datetime.datetime.now()
    path = today.strftime("journal/%Y/%b/%d").lower()
    if get_single_page(path) is not None:
        edit({"path": path})
    else:
        date_int = int(today.strftime("%d"))
        title = today.strftime("%B ") + str(date_int)
        create([path, title])

def create(args):
    page = get_single_page(args["path"])
    if page is not None:
        print("Page already exists with path: %s" % args["path"])
        if input("Edit it? (y/n) ") == "y":
            edit(args)
            return
    title = args["title"]
    if "content" in args:
        content = open_editor("create", path, "")
    else:
        content = args["content"]
    response = graphql_queries.create_page(content, title, path)
    result = response["data"]["pages"]["create"]["responseResult"]
    if not result["succeeded"]:
        print("Error!", result["message"])
        sys.exit(1)
    print(result["message"])

def tree(args):
    response = graphql_queries.get_tree()
    regex = " ".join(args["regex"])
    for item in response["data"]["pages"]["list"]:
        if not re.search(regex, item["path"]):
            continue
        print_item(item)

def get_single_page(path):
    if path.startswith("/"):
        path = path[1:]
    for item in graphql_queries.get_tree()["data"]["pages"]["list"]:
        if path == item["path"]:
            page_id = int(item["id"])
            response = graphql_queries.get_single_page(page_id)
            return response["data"]["pages"]["single"]
    return None

def single(args):
    page = get_single_page(args["path"])
    if page is None:
        print("No page with path: %s" % args["path"])
        sys.exit(1)
    print("-" * 80)
    print_item(page)
    print("-" * 80)
    print(page["content"])

def move(args):
    source = args["src_path"]
    dest = args["dst_path"]
    page = get_single_page(source)
    if page is None:
        print("Source page %s does not exist" % source)
        sys.exit(1)
    response = graphql_queries.move_page(page["id"], dest)
    result = response["data"]["pages"]["move"]["responseResult"]
    if not result["succeeded"]:
        print("Error!", result["message"])
        sys.exit(1)
    print(result["message"])

def clean_filename(pathname):
    pathname = str(pathname).strip().replace('/', '_')
    pathname = re.sub(r'\W', '', pathname)
    return pathname[:200]

def open_editor(action, pathname, initial_body):
    if "VISUAL" in os.environ:
        editor = os.environ['VISUAL']
    else:
        editor = os.environ['EDITOR']
    filename = "/tmp/wikijscmd-"+action+"-"+clean_filename(pathname)+".md"
    if len(initial_body) > 0:
        with open(filename, "w") as f:
            f.write(initial_body)
    subprocess.run([editor, filename])
    with open(filename, "r") as f:
        new_body = f.read()
    os.remove(filename)
    return new_body

def edit(args):
    page = get_single_page(args["path"])
    if page is None:
        print("No page with path: %s" % args["path"])
        if input("Create it? (y/n) ") == "y":
            title = input("Enter the title: ").strip()
            create({"path": args["path"], "title": title})
        return
    body = page["content"]

    # Open it in editor
    new_body = open_editor("edit", args["path"], body)

    # Prompt user to save it to the wiki
    print_item(page)
    print("-" * 80)
    print(new_body)
    print("-" * 80)
    if input("Save changes? (y/n) ") == "y":
        response = graphql_queries.edit_page(page["id"], new_body, page["title"], page["path"])
        result = response["data"]["pages"]["update"]["responseResult"]
        if not result["succeeded"]:
            print("Error!", result["message"])
            sys.exit(1)
        print(result["message"])

def no_command(args):
    print("Please use a command")

def main():
    parser = argparse.ArgumentParser("wikijscmd")
    #parser.add_argument("command",
    #        choices=["create", "tree", "single", "edit", "today", "move"])
    parser.set_defaults(command=None)
    subparsers = parser.add_subparsers()

    parser_create = subparsers.add_parser("create", help="create a page")
    parser_create.add_argument("path", type=str, help="the path of the new page")
    parser_create.add_argument("title", type=str, help="the title of the new page")
    parser_create.add_argument("content", nargs='*', type=str, help="optional page content")
    parser_create.set_defaults(command=create)

    parser_tree = subparsers.add_parser("tree", help="search in the page tree")
    parser_tree.add_argument("regex", nargs='*', type=str, help="optional regex to search paths with")
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
    parser_move.add_argument("src_path", type=str, help="the path of the page to move")
    parser_move.add_argument("dst_path", type=str, help="the destination path")
    parser_move.set_defaults(command=move)

    args = vars(parser.parse_args())
    callback = args["command"]
    if callback is None:
        parser.print_help()
    else:
        del args["command"]
        callback(args)


if __name__ == "__main__":
    main()
