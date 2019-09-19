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

@bot.message_handler(commands=['dm'])
def dm_send(message):
	temp=message.text.lower().split(' ')
	if(len(temp)>1):
		result=get_stats(0,temp[1])
		bot.send_message(message.chat.id, str(result), parse_mode='Markdown')
	else:
		bot.send_message(message.chat.id, 'Введи "/dm Фамилия", чтобы узнать свои баллы по ДМ.')

@bot.message_handler(commands=['dm_rating'])
def dm_rating(message):
	result=get_stats(1,temp[1])



def get_stats(mode,name):
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
		for i in range(len(values)):
			if(len(values[i]) and name in values[i][0].lower()):
				if(mode==0):
					total=0;
					scores='';

					for n in range(len(values[i][1:])):
						if(values[i][1:][n]!=''):
							total=total+int(values[i][1:][n])
							scores=scores+'*'+values[0][n+1]+'*'+": "+str(values[i][1:][n])+"\n"

					return('_'+values[i][0]+"_\n\n"+scores+"\n*Общий балл*: "+str(total))
				elif(mode==1):
					pass
		return("*ЪУЪ!*")



bot.polling()