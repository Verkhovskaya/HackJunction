import os
import sys

program_path = os.getcwd()

if "/root" in program_path:
    root_path = "/root/my_website"
else:
    root_path = "/".join(program_path.split("/")[:-2])
ip_address = open(root_path + "/ip_address.txt", "w")
ip_address.write(sys.argv[1])
ip_address.close()

print("Executing initial setup")
"""
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
"""
print("Done initial setup")