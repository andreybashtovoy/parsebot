#
# Телеграм-бот для парсинга оценок по Дискретной Математике
#
# Мой Telegram: @andrey_bashtovoy
# Инста: @andrey_bashtovoy_sd
#

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import telebot
import json


# Данные таблицы для парсинга
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SAMPLE_SPREADSHEET_ID = '1wgjxDcPGbcFnFhToXQApPerdURvo6ureUrCfyvOv_WU'
SAMPLE_RANGE_NAME = 'B2:U'


# Подключение самого бота
bot = telebot.TeleBot('956609068:AAHkOA95qzROv8Vrq56qLKqlp9UPVvMPFgE')

@bot.message_handler(commands=['start'])
def dm_start(message):
	bot.send_message(message.chat.id, 'Привет! Введи "/dm Фамилия", чтобы узнать свои баллы по ДМ.')

@bot.message_handler(commands=['dm'])
def dm_send(message):
	temp=message.text.lower().split(' ') # Разделяю команду на две части
	if(len(temp)>1): # Если вторая часть введена (Фамилия)
		result=get_stats(0,temp[1])
		bot.send_message(message.chat.id, str(result), parse_mode='Markdown', reply_to_message_id=message.message_id)

		file=json.loads(open("names.json","r").read()) # Считываю все данные о пользователях
		
		for i in range(len(file)):
			if(file[i][0]==message.from_user.id):
				file[i][1]=temp[1]
				open("names.json","w").write(json.dumps(file)) # После всех манипуляций перезаписываю данные в файл
				#bot.send_message(message.chat.id, 'Я тебя запомнил!', reply_to_message_id=message.message_id)
				return(1)

		file.append([message.from_user.id,temp[1]])
		open("names.json","w").write(json.dumps(file))
	else: # Если только /dm
		file=json.loads(open("names.json","r").read())
		for i in range(len(file)):
			if(file[i][0]==message.from_user.id):
				result=get_stats(0,file[i][1])
				bot.send_message(message.chat.id, str(result), parse_mode='Markdown', reply_to_message_id=message.message_id)
				return(1)

		bot.send_message(message.chat.id, 'Введи "/dm Фамилия", чтобы бот тебя запомнил. Далее просто узнавай свои баллы командой "/dm".')

@bot.message_handler(commands=['dm_rating'])
def dm_rating(message):
	'''
		Просто беру строку из get_stats() с параметром mode=1 и вывожу её в чат
	'''
	result=get_stats(1)
	bot.send_message(message.chat.id, str(result), parse_mode='Markdown', reply_to_message_id=message.message_id)

'''
@bot.message_handler(commands=['dm_reg'])
def dm_reg(message):
	temp=message.text.lower().split(' ')
	if(len(temp)>1):
		file=json.loads(open("names.json","r").read()) # Считываю все данные о пользователях

		for i in range(len(file)):
			if(file[i][0]==message.from_user.id):
				file[i][1]=temp[1]
				open("names.json","w").write(json.dumps(file)) # После всех манипуляций перезаписываю данные в файл
				bot.send_message(message.chat.id, 'Я тебя запомнил!', reply_to_message_id=message.message_id)
				return(1)

		file.append([message.from_user.id,temp[1]])
		open("names.json","w").write(json.dumps(file))
		bot.send_message(message.chat.id, 'Я тебя запомнил!', reply_to_message_id=message.message_id)
	else:
		bot.send_message(message.chat.id, 'Введи "/dm_reg Фамилия", чтобы бот запомнил твою фамилию.', reply_to_message_id=message.message_id)
'''

@bot.message_handler(commands=['dm_about'])
def dm_about(message):
	'''
		Инфа о боте
	'''
	bot.send_message(message.chat.id, "*Discrete Math* - бот для парсинга оценок ДМ из Google Sheets\n\
\n\
*Исходный код* бота на *GitHub* с небольшими объяснениями: [ССЫЛКА](https://github.com/andreybashtovoy/parsebot)\n\
\n\
Поддержи разработчика - подпишись на инстик:  [andrey_bashtovoy_sd](https://www.instagram.com/andrey_bashtovoy_sd/)))0)", parse_mode='Markdown', reply_to_message_id=message.message_id)


def get_stats(mode,name=''):
	"""
		Тут пол функции - это просто скопированный код для парсинга с Google Sheets (Изобретать велосипед смысла не вижу).
		Во второй части функция формирует строку с инфой и возвращает её.
	"""
	creds = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('sheets', 'v4', credentials=creds)

	# Call the Sheets API
	sheet = service.spreadsheets()
	result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
								range=SAMPLE_RANGE_NAME).execute()
	values = result.get('values', [])

	# Дальше сам вывод инфы

	if not values:
		print('No data found.')
	else:
		if(mode==0): #Если это /dm ...
			for i in range(len(values)):
				if(len(values[i]) and name in values[i][0].lower()):
						total=0;
						scores='';

						for n in range(len(values[i][2:])):
							if(values[i][2:][n].isdigit()):
								total=total+int(values[i][2:][n])

								col_id=0

								if(i>37 and i<73):
									col_id=37
								elif(i>74):
									col_id=74

								scores=scores+'*'+values[col_id][n+1]+'*'+": "+str(values[i][2:][n])+"\n"

						return('_'+values[i][0]+"_\n\n"+scores+"\n*Общий балл*: "+str(total))
		elif(mode==1): # Если это /dm_rating
			arr=[]
			for i in range(len(values)):
				if(len(values[i]) and i!=0):
					total=0;

					for n in range(len(values[i][2:])):
						if(values[i][2:][n]!='' and values[i][0]!='' and not('Група' in values[i][0])):
							#print(values[i][0]+" "+values[i][2:][n])
							try:
								total=total+int(values[i][2:][n])
							except:
								pass
					arr.append([total,values[i][0]])

			arr.sort()
			arr.reverse()

			string="*Текущий рейтинг потока по ДМ:*\n"

			place=0;
			last=200;

			for i in range(len(arr)):
				if(i<20):
					if(arr[i][0]<last):
						place=place+1
					last=arr[i][0]
					string=string+"\n*"+checkio(place)+"*. _"+arr[i][1]+"_: *"+str(arr[i][0])+"б.*"
				else:
					break
			return(string)


					
		return("*ЪУЪ!*")


def checkio(n):
	'''
		Переводит арабские в римские (код не мой)
	'''
	result = ''
	for arabic, roman in zip((1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
							 'M     CM   D    CD   C    XC  L   XL  X   IX V  IV I'.split()):
		result += n // arabic * roman
		n %= arabic
		#print('({}) {} => {}'.format(roman, n, result))
	return result



bot.polling()
