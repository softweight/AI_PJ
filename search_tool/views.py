import requests
import time
import xml.etree.ElementTree as ET
import json,string,random

from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.core import serializers
from .models import *
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def api_search(req):
    if req.method == 'POST':
        result = []
        url_search = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term='+ req.POST['value'] +'&reldate=90&datetype=edat&retmax=100&usehistory=y'
        ret_search = requests.get(url_search)
        root = ET.fromstring(ret_search.text)
        for child in root.iter('WebEnv'):
            WebEnv = child.text

        url_fetch = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=Pubmed&retmode=text&rettype=abstract&term='+ req.POST['value'] +'&query_key=1&retstart=0&retmax=1000&WebEnv='+WebEnv
        ret_fetch = requests.get(url_fetch)
        index = ret_fetch.text[0:1000]
        result.append({'data': index})
        return JsonResponse({'result': result})