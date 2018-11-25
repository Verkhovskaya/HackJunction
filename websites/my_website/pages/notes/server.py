import sys
import os
from bottle import route, run, request, static_file, post, response, redirect
import datetime
import json

if len(sys.argv) == 1:
    port = 8080
else:
    port = sys.argv[1]

program_path = os.getcwd()
if "/root" in program_path:
    root_path = "/root/my_website"
    page_path = os.path.dirname(os.path.abspath(__file__))
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


@post('/save')
def save_file():
    form = json.loads(request.forms.keys()[0])
    print(form)
    file_name = form.get('name')
    file_text = form.get('body')
    save_to = open(page_path + "/data/" + file_name, "w")
    save_to.write(file_text)
    save_to.close()


@route("/")
def new_note():
    response.set_cookie("notes", "yes")
    if not os.path.isfile(page_path + "/data/new_note"):
        new_note = open(page_path + "/data/new_note", "w")
        new_note.write("Write something here :)")
        new_note.close()
    return redirect("/notes/open/new_note")


@route('/open/<page>')
def open_file(page):
    links = os.listdir(page_path + '/data')
    link_text = "\n".join(["<a href=\"/notes/open/" + link_name + "\">" + link_name + "</a>" for link_name in links])
    body_text = open(page_path + '/data/' + page).read()
    text = open(page_path + '/html/header.html').read().\
            replace("$$meta_header$$", meta_header(request, override="notes")) + \
        open(page_path + '/html/nav.html').read().\
           replace("$$links$$", link_text) +\
        open(page_path + "/html/top_bar.html").read().\
           replace("$$note_title$$", page).\
           replace("$$note_title$$", page) + \
        open(page_path + '/html/body.html').read().replace("$$note_title$$", str(page)) +\
        open(page_path + '/html/footer.html').read()
    return text


@route('/note/<name>')
def note_text(name):
    return open(page_path + '/data/' + name).read()


@route("/delete/<page>")
def delete(page):
    os.remove(page_path + "/data/" + page)
    if page == "new_note":
        return new_note()
    return redirect("/notes/open/new_note")


@route('/codemirror/<dir>/<filename>')
def codemirror_file(dir, filename):
    return static_file(filename, page_path + "/logic")


run(host='0.0.0.0', port=port, debug=True)