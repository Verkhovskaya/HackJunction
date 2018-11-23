import sys
import os
from bottle import route, run

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
    text = open(root_path + "/html/header.html").read() + \
        open(root_path + '/html/root_page.html').read() +\
        open(root_path + "/html/footer.html").read()
    return text


@post('/setup_new_page')
def setup_new_page():
    ip_address = request.forms.get('ip_address')
    password = request.forms.get('password')
    try:
        os.system("ssh root@" + ip_address + )

    text = open(root_path + "/html/header.html").read() + \
        open(root_path + '/html/new_page.html').read() +\
        open(root_path + "/html/footer.html").read()
    return text


run(host='0.0.0.0', port=port, debug=True)