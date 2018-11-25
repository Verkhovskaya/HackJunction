import os

os.system("pkill screen")

pages = os.listdir("/root/my_website/pages")
apache_config = open("/etc/apache2/sites-available/000-default.conf", "w")
apache_config.write("<VirtualHost *:80>\n")
apache_config.write("ProxyPreserveHost On\n")

for i in range(len(pages)):
    page_name = pages[i]
    print(page_name)
    if page_name[0] != ".":
        os.system("screen -d -m python pages/" + page_name + "/server.py " + str(8080+i) + " /root/my_website/pages/" + page_name)
        apache_config.write("<Location /" + page_name + ">\n")
        apache_config.write("ProxyPass \"http://0.0.0.0:" + str(8080+i) + "\"\n")
        apache_config.write("ProxyPassReverse \"http://0.0.0.0:" + str(8080+i) + "\"\n")
        apache_config.write("</Location>\n")

apache_config.write("</VirtualHost>")
apache_config.close()

os.system("systemctl restart apache2")
print("Done reset server")