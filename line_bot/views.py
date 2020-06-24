import requests
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
# from static.bitly_api import Connection, BitlyError, Error
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

user_stage = {}


hostname = 'https://1ef81fc4baf5.ngrok.io'

# def shortLink (link):
#     BITLY_ACCESS_TOKEN ="770e7c4e4e6b98de8655716a588b5d36301ef27a"
#     b = Connection(access_token = BITLY_ACCESS_TOKEN)
#     response = b.shorten(link)
#     return response['url']


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

        for event in events:  # 每個訊息進來時
            if isinstance(event, MessageEvent):
                ipt_msg = event.message.text.split('@')
                if ipt_msg[0] == '1':
                    try:
                        url = 'http://127.0.0.1:8000/search/?b='+ipt_msg[1]
                        print(ipt_msg[1])
                        output = ""
                        r = requests.get(url)
                        data = r.json()
                        output = data['result']
                        tob64 = output.encode("UTF-8")
                        e = base64.b64encode(tob64)
                        manstr = e.decode("UTF-8")
                        # print(manstr)
                        dw_path = hostname+'/dw/?@='+manstr
                        buttons_template = TemplateSendMessage(
                            alt_text='Buttons Template',
                            template=ButtonsTemplate(
                                title=' ',
                                text=' ',
                                thumbnail_image_url='https://i2.read01.com/SIG=2jnq5ks/3049625466664f534234.jpg',
                                actions=[
                                    # MessageTemplateAction(
                                    #     label='ButtonsTemplate',
                                    #     text='ButtonsTemplate'
                                    # ),
                                    URITemplateAction(
                                        label='下載',
                                        uri=dw_path
                                    )
                                    # ,
                                    # PostbackTemplateAction(
                                    #     label='postback',
                                    #     text='postback text',
                                    #     data='postback1'
                                    # )
                                ]
                            )
                        )
                        line_bot_api.reply_message(
                            event.reply_token, buttons_template)
                        # line_bot_api.reply_message(
                        #     event.reply_token, TextSendMessage(text=hostname+'/dw/?@='+manstr))
                    except Exception as e:
                        print(e)

                elif ipt_msg[0] == '2':
                    try:
                        url = 'http://127.0.0.1:8000/news/?a='+ipt_msg[1]
                        output = ""
                        r = requests.get(url)
                        data = r.json()
                        output = data['result']
                        columns = []
                        if len(output) == 0:
                            line_bot_api.reply_message(
                                event.reply_token, TextSendMessage(text="查無資料"))
                        else:
                            for i in range(len(output)):
                                img_path = output[i]['url']
                                try:
                                    nl_response = requests.get(img_path)   
                                except requests.exceptions.MissingSchema :
                                    continue
                                columns.append(
                                    CarouselColumn(
                                        thumbnail_image_url=output[i]['url'],
                                        title=output[i]['title'],
                                        text='來源:Udn',
                                        actions=[
                                            # PostbackTemplateAction(
                                            #     label='postback1',
                                            #     text='postback text1',
                                            #     data='action=buy&itemid=1'
                                            # ),
                                            # MessageTemplateAction(
                                            #     label='message1',
                                            #     text='message text1'
                                            # )
                                            # ,
                                            URITemplateAction(
                                                label='點我看大圖',
                                                uri=img_path
                                            )
                                        ]
                                    ))

                            line_bot_api.reply_message(
                                event.reply_token,
                                TemplateSendMessage(
                                    alt_text="???", template=CarouselTemplate(columns=columns))
                            )
                    except Exception as e:
                        print(e)

                    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text="this is news " + ipt_msg[0]))
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(
                        text="請輸入1@XXX 或是 2@XXX"))

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
