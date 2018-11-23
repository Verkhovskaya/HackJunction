import sys
import os
from bottle import route, run, request

if len(sys.argv) == 1:
    port = 8080
else:
    port = sys.argv[1]

if len(sys.argv) == 1:
    root_path = os.getcwd()
else:
    root_path = sys.argv[2]


@route('/')
def hello():
    domain = request.get_header('host')
    text = open(root_path + '/html/header.html').read() + \
        open(root_path + '/html/root_page.html').read().\
           replace("$$domain$$", domain).\
           replace("$$domain$$", domain).\
           replace("$$domain$$", domain).\
           replace("$$domain$$", domain) +\
        open(root_path + '/html/footer.html').read()
    return text


run(host='0.0.0.0', port=port, debug=True)