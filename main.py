#!/usr/bin/python3
import sys
import os
import subprocess
from config import config
import graphql_queries

def print_item(item):
    trimmmed_path = item["path"][:17]+"..." if len(item["path"]) > 20 else item["path"]
    print("| %6s | %20s | %44s |" % (item["id"], trimmmed_path, item["title"]) )

def create():
    if len(sys.argv) < 4:
        print("Usage: ./main.py create <path> <title> <content?>")
        sys.exit(1)
    path = sys.argv[2]
    title = sys.argv[3]
    if len(sys.argv) == 4: 
        content = open_editor("/tmp/wikijscmd-create", "")
    else:
        content = sys.argv[4]
    response = graphql_queries.create_page(content, title, path)
    result = response["data"]["pages"]["create"]["responseResult"]
    if not result["succeeded"]:
        print("Error!", result["message"])
        sys.exit(1)
    print(result["message"])

def tree():
    response = graphql_queries.get_tree()
    for item in response["data"]["pages"]["list"]:
        if len(sys.argv) == 3 and sys.argv[2] not in item["path"]:
            continue
        print_item(item)

def get_single_page():
    if not sys.argv[2].isdigit():
        if sys.argv[2].startswith("/"):
            sys.argv[2] = sys.argv[2][1:]
        found = False
        for item in graphql_queries.get_tree()["data"]["pages"]["list"]:
            if sys.argv[2] == item["path"]:
                sys.argv[2] = item["id"]
                found = True
        if not found:
            print("No page with path: %s" % sys.argv[2])
            sys.exit(0)
    page_id = int(sys.argv[2])
    response = graphql_queries.get_single_page(page_id)
    return response["data"]["pages"]["single"]

def single():
    if len(sys.argv) < 3:
        print("Usage: ./main.py single <id|path>")
        sys.exit(0)
    page = get_single_page()
    print("-" * 80)
    print_item(page)
    print("-" * 80)
    print(page["content"])

def open_editor(filename, initial_body):
    if "VISUAL" in os.environ:
        editor = os.environ['VISUAL']
    else:
        editor = os.environ['EDITOR']
    if len(initial_body) > 0:
        with open(filename, "w") as f:
            f.write(initial_body)
    subprocess.run([editor, filename])
    with open(filename, "r") as f:
        new_body = f.read()
    os.remove(filename)
    return new_body

def edit():
    # Load content to edit
    if len(sys.argv) < 3:
        print("Usage: ./main.py edit <id|path>")
        sys.exit(0)
    page = get_single_page()
    body = page["content"]

    # Open it in editor
    new_body = open_editor("/tmp/wikijscmd-edit", body)

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
        print("\ttree <contains?>")
        print("\tsingle <id|path>")
        print("\tedit <id|path>")
        sys.exit(0)

    if sys.argv[1] == "create":
        create()
    elif sys.argv[1] == "tree":
        tree()
    elif sys.argv[1] == "single":
        single()
    elif sys.argv[1] == "edit":
        edit()
    else:
        print("Unknown command: %s" % sys.argv[1])

if __name__ == "__main__":
    main()
