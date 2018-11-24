import sys
import os
from bottle import route, run, request

if len(sys.argv) == 1:
    port = 8080
else:
    port = sys.argv[1]

program_path = os.getcwd()
if "/root" in program_path:
    root_path = "/root"
    page_path = "/root/" + program_path.split("/")[-1]
else:
    root_path = "/".join(program_path.split("/")[:-2])
    page_path = program_path

sys.path.append(root_path)
print(program_path)
from shared_utils import meta_header

@route('/')
def hello():
    domain = request.get_header('host')
    text = open(page_path + '/html/header.html').read().\
           replace("$$meta_header$$", meta_header(request))+ \
        open(page_path + '/html/root_page.html').read().\
           replace("$$domain$$", domain).\
           replace("$$domain$$", domain).\
           replace("$$domain$$", domain).\
           replace("$$domain$$", domain) +\
        open(page_path + '/html/footer.html').read()
    return text


run(host='0.0.0.0', port=port, debug=True)