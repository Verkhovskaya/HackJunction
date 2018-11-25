import sys
import os
from bottle import route, run, request, post, response, static_file, redirect
import ast
import requests
import time
import json
import shutil
import datetime
from socket import gethostname, gethostbyname

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


@route('/javascript')
def js():
    return static_file('main.js', page_path + '/javascript')


@route('/')
def get_friends():
    origin = open(root_path + "/ip_address.txt").read()
    response.set_cookie("social", "yes")
    text = open(page_path + '/html/header.html').read().\
            replace("$$meta_header$$", meta_header(request, override="social")) + \
        open(page_path + '/html/friends_photos.html').read().replace("$$my_ip$$", origin) +\
        open(page_path + '/html/footer.html').read()
    return text


@route('/stalkees')
def get_stalkees():
    if not os.path.isfile(page_path + '/data/stalkees.txt'):
        stalkees_file = open(page_path + '/data/stalkees.txt', 'w')
        stalkees_file.write(str({}))
        stalkees_file.close()
        return {}
    else:
        stalkees_file = open(page_path + '/data/stalkees.txt')
        stalkees_list = ast.literal_eval(stalkees_file.read())
        stalkees_file.close()
        return stalkees_list


@post('/new_stalkee/<origin>')
def new_stalkee(origin):
    website = request.forms.get('stalkee_website')
    message = ""
    r = requests.post("http://" + website + "/social/request_follow", data={'origin': origin, 'message': message})
    print(r.status_code, r.text)

    follow_requests_file = open(page_path + '/data/stalkees.txt')
    follow_requests = ast.literal_eval(follow_requests_file.read())
    follow_requests[website] = {'message': message, 'status': 'pending'}
    follow_requests_file.close()
    follow_requests_file = open(page_path + '/data/stalkees.txt', 'w')
    follow_requests_file.write(str(follow_requests))
    follow_requests_file.close()
    return redirect("/social/")

@route('/confirm_request/<origin>')
def confirm_request(origin):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

    stalkers_file = open(page_path + '/data/stalkees.txt')
    stalkers = ast.literal_eval(stalkers_file.read())
    stalkers[origin]['status'] = 'confirmed'
    stalkers_file.close()
    stalkers_file = open(page_path + '/data/stalkees.txt', 'w')
    stalkers_file.write(str(stalkers))
    stalkers_file.close()


@post('/request_follow')
def request_follow():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

    message = ""
    origin = request.forms.get('origin')

    stalkees_file = open(page_path + '/data/stalkers.txt')
    stalkees = ast.literal_eval(stalkees_file.read())
    stalkees[origin] = {'message': message, 'status': 'pending'}
    stalkees_file.close()
    stalkees_file = open(page_path + '/data/stalkers.txt', 'w')
    stalkees_file.write(str(stalkees))
    stalkees_file.close()
    return "done"


@post('/new_post')
def new_post():
    text = request.forms.get('new_post_text')
    img = request.files.get('new_post_img')
    timestamp = str(int(time.time()))
    os.mkdir(page_path + '/data/posts/' + timestamp)
    log = open(page_path + "/data/posts/" + timestamp + "/log.txt", "w")
    log.close()
    text_file = open(page_path + '/data/posts/' + timestamp + "/text.txt", "w")
    text_file.write(text)
    text_file.close()
    print(text, img)
    if img:
        request.files.get('new_post_img').save(page_path + '/data/posts/' + timestamp + '/img.png')
    return redirect("/social/")


@route('/stalkers')
def stalkers_list():
    if not os.path.isfile(page_path + '/data/stalkers.txt'):
        stalkers_file = open(page_path + '/data/stalkers.txt', 'w')
        stalkers_file.write(str({}))
        stalkers_file.close()
        return {}
    else:
        stalkers_file = open(page_path + '/data/stalkers.txt')
        stalkers_list = ast.literal_eval(stalkers_file.read())
        stalkers_file.close()
        return stalkers_list


@route('/get_img/<timestamp>')
def get_img(timestamp):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    return static_file('img.png', page_path + '/data/posts/' + timestamp)


@route('/get_text/<timestamp>')
def get_text(timestamp):
    log_access(timestamp, request)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    return open(page_path + '/data/posts/' + timestamp + "/text.txt").read()


@route('/delete_post/<timestamp>')
def delete_post(timestamp):
    shutil.rmtree(page_path + '/data/posts/' + timestamp)
    return redirect("/social/")


@route('/delete_stalker/<address>')
def delete_stalker(address):
    stalkers_file = open(page_path + '/data/stalkers.txt')
    stalkers = ast.literal_eval(stalkers_file.read())
    stalkers.pop(address, None)
    stalkers_file.close()
    stalkers_file = open(page_path + '/data/stalkers.txt', 'w')
    stalkers_file.write(str(stalkers))
    stalkers_file.close()
    return redirect("/social/")


@route('/confirm_stalker/<address>')
def confirm_stalker(address):
    stalkers_file = open(page_path + '/data/stalkers.txt')
    stalkers = ast.literal_eval(stalkers_file.read())
    stalkers[address]['status'] = 'confirmed'
    r = requests.post('http://' + address + "/social/confirm_request/" + open(root_path + "/ip_address.txt").read())
    stalkers_file.close()
    stalkers_file = open(page_path + '/data/stalkers.txt', 'w')
    stalkers_file.write(str(stalkers))
    stalkers_file.close()
    return redirect("/social/")


def log_access(timestamp, request):
    log = open(page_path + "/data/posts/" + timestamp + "/log.txt", "a")
    ip = request.environ.get('REMOTE_ADDR')
    log.write("Accessed by " + ip + " at " + str(datetime.datetime.now()) + "\n\n")
    log.close()


@route('/delete_stalkee/<address>')
def delete_stalkee(address):
    stalkees_file = open(page_path + '/data/stalkees.txt')
    stalkees = ast.literal_eval(stalkees_file.read())
    stalkees.pop(address, None)
    stalkees_file.close()
    stalkees_file = open(page_path + '/data/stalkees.txt', 'w')
    stalkees_file.write(str(stalkees))
    stalkees_file.close()
    return redirect("/social/")


@route('/log/<timestamp>')
def log(timestamp):
    return open(page_path + '/data/posts/' + timestamp + '/log.txt').read()


@route('/my_posts')
def my_posts():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    print(os.listdir(page_path + '/data/posts'))
    return json.dumps(os.listdir(page_path + '/data/posts'))


run(host='0.0.0.0', port=port, debug=True)