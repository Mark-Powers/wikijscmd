import sys

from wikijscmd import graphql_queries
from datetime import datetime, timedelta
from wikijscmd.util import clean_filename, get_tree, open_editor, get_single_page, print_item, args_for_date

def create(path, title, content=None):
    page = get_single_page(path)
    if page is not None:
        print("Page already exists with path: %s" % path)
        if input("Edit it? (y/n) ") == "y":
            edit(path)
            return
    if not content:
        content = open_editor("create", path, "")
    response = graphql_queries.create_page(content, title, path)
    result = response["data"]["pages"]["create"]["responseResult"]
    if not result["succeeded"]:
        print("Error!", result["message"])
        sys.exit(1)
    print(result["message"])

def tree(regex):
    """
    Finds pages based on a path search
    """
    for item in get_tree(regex):
        print_item(item)

def single(path, raw=False):
    """
    View a page with the given path
    """
    page = get_single_page(path)
    if page is None:
        print("No page with path: %s" % path)
        sys.exit(1)
    if raw:
        print("-" * 80)
        print_item(page)
        print("-" * 80)
    print(page["content"])

def move(source, dest):
    """
    Move a page from one path to another
    """
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

def edit(path, save=False):
    """
    Edit a page
    """
    page = get_single_page(path)
    if page is None:
        print("No page with path: %s" % path)
        if input("Create it? (y/n) ") == "y":
            title = input("Enter the title: ").strip()
            create(path, title)
        return
    body = page["content"]

    # Open it in editor
    new_body = open_editor("edit", path, body)

    # Prompt user to save it to the wiki
    print_item(page)
    print("-" * 80)
    print(new_body)
    print("-" * 80)
    if save or input("Save changes? (y/n) ") == "y":
        response = graphql_queries.edit_page(page["id"], new_body, page["title"], page["path"])
        result = response["data"]["pages"]["update"]["responseResult"]
        if not result["succeeded"]:
            print("Error!", result["message"])
            sys.exit(1)
        print(result["message"])

def fill_in_pages():
    last_date = None
    for page in get_tree("journal"):
        try:
            date = datetime.strptime(page["path"], "journal/%Y/%b/%d")
            if last_date is None or date > last_date:
                last_date = date
        except ValueError:
            continue
    today = datetime.now().date()
    if last_date is None:
        last_date = today
    pending_date = last_date.date()
    while pending_date < today:
        pending_date += timedelta(days=1)
        create(**args_for_date(pending_date))

def today():
    """
    Creates a journal page with the path "journal/YYYY/MM/DD"
    """
    args = args_for_date(datetime.now().date())
    if get_single_page(args["path"]) is not None:
        edit(args["path"])
    else:
        create(**args)
