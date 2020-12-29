# wikijscmd
## Description
A client to use wiki.js over the command line. Supports creating, editing,
and viewing pages, and viewing the wiki file tree.

## Usage
wikijscmd supports the following commands:

### create PATH TITLE CONTENT?
creates a page with the given page, title, and content. Content is optional, 
if none is provided, then an editor will open based on the VISUAL or EDITOR 
variable. 

### edit (PATH|ID)
opens a page in the editor based on VISUAL or EDITOR variables for the given 
path or ID parameters. An ID is the integer type for the page. Path may 
optionally start with a / to indicate that an integer only path is not an ID.

### single (PATH|ID)
prints the page contents for the given  path or ID parameters. An ID is the 
integer type for the page. Path may optionally start with a / to indicate that 
an integer only path is not an ID.

### tree PATH\_REGEX?
prints out the tree of all pages where the path matches the regex given.
Printed information includes the page title, ID, path.

### today
Creates a page with the path `YYYY/MM/DD` and title as the date name. For 
example, if the date is January 1, 1970, this is equivalent of running the
command `create 1970/01/01 "Janurary 1"`.

## Installation
Clone the repository or download the source code.

Install python3, and pip for python3 for your system.

Install the dependencies
`pip3 install -r requirements.txt`

Create a file `config.ini` with the following information:
```
[wiki]
key=YOUR_KEY_HERE
url=YOUR_GRAPHQL_ENDPOINT_HERE
```
The key is provided via the admin panel under the API access tab. The URL
for wiki.js is typically the URL of your wiki with the path `/graphql`. For
example, if your wiki is at `wiki.example.com`, the url field should be set to
`https://wiki.example.com/graphql`.

Run `main.py` in order to use the program.


## TODO
- Include options to always answer yes or no
- Allow for moving pages

