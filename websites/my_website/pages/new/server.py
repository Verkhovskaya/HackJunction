import sys
import os
from bottle import route, run, request, post, static_file
import shutil
import zipfile

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


@route('/css')
def css():
    return static_file("main.css", page_path + '/css')


@route('/img/<name>')
def img(name):
    return static_file(name, page_path + '/imgs')

@post('/upload')
def upload():
    zip = request.files.get("zip_file")
    os.mkdir(page_path + '/new_upload')
    zip.save(page_path + '/new_upload')
    file_name = os.listdir(page_path + '/new_upload')[0][:-4]
    zip_ref = zipfile.ZipFile(page_path + '/new_upload/' + file_name + ".zip", 'r')
    zip_ref.extractall(page_path + '/new_upload2')
    page_name = os.listdir(page_path + '/new_upload2/' + file_name)[0]
    shutil.move(page_path + '/new_upload2/' + file_name + '/' + page_name, root_path  + '/pages/' + page_name)
    zip_ref.close()
    shutil.rmtree(page_path + '/new_upload')
    os.system("python " + root_path + "/reset_server.py")


run(host='0.0.0.0', port=port, debug=True)