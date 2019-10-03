from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import telebot
import json


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1wgjxDcPGbcFnFhToXQApPerdURvo6ureUrCfyvOv_WU'
SAMPLE_RANGE_NAME = 'B2:U'

bot = telebot.TeleBot(open('bot',"r").read())

@bot.message_handler(commands=['start'])
def dm_start(message):
	bot.send_message(message.chat.id, 'Привет! Введи "/dm Фамилия", чтобы узнать свои баллы по ДМ.')

@bot.message_handler(commands=['dm'])
def dm_send(message):
	temp=message.text.lower().split(' ')
	if(len(temp)>1):
		result=get_stats(0,temp[1])
		bot.send_message(message.chat.id, str(result), parse_mode='Markdown')
	else:
		file=json.loads(open("names.json","r").read())
		for i in range(len(file)):
			if(file[i][0]==message.from_user.username):
				result=get_stats(0,file[i][1])
				bot.send_message(message.chat.id, str(result), parse_mode='Markdown')
				return(1)

		bot.send_message(message.chat.id, 'Введи "/dm Фамилия", чтобы узнать свои баллы по ДМ или зарегистрируй свою фамилию командой "/dm_reg Фамилия".')

@bot.message_handler(commands=['dm_rating'])
def dm_rating(message):
	result=get_stats(1)
	bot.send_message(message.chat.id, str(result), parse_mode='Markdown')

@bot.message_handler(commands=['dm_reg'])
def dm_reg(message):
	temp=message.text.lower().split(' ')
	if(len(temp)>1):
		file=json.loads(open("names.json","r").read())

		for i in range(len(file)):
			if(file[i][0]==message.from_user.username):
				file[i][1]=temp[1]
				open("names.json","w").write(json.dumps(file))
				bot.send_message(message.chat.id, 'Я тебя запомнил!')
				return(1)

		file.append([message.from_user.username,temp[1]])
		open("names.json","w").write(json.dumps(file))
		bot.send_message(message.chat.id, 'Я тебя запомнил!')
	else:
		bot.send_message(message.chat.id, 'Введи "/dm_reg Фамилия", чтобы бот запомнил твою фамилию.')



def get_stats(mode,name=''):
	"""Shows basic usage of the Sheets API.
	Prints values from a sample spreadsheet.
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

	if not values:
		print('No data found.')
	else:
		if(mode==0):
			for i in range(len(values)):
				if(len(values[i]) and name in values[i][0].lower()):
						total=0;
						scores='';

						for n in range(len(values[i][1:])):
							if(values[i][1:][n]!=''):
								total=total+int(values[i][1:][n])

								col_id=0

								if(i>37 and i<73):
									col_id=37
								elif(i>74):
									col_id=74

								scores=scores+'*'+values[col_id][n+1]+'*'+": "+str(values[i][1:][n])+"\n"

						return('_'+values[i][0]+"_\n\n"+scores+"\n*Общий балл*: "+str(total))
		elif(mode==1):
			arr=[]
			for i in range(len(values)):
				if(len(values[i]) and i!=0):
					total=0;

					for n in range(len(values[i][1:])):
						if(values[i][1:][n]!='' and values[i][0]!='' and not('Група' in values[i][0])):
							#print(values[i][0]+" "+values[i][1:][n])
							try:
								total=total+int(values[i][1:][n])
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
	result = ''
	for arabic, roman in zip((1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
							 'M     CM   D    CD   C    XC  L   XL  X   IX V  IV I'.split()):
		result += n // arabic * roman
		n %= arabic
		print('({}) {} => {}'.format(roman, n, result))
	return result



bot.polling()