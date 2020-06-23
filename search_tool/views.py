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


# text = "NUKCSIE A1065509"
# b = text.encode("UTF-8")
# e = base64.b64encode(b)
# s1 = e.decode("UTF-8")


def FileDownload(request):
    a = request.GET['@']
    b1 = a.encode("UTF-8")
    d = base64.b64decode(b1)
    s2 = d.decode("UTF-8")
    filename = "hihi.txt"
    content = str(s2)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response