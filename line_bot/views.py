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
                if event.source.user_id not in user_stage:
                    user_stage[event.source.user_id] = {
                        'stage': -1
                        }

                if user_stage[event.source.user_id]['stage'] == -1:
                    if event.message.text == '1' :
                        user_stage[event.source.user_id] = 1
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="stage--1to1\n"+stage1_ask))
                    elif event.message.text == '2' :
                        user_stage[event.source.user_id] = 2
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="stage--1to2\n"+stage2_ask))
                    else :
                        user_stage[event.source.user_id] = 0
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="stage--1to0\n"+"Hello!\n"+stage0_ask))
                    return HttpResponse()

                elif user_stage[event.source.user_id]['stage'] == 0:
                    if event.message.text == '1' :
                        user_stage[event.source.user_id]['stage'] = 1
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="stage0to1\n"+stage1_ask))
                    elif event.message.text == '2' :
                        user_stage[event.source.user_id]['stage'] = 2
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="stage0to2\n"+stage2_ask))
                    else :
                        user_stage[event.source.user_id]['stage'] = 0
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="stage0to0\n"+"try again!\n"+stage0_ask))
                    return HttpResponse()

                elif user_stage[event.source.user_id]['stage'] == 1:
                    user_stage[event.source.user_id]['stage'] = 3
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="stage1to3\n"+stage3_ask))
                    # line_bot_api.push_message(event.source.user_id,TextSendMessage(text=stage3_ask))
                    return HttpResponse()

                elif user_stage[event.source.user_id]['stage'] == 2:
                    user_stage[event.source.user_id]['stage'] = 3
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="stage2to3\n" + stage3_ask))
                    # line_bot_api.push_message(event.source.user_id,TextSendMessage(text=stage3_ask))
                    return HttpResponse()

                elif user_stage[event.source.user_id]['stage'] == 3:
                    if event.message.text == '1' :
                        user_stage[event.source.user_id]['stage'] = 1
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="stage3to1\n" +stage1_ask))
                    elif event.message.text == '2' :
                        user_stage[event.source.user_id]['stage'] = 2
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="stage3to2\n" +stage2_ask))
                    elif event.message.text == '3' :
                        user_stage[event.source.user_id]['stage'] = -1
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="bye~"))
                    else :
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="stage3to3\n" +"Unvaildable\n"+ stage3_ask))
                    return HttpResponse()

                # else:    # 不在user stage裡 stage=-1
                #     if event.message.text == '1' :
                #         user_stage[event.source.user_id] = {
                #         'stage': 1,
                #         'time': time.time()
                #         }
                #         line_bot_api.reply_message(event.reply_token, TextSendMessage(text="stage-1to1\n"+stage1_ask))
                #     elif event.message.text == '2' :
                #         user_stage[event.source.user_id] = {
                #         'stage': 2,
                #         'time': time.time()
                #         }
                #         line_bot_api.reply_message(event.reply_token, TextSendMessage(text="stage-1to2\n"+stage2_ask))
                #     else :
                #         user_stage[event.source.user_id] = {
                #         'stage': 0,
                #         'time': time.time()
                #         }
                #         line_bot_api.reply_message(event.reply_token, TextSendMessage(text="stage-1to0\n"+"Hello!\n"+stage0_ask))
                
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


# line_bot_api.push_message(event.source.user_id,TextSendMessage(text=output))

# url = 'https://ai-project-bot.herokuapp.com/api/search'
#             r = requests.post(url, data={"value": event.message.text})
#             data = r.json()
#             for i in data['result']:
#                 string = i['data'] + '\n'
#                 line_bot_api.reply_message(event.reply_token, TextSendMessage(text=string))



### sample here

# @csrf_exempt
# def callback(request):

#     if request.method == 'POST':
#         signature = request.META['HTTP_X_LINE_SIGNATURE']
#         body = request.body.decode('utf-8')

#         try:
#             events = parser.parse(body, signature)
#         except InvalidSignatureError:
#             return HttpResponseForbidden()
#         except LineBotApiError:
#             return HttpResponseBadRequest()
#         for event in events:  # 每個訊息進來時
#             if isinstance(event, MessageEvent):
#                 if event.source.user_id in user_stage:
#                     if time.time()-user_stage[event.source.user_id]['time'] <= 86400:
#                         if user_stage[event.source.user_id]['stage'] == 1:
#                             try:
#                                 idx = int(event.message.text)-1
#                                 data = user_stage[event.source.user_id]['data']['result'][idx]['data']
#                                 columns = []
#                                 for i in range(len(data)):
#                                     if i >= 3: break
#                                     title = str(data[i]['title'])
#                                     if len(title)>20:title = title[0:20]
#                                     columns.append(CarouselColumn(thumbnail_image_url=data[i]['image_url'], title=title, text='$'+str(
#                                         data[i]['price']), actions=[URITemplateAction(label='前往購買', uri=data[i]['url'])]))
#                                 line_bot_api.push_message(
#                                     event.source.user_id,
#                                     TemplateSendMessage(
#                                         alt_text="???", template=CarouselTemplate(columns=columns))
#                                 )
#                             except:
#                                 user_stage[event.source.user_id]['stage'] = 0
#                             return HttpResponse()
#                 user_stage[event.source.user_id] = {
#                     'stage': 1,
#                     'time': time.time()
#                 }
#                 url = 'http://localhost:8000/api/search'
#                 output = ""
#                 r = requests.post(url, data={"value": event.message.text})
#                 data = r.json()
#                 user_stage[event.source.user_id]['data'] = data
#                 if len(data['result']) != 0:
#                     count = 1
#                     for i in data['result']:
#                         string = str(count) + " :" + i['model'] + '\n'
#                         if (len(output)+len(string) < 500):
#                             output += string
#                         else:
#                             line_bot_api.push_message(
#                                 event.source.user_id,
#                                 TextSendMessage(text=output)
#                             )
#                             output = string
#                         count = count + 1
#                     line_bot_api.push_message(
#                         event.source.user_id,
#                         TextSendMessage(text=output)
#                     )
#         return HttpResponse()
#     else:
#         return HttpResponseBadRequest()