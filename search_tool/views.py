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

from wsgiref.util import FileWrapper
import mimetypes



def FileDownload(request):
    filename = "hihi.txt"
    content = 'SMD'
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response