from wikijscmd import custom_requests

def get_single_page(page_id):
    query = 'query ($id: Int!) {\npages {\nsingle (id: $id) {\nid\npath\ntitle\ncontent\n}\n}\n}'
    query_vars = {"id": page_id}
    return custom_requests.send_query(query, query_vars)

def create_page(content, title, path):
    query = 'mutation ($content: String!, $path: String!, $title: String!) {\npages {\ncreate(\ncontent: $content\ndescription: ""\neditor: "markdown"\nisPrivate: false\nisPublished: true\nlocale: "en"\npath: $path\npublishEndDate: ""\npublishStartDate: ""\nscriptCss: ""\nscriptJs: ""\ntags: []\ntitle: $title\n) {\nresponseResult {\nsucceeded\nerrorCode\nslug\nmessage\n__typename\n}\npage {\nid\nupdatedAt\n__typename\n}\n__typename\n}\n__typename\n}\n}'
    query_vars = {"content": content, "title": title, "path": path}
    return custom_requests.send_query(query, query_vars)

def get_tree():
    query = 'query {\n pages {\n list (orderBy: PATH) {\n id\npath\ntitle\n}\n}\n}'
    query_vars = {  }
    return custom_requests.send_query(query, query_vars)

def edit_page(page_id, content, title, path):
    query = 'mutation ($id: Int!, $content: String!, $path: String!, $title: String!){\npages {\nupdate(\nid: $id\ncontent: $content\ndescription: ""\neditor: "markdown"\nisPrivate: false\nisPublished: true\nlocale: "en"\npath: $path\npublishEndDate: ""\npublishStartDate: ""\nscriptCss: ""\nscriptJs: ""\ntags: []\ntitle: $title\n) {\nresponseResult {\nsucceeded\nerrorCode\nslug\nmessage\n__typename\n}\npage {\nid\nupdatedAt\n__typename\n}\n__typename\n}\n__typename\n}\n}'
    query_vars = {"id": page_id, "content": content, "title": title, "path": path}
    return custom_requests.send_query(query, query_vars)

def move_page(page_id, destination_path):
    query = '''mutation ($id: Int!, $destinationPath: String!, $destinationLocale: String!) {
      pages {
        move(id: $id, destinationPath: $destinationPath, destinationLocale: $destinationLocale) {
          responseResult {
            succeeded
            errorCode
            slug
            message
            __typename
          }
          __typename
        }
        __typename
      }
    }'''
    query_vars = {"id": page_id, "destinationPath": destination_path, "destinationLocale": "en"}
    return custom_requests.send_query(query, query_vars)

