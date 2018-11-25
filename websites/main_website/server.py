import sys
import os
from bottle import route, post, run, request, redirect, static_file
import pexpect
import random
import time

if len(sys.argv) == 1:
    port = 8080
else:
    port = sys.argv[1]

program_path = os.getcwd()
if "/root" in program_path:
    root_path = "/root/main_website"
    page_path = "/root/" + program_path.split("/")[-1]
    file_path = '/root/my_website'
else:
    root_path = program_path
    page_path = program_path
    file_path = '/Users/2017-A/Dropbox/hackathon/HackJunction/websites/my_website'


@route('/')
def hello():
    text = open(root_path + "/html/header.html").read() + \
        open(root_path + '/html/root_page.html').read() +\
        open(root_path + "/html/footer.html").read()
    return text


@route("/img")
def img():
    return static_file("front_page.jpg", root_path + "/data")


@post('/setup_new_page')
def setup_new_page():
    ip_address = request.forms.get('ip_address')
    password = request.forms.get('password')
    print(ip_address, password)
    new_password = ""
    print("ssh root@" + ip_address)
    child = pexpect.spawn("scp -r " + file_path + " root@" + ip_address + ":/root")
    child.logfile = sys.stdout

    i = child.expect(["The authenticity .*", "root@" + ip_address + "'s password.*", "ssh: connect.*"])
    if i == 0:
        print("Accepting authenticity")
        child.sendline('yes')
        child.expect(["root@.*"])
        print("Sending password")
        time.sleep(0.1)
        child.sendline(password)
    elif i == 2:
        return "CONNECTION TO " + ip_address + " REFUSED"
    else:
        print("Sending password (" + password + ")")
        child.sendline(password)
    child.expect(["\bFiles copied", pexpect.EOF])
    print("Files copied")

    child = pexpect.spawn("ssh root@" + ip_address)
    child.logfile = sys.stdout
    child.expect("root@.*")
    child.sendline(password)
    child.expect("root@.*")
    child.sendline("cd my_website")
    child.expect("~/my_website")
    child.sendline("python initial_setup.py " + ip_address)
    child.expect("Done initial setup")
    child.sendline("python reset_server.py")
    child.expect("Done reset server")
    print("DONE")
    return redirect("http://" + ip_address + "/new")


run(host='0.0.0.0', port=port, debug=True)