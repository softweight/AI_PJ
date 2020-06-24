import requests as rq
from bs4 import BeautifulSoup
import io
import time
import sqlite3
import os



connAll = sqlite3.connect('News2.db')

connAll.execute('''CREATE TABLE test
       (ID TEXT PRIMARY KEY    ,
       word TEXT NOT　NULL,
       count INT);''')

files=os.listdir('test')
for fileName in files:
    f=open('test\\'+fileName)
    text=f.read()
    textList=text.split(",")
    textDic={}
    for word in textList:
        if word in textDic:
            textDic[word]+=1
        else:
            textDic[word]=1
    strWord=""
    strCount=""
    for word in textDic:
        strWord=strWord+"~"+word
        strCount=strCount+"~"+str(textDic[word])
    connAll.execute("INSERT INTO test (ID,word,count) \
        VALUES ('"+ fileName +"','"+strWord+"','"+strCount+"')")
    connAll.commit()
    f.close()

#tStart = time.time()#計時開始
