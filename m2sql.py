# -*- coding: utf-8 -*-
#!/usr/bin/env python

REF_ = ['CREATE','TABLE','SELECT','*','FROM','INSERT','INTO','WHERE','NOT','VALUES','DELETE_', 'UPDATE_']
ERROR_ = ['database file not find error!','connect error!']

def connect(beta):
    import os
    global database, n
    n = beta
    if os.path.lexists(beta) == True:
        with open(beta,"r") as source: 
            database = source.read() + "\n"
        return database
    else: return 'database file not find error!'
    
def update():
    global database, n
    with open(n, "w") as m2sql: m2sql.write(database[0:len(database)-1])
    
def UPDATE_(id, table, row, string):
    global database
    table = str(table)
    row = str(row)
    string = str(string)
    id = str(id)
    old = '[' + table + ':' + row + ':' + id + ']' + str(gets(table, id)[getrows(table).index(row)])
    new = '[' + table + ':' + row + ':' + id + ']' + string
    database = database.replace(old, new)
    update()

def DELETE_(table, id):
    global database
    id = str(id)
    table = str(table)
    for beta in getrows(table)[1:]:
        string = '[' + table + ':' + beta + ':' + id + ']' + str(gets(table, id)[getrows(table).index(beta)])
        delete = '[' + table + ':' + beta + ':' + id + ']' + 'Null'
        database = database.replace(string, delete)
    update()

def getstr(ref, string):
    strlen, referans, beta, getstr = len(string) + 1, [], [], []
    for chr in range(0, strlen):
        if string[chr-1:chr] == ref: referans.append(chr - 1)
        elif (strlen - 1) == chr:
            referans.append(chr)
    for chr in range(0, len(referans)):
        if (chr == 0): beta.append(0)
        elif (chr > 0): beta.append(referans[chr-1]+1)
    for chr in range(len(referans)):
        if string[beta[chr]:referans[chr]] != '':
            getstr.append(string[beta[chr]:referans[chr]].replace(' ',''))
    return getstr
    
def gets(table, id):
    id = str(id)
    item, index, gets = [], [], []
    item.append(id)
    try:
        for row in getrows(table)[1:]: ##iyilestirme <- (0:)
            '''if row == getrows(table)[0]: ##id
                continue'''
            string = "[" + table + ":" + row + ":" + id + "]"
            ls = len(string)
            index.append(database.find(string) + ls)
            for beta in range(index[len(index)-1], len(database)):
                if database[beta:beta+ls] == string:
                    index.insert(len(index), beta)
                    break #iyilestirme <- (continue)
        for beta in range(0, len(index), +2):
            test = database[index[beta]:index[beta+1]]
            item.append(test)
        for type, string in zip(gettype(table), item):
            if (type == 'Int'): gets.append(int(string))
            elif (type == 'Bool'): 
                if (string == '0'): 
                    gets.append(False)
                else:
                    gets.append(True)
            elif (type == 'Float'): 
                gets.append(float(string))
            elif (type == 'id'): 
                gets.append(int(string))           
            else: 
                gets.append(str(string))
        return gets    
    except:
        return 'connect error!'
        pass

def trim(string):
    index = []
    for trim in range(0, len(string), +1):
        if string[trim:trim+1] != ' ': 
            index.append(trim)
            break   
    for trim in range(len(string)-1,-1, -1):
        if string[trim:trim+1] != ' ': 
            index.append(trim+1)
            break
    return string[index[0]:index[1]]
    
def gettables():
    beta = database.find("tablo:info")
    for index in range(beta+len('tablo:info'), len(database), +1):
        if database[index:index+1] == "\n":
            f = index; break
    return getstr('|',database[beta+len('tablo:info')+1:index])

def count(table):
    global database
    try:
        string = table+':'+'count'+'|'
        count = database.find(string) + len(string)
        for ln_ in range(count, count + 16, +1):
            if database[ln_:ln_+1] == '\n':
                break
        return int(database[count:ln_])
    except:
        return 'connect error!'
        pass
        
def getrows(table):
    beta = database.find(table+":sutun") + len(table+":sutun")+1
    for index in range(beta, len(database), +1):
        if database[index:index+1] == "\n":
            f = index; break
    return getstr("|",database[beta:index])
    
def gettype(table):
    beta = database.find(table+":type")+len(table+":type")+1
    for index in range(beta, len(database), +1):
        if database[index:index+1] == "\n":
            f = index; break
    return getstr("|",database[beta:index])
    
def execute(command, *values):
    global database, n, table, x
    import os
    nrow, ntype = [], []
    m2 = []; notif = []
    select = []
    sort = []
    command = command.replace('(', ' ( ').replace(')',' ) ').replace(',',' ')
    command = getstr(' ',command)
    for beta in range(command.index(command[2])+1, len(command), +1):
        if command[beta] != chr(40) or command[beta] != chr(41):
            if command[beta] == chr(40): 
                continue 
            if command[beta] == chr(41): 
                break
            m2.append(command[beta])    
            
    for beta in command:
        if 'NOT' == beta:
            for beta in range(command.index(beta)+1, len(command), +1):
                if command[beta] != chr(40) or command[beta] != chr(41):
                    if command[beta] == chr(40): continue 
                    if command[beta] == chr(41): 
                        break
                    notif.append(command[beta])
            
    if command[0] == 'CREATE' and command[1] == 'TABLE':
        text_nrow = command[2] + ':sutun'
        text_ntype = command[2] + ':type'
        for beta in range(0, len(m2), +2):
            nrow.append(m2[beta])
            ntype.append(m2[beta+1])
        for row, type in zip(nrow, ntype):
            text_nrow = text_nrow + '|' + row
            text_ntype = text_ntype + '|' + type
            tcount = command[2] + ':count' + '|' + '0'
        if os.path.lexists(n) == True:
            string = ''
            if command[2] not in gettables():
                for beta in gettables():
                    string = string + '|' + beta 
                string = 'tablo:info' + string
                if string.find(command[2]) == -1:
                    database = database.replace(string, string + '|' + command[2] + '\n' + text_nrow + '\n' + text_ntype + '\n' + tcount ) 
                    update()
        else:
            database = 'tablo:info' + '|' + command[2] + '\n' + text_ntype + '\n' + text_nrow + '\n' + tcount + '\n'
            update()           
            
    if 'SORT' in command:
        for beta in range(command.index('SORT')+1, len(command), +1):
            if command[beta] != chr(40) or command[beta] != chr(41):
                if command[beta] == chr(40): 
                    continue 
                if command[beta] == chr(41): 
                    break
                sort.append(command[beta])  
        #print sort
            
    if 'NOT' not in command:
        if command[0] == 'INSERT' and command[1] == 'INTO':
            id = str(count(command[2])+1)
            if len(m2) != len(values):
                print 'error', values, m2
            for beta in getrows(command[2]):
                string = '[' + command[2] + ':' + beta + ':' + id + ']'
                if beta ==  getrows(command[2])[0]: ##id
                    database = database + string + '\n'
                    continue
                if beta not in m2:
                    database = database + string + 'Null' + string + '\n'
                else:
                    database = database + string + str(values[m2.index(beta)])  + string + '\n'
            database = database.replace(command[2] + ':' + 'count' + '|' + str(int(id)-1), command[2] + ':' + 'count' + '|' + id)
            #update()      
              
    if 'NOT' in command:
        if_ = []
        search = str(values[m2.index(notif[0])])
        for id in range(1, count(command[2])+1, +1):
            string = '['+ str(command[2]) + ':' + str(notif[0]) + ':' + str(id) + ']' + search + '['
            if database.find(string) != -1: 
                if_.append(1); break 
            else: if_.append(0)
        if (True not in if_):
            id = str(count(command[2])+1)
            if len(m2) != len(values):
                print 'error', values, m2
            for beta in getrows(command[2]):
                string = '[' + command[2] + ':' + beta + ':' + id + ']'
                if beta ==  getrows(command[2])[0]: ##id 
                    database = database + string + '\n'
                    continue
                if beta not in m2:
                    database = database + string + 'Null' + string + '\n'
                else:
                    database = database + string + str(values[m2.index(beta)]) + string + '\n'
            database = database.replace(command[2] + ':' + 'count' + '|' + str(int(id)-1), command[2] + ':' + 'count' + '|' + id)
            #update()   
        #print if_
    if command[0] == 'SELECT' and command[1] == "*" and command[2] == 'FROM':
        table = command[3]
        
        if 'WHERE' in command:
            if len(sort) == 0:
                for id in range(1, count(table)+1, +1):
                    if gets(table, id)[getrows(table).index(command[command.index('WHERE')+1])] == values[0]:
                        select.append(gets(table, id)) 
                        continue
                return select
            if sort[0] == 'ZA':
                for id in range(count(table), 0, -1):
                    if gets(table, id)[getrows(table).index(command[command.index('WHERE')+1])] == values[0]: 
                        select.append(gets(table, id)) 
                        continue
                return select
            if sort[0] == 'AZ':
                for id in range(1, count(table)+1, +1):
                    if gets(table, id)[getrows(table).index(command[command.index('WHERE')+1])] == values[0]: 
                        select.append(gets(table, id)) 
                        continue
                return select
        if 'WHERE' not in command:
            if len(sort) == 0:
                for id in range(1, count(table)+1, +1):
                    select.append(gets(table, id))
                return select
            if sort[0] == 'ZA':
                for id in range(count(table), 0, -1):
                    select.append(gets(table, id))
                return select    
            if sort[0] == 'AZ':
                for id in range(1, count(table)+1, +1):
                    select.append(gets(table, id))
                return select  
                
                
                