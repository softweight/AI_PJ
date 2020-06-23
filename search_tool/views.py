import requests
import time,os
import xml.etree.ElementTree as ET
import json,string,random

from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect,FileResponse
from django.core import serializers
from .models import *
from django.views.decorators.csrf import csrf_exempt

import base64

class sample():
    def __init__(self,title,text):
        self.title = title
        self.counter = dict()
        self.match = 0
        self.total = 0
        self.process(text)
        # self.printf()
    def process(self,text):
        text = text.split(',')
        # print(text)
        for var in text:
            if var not in self.counter.keys():
                self.counter[var.lower()] = 1 
                continue
            self.counter[var]+=1
    def printf(self):
        print(self.title)
        print(self.counter)
        return

def search(SampleArr,key):
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
            temp.sort(key= lambda x:x.total)
            SampleArr[start:count] = temp
            start = count 
            now = var.match 
        count += 1
    return 


@csrf_exempt
def boolean_search(req):
    if req.method == 'POST':
        All_file = os.listdir('test')
        SampleList = []
        opt = ""
        for filename in All_file:
            f = open('test/'+filename)
            txt = f.read()
            SampleList.append(sample(filename,txt))
            f.close()
        search(SampleList,req.POST['key'])
        SampleList.sort(key= lambda x:x.match)
        sorting(SampleList)
        for i,var in enumerate(SampleList):
            opt.append(str(var.title)+'\n')
        return JsonResponse({'result': opt})








def FileDownload(request):
    a = request.GET['@']
    b1 = a.encode("UTF-8")
    d = base64.b64decode(b1)
    s2 = d.decode("UTF-8")
    filename = "out.txt"
    content = str(s2)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response