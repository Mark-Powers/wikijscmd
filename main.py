#!/usr/bin/python3
import sys

from config import config
import graphql_queries, graphql_requests

def print_item(item):
    trimmmed_path = item["path"][:17]+"..." if len(item["path"]) > 20 else item["path"]
    print("| %6s | %20s | %44s |" % (item["id"], trimmmed_path, item["title"]) )

def create():
    if len(sys.argv) < 5:
        print("Usage: ./main.py create <path> <title> <content>")
        sys.exit(1)
    path = sys.argv[2]
    title = sys.argv[3]
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

def single():
    if len(sys.argv) < 3:
        print("Usage: ./main.py single <id|path>")
        sys.exit(0)
    if not sys.argv[2].isdigit():
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
    page = response["data"]["pages"]["single"]
    print("-" * 80)
    print_item(page)
    print("-" * 80)
    print(page["content"])

def main():
    if len(sys.argv) < 2:
        print("Usage: ./main.py <command> <args>")
        print("Commands:")
        print("\tcreate <path> <title> <content>")
        print("\ttree <contains?>")
        print("\tsingle <id|path>")
        sys.exit(0)

    if sys.argv[1] == "create":
        create()
    elif sys.argv[1] == "tree":
        tree()
    elif sys.argv[1] == "single":
        single()
    else:
        print("Unknown command: %s" % sys.argv[1])

if __name__ == "__main__":
    main()
