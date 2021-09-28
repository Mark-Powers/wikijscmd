import requests
import sys
import json
from wikijscmd.config import config

def handle_errors(r):
    error = False
    if r.status_code != 200:
        error = True
        print("Error status code: %s" % r.status_code)
    json = r.json()
    if "errors" in json:
        error = True
        for e in json["errors"]:
            print(e["message"])
            print(e)
    if error:
        sys.exit(1)


def get_headers():
    return { "Authorization": "Bearer %s" % config["wiki"]["key"] } 

def send_query(query, query_vars):
    '''Returns status code, json'''
    payload = { "query": query, "variables": query_vars}
    r = requests.post(config["wiki"]["url"], json=payload, headers = get_headers())
    handle_errors(r)
    return r.json()

