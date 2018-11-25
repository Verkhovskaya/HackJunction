import sys
import os
from bottle import route, run

if len(sys.argv) == 1:
    port = 8080
else:
    port = sys.argv[1]

program_path = os.getcwd()
if "/root" in program_path:
    root_path = "/root"
    page_path = "/root/" + program_path.split("/")[-1]
else:
    root_path = program_path
    page_path = program_path


@route('/')
def hello():
    text = open(page_path + "/html/header.html").read() + \
        open(page_path + '/html/root_page.html').read() +\
        open(page_path + "/html/footer.html").read()
    return text


run(host='0.0.0.0', port=port, debug=True)