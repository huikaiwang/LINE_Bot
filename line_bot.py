from __future__ import unicode_literals
import os
import configparser
import psycopg2
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, FollowEvent
from mysql.connector import Error
from seat_db import search_user, check_reg, check_user, err_test, check_state

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

func = False #功能

@handler.add(FollowEvent)
def handle_follow(event):
	global func
	if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
		user = check_user(event.source.user_id)
		if user:
			state = check_state(event.source.user_id)
			if state == "Root":
				func = True
				reply = "Welcome,Root " + user +"\nInstr table:\n傳座位表給學生: e.g. pass 圖片網址" 
			else:
				reply = "Hello " + user
		else:
			reply = "同學你好，請輸入你在SmartExam上的AccessToken"


		line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(text=reply)
		)


@handler.add(MessageEvent, message=TextMessage)
def echo(event):
	global func
	if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
		state = check_state(event.source.user_id)
		if state == "Root":
			if func:
				text = event.message.text.split(" ")
				if text[0]=="pass":
					image_url = text[1]
					#course_id = text[2]
					stu = search_user()
					for i in stu:	
						to = ''.join(i)
			
						line_bot_api.push_message(
							to,
							ImageSendMessage(original_content_url=image_url,
							preview_image_url=image_url)
						)
						
					reply = "instr executed"
					func = False				
				else:
					reply = "invalid instr"

				line_bot_api.reply_message(
					event.reply_token,
					TextSendMessage(text=reply)
				)				

			else:
				reply = "Instr table:\n傳座位表給學生:\ne.g. pass 圖片網址"
				line_bot_api.reply_message(
					event.reply_token,
					TextSendMessage(text=reply)
				) 
				func = True
		elif state == "Member": 

			line_bot_api.reply_message(
				event.reply_token,
				TextSendMessage(text="尚未開放其他功能")
			)	
		
		else:
			reg = check_reg(event.source.user_id,event.message.text)

			if reg:
				reply = "Register Success!" 
			else:
				reply = "Register Faild, Please try again"

			line_bot_api.reply_message(
				event.reply_token,
				TextSendMessage(text=reply)
			)
		

if __name__ == "__main__":
    app.run()
