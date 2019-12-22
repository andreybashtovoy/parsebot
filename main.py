#
# Телеграм-бот для парсинга оценок по Дискретной Математике
#
# Мой Telegram: @andrey_bashtovoy
# Инста: @andrey_bashtovoy_sd
#

from __future__ import print_function
import pickle
import os.path
import random

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import telebot
import json
import requests

from sys import platform

if (platform != "win32" and 0):
	from systemd import journal

# Данные таблицы для парсинга
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SAMPLE_SPREADSHEET_ID = '1wgjxDcPGbcFnFhToXQApPerdURvo6ureUrCfyvOv_WU'
SAMPLE_RANGE_NAME = 'B2:U'

# Подключение самого бота
bot = telebot.TeleBot('956609068:AAHkOA95qzROv8Vrq56qLKqlp9UPVvMPFgE')
bot.send_message(858295159, "ДОБРОГО РАНКУ")


@bot.message_handler(commands=['start'])
def dm_start(message):
	bot.send_message(message.chat.id, 'Привет! Введи "/dm Фамилия", чтобы узнать свои баллы по ДМ.')


@bot.message_handler(commands=['dm_send_data'])
def dm_send_data(message):
	file = open("names.json", "r").read()
	r = requests.post("http://sdpromotion.zzz.com.ua/sync_names.php", data={'data': file})
	bot.send_message(message.chat.id, str(r.status_code) + ' ' + r.reason)


@bot.message_handler(commands=['dm_get_data'])
def dm_get_data(message=0):
	r = requests.get("http://sdpromotion.zzz.com.ua/names.json")
	if r.status_code == 200:
		open("names.json", "w").write(r.text)

	# file=open("names.json","r").read()
	if (message != 0):
		bot.send_message(message.chat.id, r.reason)
	else:
		print(str(r.reason))


dm_get_data()


@bot.message_handler(commands=['dm'])
def dm_send(message):
	temp = message.text.lower().split(' ')  # Разделяю команду на две части
	if (len(temp) > 1):  # Если вторая часть введена (Фамилия)
		result = get_stats(0, temp[1])
		bot.send_message(message.chat.id, str(result), parse_mode='Markdown', reply_to_message_id=message.message_id)

		file = json.loads(open("names.json", "r").read())  # Считываю все данные о пользователях

		for i in range(len(file)):
			if (file[i][0] == message.from_user.id):
				file[i][1] = temp[1]
				open("names.json", "w").write(json.dumps(file))  # После всех манипуляций перезаписываю данные в файл
				# bot.send_message(message.chat.id, 'Я тебя запомнил!', reply_to_message_id=message.message_id)
				return (1)

		file.append([message.from_user.id, temp[1]])
		open("names.json", "w").write(json.dumps(file))
	else:  # Если только /dm
		file = json.loads(open("names.json", "r").read())
		for i in range(len(file)):
			if (file[i][0] == message.from_user.id):
				result = get_stats(0, file[i][1])
				bot.send_message(message.chat.id, str(result), parse_mode='Markdown',
				                 reply_to_message_id=message.message_id)
				return (1)

		bot.send_message(message.chat.id,
		                 'Введи "/dm Фамилия", чтобы бот тебя запомнил. Далее просто узнавай свои баллы командой "/dm".')


@bot.message_handler(commands=['dm_rating'])
def dm_rating(message):
	'''
		Просто беру строку из get_stats() с параметром mode=1 и вывожу её в чат
	'''
	temp = message.text.lower().split(' ')
	if (len(temp) > 1 and temp[1].isdigit()):
		result = get_stats(1, page=int(temp[1]))
		bot.send_message(message.chat.id, str(result), parse_mode='Markdown', reply_to_message_id=message.message_id)
	else:
		result = get_stats(1)
		bot.send_message(message.chat.id, str(result), parse_mode='Markdown', reply_to_message_id=message.message_id)


@bot.message_handler(commands=['dm_a'])
def dm_rating(message):
	'''
		Просто беру строку из get_stats() с параметром mode=3 и вывожу её в чат
	'''

	result = get_stats(3)
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


@bot.message_handler(commands=['dm_groups'])
def dm_rating(message):
	'''
		Просто беру строку из get_stats() с параметром mode=1 и вывожу её в чат
	'''
	temp = message.text.lower().split(' ')
	if (len(temp) > 1):
		result = get_stats(2)
		bot.send_message(message.chat.id, str(result), parse_mode='Markdown', reply_to_message_id=message.message_id)
	else:
		result = get_stats(2)
		bot.send_message(message.chat.id, str(result), parse_mode='Markdown', reply_to_message_id=message.message_id)


@bot.message_handler(commands=['dm_about'])
def dm_about(message):
	'''
		Инфа о боте
	'''
	bot.send_message(message.chat.id, "Бот для парсинга оценок ДМ из Google Sheets\n\
\n\
*Исходный код* бота на *GitHub* с небольшими объяснениями: [ССЫЛКА](https://github.com/andreybashtovoy/parsebot)\n\
\n\
Поддержи разработчика - подпишись на инстик:  [andrey_bashtovoy_sd](https://www.instagram.com/andrey_bashtovoy_sd/)))0)",
	                 parse_mode='Markdown', reply_to_message_id=message.message_id)


def get_stats(mode, name='', page=1):
	if page <= 0:
		page = 1;
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
		if (mode == 0):  # Если это /dm ...
			for i in range(len(values)):
				if (len(values[i]) and name in values[i][0].lower()):
					total = 0;
					scores = '';

					for n in range(len(values[i][2:])):
						if (values[i][2:][n].isdigit()):
							total = total + int(values[i][2:][n])

							col_id = 0

							if (i > 37 and i < 73):
								col_id = 37
							elif (i > 74):
								col_id = 74

							scores = scores + '*' + values[col_id][n + 2] + '*' + ": " + str(values[i][2:][n]) + "\n"

					return ('_' + values[i][0] + "_\n\n" + scores + "\n*Общий балл*: " + str(total))
		elif (mode == 1):  # Если это /dm_rating
			arr = []
			for i in range(len(values)):
				if (len(values[i]) and i != 0):
					total = 0;

					for n in range(len(values[i][2:])):
						if (values[i][2:][n] != '' and values[i][0] != '' and not ('Група' in values[i][0])):
							# print(values[i][0]+" "+values[i][1:][n])
							try:
								total = total + int(values[i][2:][n])
							except:
								pass
					arr.append([total, values[i][0]])

			arr.sort()
			arr.reverse()

			string = "*Текущий рейтинг потока по ДМ* (Стр. " + str(page) + ")\n"

			place = 0;
			last = 200;

			for i in range(len(arr)):
				if (arr[i][0] < last):
					place = place + 1
				last = arr[i][0]

				if (i < 20 * page and i >= 20 * page - 20):
					string = string + "\n*" + checkio(place) + "*. _" + arr[i][1] + "_: *" + str(arr[i][0]) + "б.*"
			# else:
			#	break
			return (string)
		elif (mode == 2):  # /dm_groups
			arr = []

			gr1 = 0
			gr2 = 0
			gr3 = 0

			for i in range(len(values)):
				if (len(values[i]) and i != 0):
					total = 0;

					for n in range(len(values[i][2:])):
						if (values[i][2:][n] != '' and values[i][0] != '' and not ('Група' in values[i][0])):
							# print(values[i][0]+" "+values[i][1:][n])
							try:
								total = total + int(values[i][2:][n])
							except:
								pass

					if 0 < i < 36:
						gr1 = gr1 + total
					elif 36 < i < 74:
						gr2 = gr2 + total
					else:
						gr3 = gr3 + total
			# arr.append([total,values[i][0]])

			string = "_Рейтинг по группам_\n\n*ОБЩИЕ:*\n_ИК-91_: *" + str(gr1) + "*\n_ИК-92_: *" + str(
				gr2) + "*\n_ИК-93_: *" + str(gr3) + "*\n\n*Средние:*\n_ИК-91_: *" + str(
				gr1 / 34) + "*\n_ИК-92_: *" + str(gr2 / 31) + "*\n_ИК-93_: *" + str(gr3 / 30) + "*"
			return (string)

		elif (mode == 3):  # Если это /dm_a
			arr = []
			for i in range(len(values)):
				if (len(values[i]) and i != 0):
					total = 0;

					for n in range(len(values[i][2:])):
						if (values[i][2:][n] != '' and values[i][0] != '' and not ('Група' in values[i][0])):
							# print(values[i][0]+" "+values[i][1:][n])
							try:
								total = total + int(values[i][2:][n])
							except:
								pass
					arr.append([total, values[i][0]])

			arr.sort()
			arr.reverse()

			string = "*Претенденты на А по ДМ*\n"

			place = 0
			last = 200

			smiles = ['👽',
			          '🍾',
			          '🍺',
			          '🍷',
			          '🥃',
			          '🎲',
			          '🤦‍♂️',
			          '👍',
			          '👑',
			          '😎',
			          '❄️',
			          '⛄️',
			          '☃️',
			          '🎄',
			          '🌲',
			          '🎄']

			for i in range(len(arr)):
				if i < 9:
					string = string + "\n*" + random.choice(smiles) + "*  _" + str(arr[i][1]) + "_: *" + str(arr[i][0]) + "б.*"
			# else:
			#	break
			return (string)

		return ("*ЪУЪ!*")


def checkio(n):
	'''
		Переводит арабские в римские (код не мой)
	'''
	result = ''
	for arabic, roman in zip((1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
	                         'M     CM   D    CD   C    XC  L   XL  X   IX V  IV I'.split()):
		result += n // arabic * roman
		n %= arabic
	# print('({}) {} => {}'.format(roman, n, result))
	return result


try:
	bot.polling()
except Exception as e:
	if (platform != "win32" and 0):
		journal.send("Error: " + e)
