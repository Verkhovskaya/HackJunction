import sys
import os
from bottle import route, run, request, post, response, static_file
import ast
import requests
import time
import json
import shutil

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


@route('/javascript')
def js():
    return static_file('main.js', page_path + '/javascript')


@route('/')
def friends():
    print("HELLO")
    text = open(page_path + '/html/header.html').read().\
            replace("$$meta_header$$", meta_header(request)) + \
        open(page_path + '/html/friends_photos.html').read() +\
        open(page_path + '/html/footer.html').read()
    return text


@route('/stalkees')
def stalkees():
    if not os.path.isfile(page_path + '/data/follow_requests.txt'):
        stalkees_file = open(page_path + '/data/follow_requests.txt', 'w')
        stalkees_file.write(str({}))
        stalkees_file.close()
        return {}
    else:
        stalkees_file = open(page_path + '/data/follow_requests.txt')
        stalkees_list = ast.literal_eval(stalkees_file.read())
        stalkees_file.close()
        return stalkees_list


@post('/new_stalkee')
def new_stalkee():
    website = request.forms.get('stalkee_website')
    message = request.forms.get('stalkee_message')

    r = requests.post(website + "/request_follow", data={'origin': 'hello', 'message': message})
    print(r.status_code, r.text)

    follow_requests_file = open(page_path + '/data/follow_requests.txt')
    follow_requests = ast.literal_eval(follow_requests_file.read())
    follow_requests[website] = {'message': message, 'status': 'pending'}
    follow_requests_file.close()
    follow_requests_file = open(page_path + '/data/follow_requests.txt', 'w')
    follow_requests_file.write(str(follow_requests))
    follow_requests_file.close()
    return friends()


@post('/request_follow')
def request_follow():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

    origin = request.forms.get('origin')
    message = request.forms.get('message')

    stalkers_file = open(page_path + '/data/stalkers.txt')
    stalkers = ast.literal_eval(stalkers_file.read())
    stalkers[origin] = {'message': message, 'status': 'pending'}
    stalkers_file.close()
    stalkers_file = open(page_path + '/data/stalkers.txt', 'w')
    stalkers_file.write(str(stalkers))
    stalkers_file.close()
    return "done"


@post('/new_post')
def new_post():
    text = request.forms.get('new_post_text')
    img = request.forms.get('new_post_img')
    timestamp = str(int(time.time()))
    os.mkdir(page_path + '/data/posts/' + timestamp)
    text_file = open(page_path + '/data/posts/' + timestamp + "/text.txt", "w")
    text_file.write(text)
    text_file.close()
    if img:
        img.save(page_path + '/data/posts/' + timestamp + '/img.png')
    print(text, img)
    return friends()


@route('/stalkers')
def stalkers():
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
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    return open(page_path + '/data/posts/' + timestamp + "/text.txt").read()


@route('/delete_post/<timestamp>')
def delete_post(timestamp):
    shutil.rmtree(page_path + '/data/posts/' + timestamp)
    return friends()


@route('/my_posts')
def my_posts():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    print(os.listdir(page_path + '/data/posts'))
    return json.dumps(os.listdir(page_path + '/data/posts'))


run(host='0.0.0.0', port=port, debug=True)