import os

print("Executing initial setup")
os.system("apt-get update")
os.system("apt-get -y install python-pip")
os.system("pip install bottle")
os.system("pip install pexpect")
os.system("pip install requests")
os.system("a2enmod proxy")
os.system("a2enmod proxy_http")
os.system("a2enmod proxy_balancer")
os.system("a2enmod lbmethod_byrequests")
os.system("systemctl restart apache2")