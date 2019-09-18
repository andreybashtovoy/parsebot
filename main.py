from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import telebot


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1wgjxDcPGbcFnFhToXQApPerdURvo6ureUrCfyvOv_WU'
SAMPLE_RANGE_NAME = 'B2:U'

bot = telebot.TeleBot('956609068:AAHkOA95qzROv8Vrq56qLKqlp9UPVvMPFgE')

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


@bot.message_handler(content_types=['text'])
def send_text(message):
	#global mid, TEMP_OBJECT
	#mid=message.chat.id
	#if message.text.lower() == 'привет':
	#	bot.send_message(message.chat.id, 'Привет, мой создатель')
	if('/dm' in message.text.lower()):
		temp=message.text.lower().split(' ')
		if(len(temp)>1):
			result=get_stats(temp[1])
			bot.send_message(message.chat.id, str(result))
		else:
			bot.send_message(message.chat.id, 'Введи "/dm Фамилия", чтобы узнать свои баллы по ДМ.')

def get_stats(name):
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
		for i in values:
			if(len(i) and name in i[0].lower()):
				return(i[0]+": "+' '.join(i[1:]))



bot.polling()