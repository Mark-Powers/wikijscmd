#!/usr/bin/python3
import sys
import os
import subprocess
from config import config
import graphql_queries
import re
import datetime

def print_item(item):
    trimmmed_path = item["path"][:17]+"..." if len(item["path"]) > 20 else item["path"]
    print("| %6s | %20s | %44s |" % (item["id"], trimmmed_path, item["title"]) )

def today(argv):
    if len(argv) != 0:
        print("Usage: ./main.py today")
    today = datetime.datetime.now()
    path = today.strftime("journal/%Y/%b/%d").lower()
    if get_single_page([path]) is not None:
        edit([path])
    else:
        date_int = int(today.strftime("%d"))
        title = today.strftime("%B ") + str(date_int)
        create([path, title])

def create(argv):
    if len(argv) < 2 or len(argv) > 3:
        print("Usage: ./main.py create <path> <title> <content?>")
        sys.exit(1)
    path = argv[0]
    page = get_single_page(argv)
    if page is not None:
        print("Page already exists with path: %s" % argv[0])
        if input("Edit it? (y/n) ") == "y":
            edit([path])
            return
    title = argv[1]
    if len(argv) == 2:
        content = open_editor("create", path, "")
    else:
        content = argv[2]
    response = graphql_queries.create_page(content, title, path)
    result = response["data"]["pages"]["create"]["responseResult"]
    if not result["succeeded"]:
        print("Error!", result["message"])
        sys.exit(1)
    print(result["message"])

def tree(argv):
    response = graphql_queries.get_tree()
    for item in response["data"]["pages"]["list"]:
        if len(argv) == 1 and not re.search(argv[0], item["path"]):
            continue
        print_item(item)

def get_single_page(argv):
    argument = argv[0]
    if not argument.isdigit():
        # Strip leading slash
        if argument.startswith("/"):
            argument = argument[1:]
        found = False
        for item in graphql_queries.get_tree()["data"]["pages"]["list"]:
            if argument == item["path"]:
                argument = item["id"]
                found = True
        if not found:
            return None
    page_id = int(argument)
    response = graphql_queries.get_single_page(page_id)
    return response["data"]["pages"]["single"]

def single(argv):
    if len(argv) != 1:
        print("Usage: ./main.py single <id|path>")
        sys.exit(1)
    page = get_single_page(argv)
    if page is None:
        print("No page with path: %s" % argument)
    print("-" * 80)
    print_item(page)
    print("-" * 80)
    print(page["content"])

def move(argv):
    if len(argv) != 2:
        print("Usage: ./main.py move <src> <dest>")
        sys.exit(1)
    source = argv[0]
    dest = argv[1]
    page = get_single_page([source])
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
    filename = "/tmp/wikijscmd-"+action+"-"+clean_filename(pathname)
    if len(initial_body) > 0:
        with open(filename, "w") as f:
            f.write(initial_body)
    subprocess.run([editor, filename])
    with open(filename, "r") as f:
        new_body = f.read()
    os.remove(filename)
    return new_body

def edit(argv):
    # Load content to edit
    if len(argv) != 1:
        print("Usage: ./main.py edit <id|path>")
        sys.exit(1)
    page = get_single_page(argv)
    if page is None:
        print("No page with path: %s" % argv[0])
        if input("Create it? (y/n) ") == "y":
            title = input("Enter the title: ").strip()
            create([argv[0], title])
        return
    body = page["content"]

    # Open it in editor
    new_body = open_editor("edit", argv[0], body)

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

def main():
    if len(sys.argv) < 2:
        print("Usage: ./main.py <command> <args>")
        print("Commands:")
        print("\tcreate <path> <title> <content?>")
        print("\ttree <regex?>")
        print("\tsingle <id|path>")
        print("\tedit <id|path>")
        print("\ttoday")
        print("\tmove <source_path|id> <dest_path>")
        sys.exit(0)
    commands = {
        "create": create,
        "tree": tree,
        "single": single,
        "edit": edit,
        "today": today,
        "move": move
    }
    command = sys.argv[1]
    if command in commands:
        # Pass in arguments after the command
        commands[command](sys.argv[2:])
    else:
        print("Unknown command: %s" % sys.argv[1])

if __name__ == "__main__":
    main()
