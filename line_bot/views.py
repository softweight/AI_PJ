import requests
import time
import xml.etree.ElementTree as ET
from .models import *
from django.db import connection
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
user_stage = {}

@csrf_exempt
def api_search(req):
    if req.method == 'POST':
        result = []
        url_search = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term='+ req.POST['value'] +'&reldate=90&datetype=edat&retmax=100&usehistory=y'
        root = ET.fromstring(requests.get(url_search))
        for child in root.iter('WebEnv'):
            WebEnv = child.text

        url_fetch = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=Pubmed&retmode=text&rettype=abstract&term='+ req.POST['value'] +'&query_key=1&retstart=0&retmax=1000&WebEnv='+WebEnv
        ret_fetch = requests.get(url_fetch)

        result.append({'data': ret_fetch.text[0:200]})
        return JsonResponse({'result': result})


@csrf_exempt
def callback(request):

    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:    #每個訊息進來時
            url = 'http://localhost:8000/api/search'
            r = requests.post(url, data={"value": event.message.text})
            data = r.json()
            for i in data['result']:
                string = i['data'] + '\n'
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=string))

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
