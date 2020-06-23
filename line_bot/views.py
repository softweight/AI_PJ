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

import base64
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

user_stage = {}

stage0_ask = "Choose service:\n1. NCBI API\n2. NEWS search"
stage1_ask = "What you want search in NCBI Lib ?"
stage2_ask = "What you want search in NEWs img Lib ?"
stage3_ask = "Else want to do ?\n1. NCBL API\n2. News search\n3. exit"

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
            if isinstance(event, MessageEvent):
                ipt_msg =  event.message.text.split('@')
                if ipt_msg[0] == '1':
                    tob64 = event.message.text.encode("UTF-8")
                    e = base64.b64encode(tob64)
                    manstr = e.decode("UTF-8")
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="this is NCBI\n " + "https://ai-project-bot.herokuapp.com/dw"+ manstr))
                elif ipt_msg[0] == '2':
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="this is news " + ipt_msg[0]))
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="this is else " + ipt_msg[0]))
                
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


# line_bot_api.push_message(event.source.user_id,TextSendMessage(text=output))

# url = 'https://ai-project-bot.herokuapp.com/dw'
# r = requests.post(url, data={"value": event.message.text})
# data = r.json()
# for i in data['result']:
#     string = i['data'] + '\n'
#     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=string))