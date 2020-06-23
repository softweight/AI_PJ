import requests
import time
import os
import xml.etree.ElementTree as ET
import json
import string
import random

from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, FileResponse
from django.core import serializers
from .models import *
from django.views.decorators.csrf import csrf_exempt

import base64


class sample():
    def __init__(self, title, text, num):
        self.title = title
        self.counter = dict()
        self.match = 0
        self.total = 0
        self.process(text,num)
        # self.printf()

    def process(self, text, num):
        for i, data in enumerate(text):
            self.counter[data] = int(num[i])
    # def printf(self):
    #     print(self.title)
    #     print(self.counter)
    #     return


def search(SampleArr, key):
    for item in SampleArr:
        item.match = 0
        for var in key:
            if var in item.counter.keys():
                item.total += item.counter[var]
                item.match += 1
    return


def sorting(SampleArr):
    now = SampleArr[0].match
    start = 0
    count = 0
    for var in SampleArr:
        if now != var.match or var == SampleArr[-1]:
            if var == SampleArr[-1]:
                count += 1
            temp = list.copy(SampleArr[start:count])
            temp.sort(key=lambda x: x.total)
            SampleArr[start:count] = temp
            start = count
            now = var.match
        count += 1
    return

def findOneWord(query):
    # connAll = sqlite3.connect('News2.db')
    # data = connAll.execute("SELECT * FROM NEWS WHERE title LIKE '%"+query+"%';").fetchall()
    curso=connection.cursor()
    data=curso.execute("SELECT * FROM NEWS WHERE title LIKE '%"+query+"%';").fetchall()
    # data  = News.objects.raw("SELECT * FROM NEWS WHERE title LIKE '%"+query+"%';")
    # connAll.close
    score={}
    for A_data in data:
        news_link=A_data[4]
        #切字
        wordList=A_data[3]+A_data[1]+A_data[2]
        AllCount=int(len(wordList)/2)
        count=len(wordList.split(query))
        score[A_data[0]]=[count/AllCount,news_link,A_data[1]]
    # print(score)
    maxScore=0
    label=""
    pic = ""
    for newsId in score:
        if score[newsId][0]>maxScore:
            maxScore=score[newsId][0]
            label=newsId
            pic = score[newsId][1]
    return score

def merge(listAll):
    result = []
    listItemKey={}
    for item in listAll:
        for key in list(item.keys()):
            if key in listItemKey:
                listItemKey[key][0] += item[key][0]
                listItemKey[key][0] += listItemKey[key][0]*2
            else:
                listItemKey[key] = item[key]
    maxCnt = [0,0,0]
    for key in list(listItemKey.keys()):
        if listItemKey[key][0] > maxCnt[0]:
            maxCnt[2] = maxCnt[1]
            maxCnt[1] = maxCnt[0]
            maxCnt[0] = listItemKey[key][0]
    for key in list(listItemKey.keys()):
        if maxCnt[0] == listItemKey[key][0]:
            dicP = {'title':listItemKey[key][2],'url':listItemKey[key][1]}
            result.append(dicP)
        if maxCnt[1] == listItemKey[key][0]:
            dicP = {'title':listItemKey[key][2],'url':listItemKey[key][1]}
            result.append(dicP)
        if maxCnt[2] == listItemKey[key][0]:
            dicP = {'title':listItemKey[key][2],'url':listItemKey[key][1]}
            result.append(dicP) 
    return result

@csrf_exempt
def news_search(req):
    try:
        inputText = req.GET['a']
        inputList = inputText.split(" ")
        app = []
        for item in inputList:
            app.append(findOneWord(item))
        opt = merge(app)
        return JsonResponse({'result': opt})
    except Exception as e:
        print(e)
        opt = "error"
        # return JsonResponse({'result': opt})


@csrf_exempt
def boolean_search(req):
    SampleList = []
    opt = ""
    try:
        for data in Test.objects.all():
            word = data.word.split('~')[1::]
            count = data.count.split('~')[1::]
            SampleList.append(sample(data.id, word, count))

        getkey = req.GET['b']
        #print(getkey)
        getkey = getkey.split(' ')
        
        search(SampleList, getkey)
        SampleList.sort(key=lambda x: x.match)
        sorting(SampleList)
        SampleList= SampleList[::-1]
        for i, var in enumerate(SampleList):
            if(var.match==0):
                if i==0:
                    opt = 'not found'
                break
            opt = opt+str(var.title)+'\n'
        return JsonResponse({'result': opt})
    except Exception as e:
        print(e)


def FileDownload(request):
    a = request.GET['@']
    b1 = a.encode("UTF-8")
    d = base64.b64decode(b1)
    s2 = d.decode("UTF-8")
    filename = "out.txt"
    content = str(s2)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(
        filename)
    return response
