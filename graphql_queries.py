import graphql_requests

def get_single_page(page_id):
    query = 'query {\npages {\nsingle (id: %s) {\nid\npath\ntitle\ncontent\n}\n}\n}' % page_id
    return graphql_requests.send_query(query)

def create_page(content, title, path):
    query = 'mutation {\npages {\ncreate(\ncontent: "%s"\ndescription: ""\neditor: "markdown"\nisPrivate: false\nisPublished: true\nlocale: "en"\npath: "%s"\npublishEndDate: ""\npublishStartDate: ""\nscriptCss: ""\nscriptJs: ""\ntags: []\ntitle: "%s"\n) {\nresponseResult {\nsucceeded\nerrorCode\nslug\nmessage\n__typename\n}\npage {\nid\nupdatedAt\n__typename\n}\n__typename\n}\n__typename\n}\n}' % ( content, path, title )
    return graphql_requests.send_query(query)

def get_tree():
    query = 'query {\n pages {\n list (orderBy: PATH) {\n id\npath\ntitle\n}\n}\n}'
    return graphql_requests.send_query(query)
