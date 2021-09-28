from wikijscmd import graphql_queries
import subprocess
import re
import os

def print_item(item):
    trimmmed_path = item["path"][:17]+"..." if len(item["path"]) > 20 else item["path"]
    print("| %6s | %20s | %44s |" % (item["id"], trimmmed_path, item["title"]) )

def get_single_page(path):
    """
    Gets the page from the wiki with the given path
    """
    if path.startswith("/"):
        path = path[1:]
    for item in graphql_queries.get_tree()["data"]["pages"]["list"]:
        if path == item["path"]:
            page_id = int(item["id"])
            response = graphql_queries.get_single_page(page_id)
            return response["data"]["pages"]["single"]
    return None

def get_tree(regex):
    response = graphql_queries.get_tree()
    pages = []
    for item in response["data"]["pages"]["list"]:
        if not re.search(regex, item["path"]):
            continue
        pages.append(item)
    return pages

def clean_filename(pathname):
    """
    Clean the path so that it can be used as a filename
    """
    pathname = str(pathname).strip().replace('/', '_')
    pathname = re.sub(r'\W', '', pathname)
    return pathname[:200]

def open_editor(action, pathname, initial_body):
    """
    Open a page with the given pathname and intial_body in an editor, using
    action in the filename. Returns the content of the edited file.
    """
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

def args_for_date(date):
    return {
        "path": date.strftime("journal/%Y/%b/%d").lower(),
        "title": date.strftime("%B %-d"),
    }
