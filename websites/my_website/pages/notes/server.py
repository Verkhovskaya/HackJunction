import sys
import os
from bottle import route, run, request, static_file
import datetime

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

@route('/css')
def css():
    return static_file("main.css", page_path + "/css")


@route('/js')
def js():
    return static_file("main.js", page_path + "/javascript")


@route('save_file/<file_name>/<file_text>')
def save_file(file_name, file_text):
    save_to = open(page_path + "/data/" + file_name, "w")
    save_to.write(file_text)
    save_to.close()


@route("/")
def new_note():
    if not os.path.isfile(page_path + "/data/new_note"):
        save_file('new_note', "Write something here :)")
    return open_file('new_note')


@route('/open/<page>')
def open_file(page):
    links = os.listdir(page_path + '/data')
    link_text = "\n".join(["<a href=\"/open/" + link_name + "\">" + link_name + "</a>" for link_name in links])
    body_text = open(page_path + '/data/' + page).read()
    text = open(page_path + '/html/header.html').read().\
            replace("$$meta_header$$", meta_header(request)) + \
        open(page_path + '/html/nav.html').read().\
           replace("$$links$$", link_text) +\
        open(page_path + "/html/top_bar.html").read().\
           replace("$$note_title$$", page).\
           replace("$$note_title$$", page) + \
        open(page_path + '/html/body.html').read().\
           replace("$$body_text$$", body_text).replace("$$note_title$$", str(page)) +\
        open(page_path + '/html/footer.html').read()
    return text


@route("/delete/<page>")
def delete(page):
    os.remove(page_path + "/data/" + page)
    if page == "new_note":
        return new_note()
    return open_file(page)


@route('/codemirror/<dir>/<filename>')
def codemirror_file(dir, filename):
    return static_file(filename, page_path + "/logic")


run(host='0.0.0.0', port=port, debug=True)