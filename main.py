from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendMessageRequest, GetMessagesRequest
from telethon.errors import (PhoneCodeExpiredError, PhoneCodeInvalidError, PhoneNumberInvalidError,
						PhoneCodeEmptyError, PhoneNumberUnoccupiedError, SessionPasswordNeededError, ApiIdInvalidError,
						ApiIdPublishedFloodError, AuthRestartError, InputRequestTooLongError, PhoneNumberAppSignupForbiddenError,
						PhoneNumberBannedError, PhoneNumberFloodError, PhoneNumberInvalidError, PhonePasswordFloodError, PhonePasswordProtectedError)
						
import asyncio, json, sys, time


from Bot.owner import OwnerDashboard
from Bot.users import UsersDashboard, SetUp, SetUp_api_id, SetUp_api_hash, worker, Spam, fixer, LongResponde, Timer, finish_login, finish_login_password, PasswordIncorrect, LoggedSuccessfully, UserAlreadyExist
from Bot.helpers import ToJson


# LOAD USERS
users = json.load(open("sessions/usersJson/users.json"))


# BOT
api_id_bot = 1724716
api_hash_bot = "00b2d8f59c12c1b9a4bc63b70b461b2f"
bot = TelegramClient("Bot/bot", api_id_bot, api_hash_bot).start(bot_token="5306342972:AAEwMs0RM1tDGixCVKql7AFWIiArfqs0z6w")

# BOT OWNER
owner_id = 5048738026

# LOOP ALWAYS TRUE
loop = True
LoginBussy = False
LoginBussyWith = None
last_id = None


# INFINITE RUN
while loop == True:
	# BOT LOOP
	@bot.on(events.NewMessage(pattern='/start'))
	async def BotOnStart(event):
		sender = await event.get_sender()
		
		try:
			if event.message.peer_id.user_id == event.message.peer_id.user_id:
				if sender.id == owner_id:
					order = await OwnerDashboard(event, sender)
				else:
					user_dashboard = await UsersDashboard(event, sender)
		except:
			pass
	
	
	# WATCH CALLBACKs
	@bot.on(events.CallbackQuery)
	async def confirms(event):
		global LoginBussy, LoginBussyWith, phone, api_id, api_hash, client
		
		sender = await event.get_sender()
		sender_id = event.query.user_id
		
		# DELETE ACTION
		delete = await event.delete()
		
		if event.data == b'setup':
			if LoginBussy == True:
				bussy = await event.client(SendMessageRequest(sender_id, '❕ Login bussy. try after few minutes.'))
			else:
				LoginBussy = True
				LoginBussyWith = sender_id
				
				RNAGE = 30
				# PHONE - COUNTDOWN
				setup_phone = await SetUp(event, sender_id, False, 0, None)
				returns = await Timer(event, sender_id, True, RNAGE, setup_phone.id, RNAGE, SetUp)
				
				fix = await fixer(returns[0])
				if fix == True:
					LoginBussy = False
					LoginBussyWith = None
					
					# DELETE ACTION > CANCEL
					delete = await event.client.delete_messages(entity=sender_id, message_ids=[returns[1]])
					back = await LongResponde(event, sender_id)

				
		if event.data == b'confirm_phone':
			phone = await worker(event, last_id)
			if phone == False:
				spam = await Spam(event, sender_id)
			else:
				if phone in users:
					back = await UserAlreadyExist(event, sender_id)
				else:
					# API ID	
					setup_api_id = await SetUp_api_id(event, sender_id, False, 0, None)
					returns = await Timer(event, sender_id, True, RNAGE, setup_api_id.id, RNAGE, SetUp_api_id)
					
					fix = await fixer(returns[0])
					if fix == True:
						LoginBussy = False
						LoginBussyWith = None
						
						# DELETE ACTION > CANCEL
						delete = await event.client.delete_messages(entity=sender_id, message_ids=[returns[1]])
						back = await LongResponde(event, sender_id)
				
				
		elif event.data == b'confirm_id':
			api_id = await worker(event, last_id)
			if api_id == False:
				spam = await Spam(event, sender_id)
			else:
				# API ID	
				setup_api_hash = await SetUp_api_hash(event, sender_id, False, 0, None)
				returns = await Timer(event, sender_id, True, RNAGE, setup_api_hash.id, RNAGE, SetUp_api_hash)
				
				fix = await fixer(returns[0])
				if fix == True:
					LoginBussy = False
					LoginBussyWith = None
					
					# DELETE ACTION > CANCEL
					delete = await event.client.delete_messages(entity=sender_id, message_ids=[returns[1]])
					back = await LongResponde(event, sender_id)
					
		elif event.data == b'confirm_hash':
			api_hash = await worker(event, last_id)
			if api_hash == False:
				spam = await Spam(event, sender_id)
			else:
				
				# ADD NEW USER
				users[str(phone)] = {
					"id": "user_"+str(sender_id),
					"phone": str(phone),
					"api_id": api_id, 
					"api_hash": str(api_hash)
				}
				
				
				on_success = await event.client(SendMessageRequest(sender_id, '❕ Great, all information collected. Wait a few seconds...'))
				
				
				client = TelegramClient("sessions/"+phone+".session", api_id, api_hash)
				await client.connect()
				if not await client.is_user_authorized():
					try:
						request = await client.send_code_request(phone)
						
					except ApiIdInvalidError:
						on_except = await event.client(SendMessageRequest(sender_id, '❕ The api_id/api_hash combination is invalid.'))
					except ApiIdPublishedFloodError:
						on_except = await event.client(SendMessageRequest(sender_id, '❕ This API id was published somewhere, you cannot use it now.'))
					except AuthRestartError:
						on_except = await event.client(SendMessageRequest(sender_id, '❕ Restart the authorization process.'))
					except InputRequestTooLongError:
						on_except = await event.client(SendMessageRequest(sender_id, '❕ The input request was too long.'))
					except PhoneNumberAppSignupForbiddenError:
						on_except = await event.client(SendMessageRequest(sender_id, '❕ You cannot sign up using this app.'))
					except PhoneNumberBannedError:
						on_except = await event.client(SendMessageRequest(sender_id, '❕ The used phone number has been banned from Telegram and cannot be used anymore.'))
					except PhoneNumberFloodError:
						on_except = await event.client(SendMessageRequest(sender_id, '❕ You asked for the code too many times.'))
					except PhoneNumberInvalidError:
						on_except = await event.client(SendMessageRequest(sender_id, '❕ The phone number is invalid.'))
					except PhonePasswordFloodError:
						on_except = await event.client(SendMessageRequest(sender_id, '❕ You have tried logging in too many times.'))
					except PhonePasswordProtectedError:
						on_except = await event.client(SendMessageRequest(sender_id, '❕ This phone is password protected.'))
					
					request_code = await finish_login(event, sender_id)
				
				else:
					on_except = await event.client(SendMessageRequest(sender_id, '❕ You are already connected.'))
		elif event.data == b'confirm_code':
			
			message_list_code = await event.client(GetMessagesRequest(id=[last_id]))
			for message in message_list_code.messages:
				CODE = (message.message).replace('-', '')

			try:
				login = await client.sign_in(phone, code=int(CODE))
				LoginBussy = False
				LoginBussyWith = None
				await ToJson(users, "sessions/usersJson/users.json")
				logged_in = await LoggedSuccessfully(event, sender_id)
			except PhoneCodeExpiredError:
				on_except = await event.client(SendMessageRequest(sender_id, '❕ The confirmation code has expired'))
			except PhoneCodeInvalidError:
				on_except = await event.client(SendMessageRequest(sender_id, '❕ The phone code entered was invalid.'))
			except PhoneNumberInvalidError:
				on_except = await event.client(SendMessageRequest(sender_id, '❕ The phone number is invalid.'))
			except PhoneCodeEmptyError:
				on_except = await event.client(SendMessageRequest(sender_id, '❕ The phone code is missing.'))
			except PhoneNumberUnoccupiedError:
				on_except = await event.client(SendMessageRequest(sender_id, '❕ The phone number is not yet being used.'))
			except SessionPasswordNeededError:
				request_password = await finish_login_password(event, sender_id)
				
		elif event.data == b'confirm_password':
			message_list = await event.client(GetMessagesRequest(id=[last_id]))
			for message in message_list.messages:
				PASSWORD = message.message
				
			try:
				login = await client.sign_in(phone, password=PASSWORD)
				LoginBussy = False
				LoginBussyWith = None
				await ToJson(users, "sessions/usersJson/users.json")
				logged_in = await LoggedSuccessfully(event, sender_id)
			except:
				password_incorrect = await PasswordIncorrect(event, sender_id)
				

		elif event.data == b'cancel':
			LoginBussy = False
			LoginBussyWith = None
			user_dashboard = await UsersDashboard(event, sender)


	# RECORED LAST MESSAGE ID
	@bot.on(events.NewMessage)
	async def last_id_(event):
		global last_id
		
		try:
			if LoginBussyWith == event.message.peer_id.user_id:
				last_id = event.message.id
				print (event.message.message, last_id)
		except:
			pass
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	# USERS LOOP
	if len(users) != 0:
		for user in users:
			# ID, HASH, USER
			phone = users[user]["phone"]
			api_id = users[user]["api_id"]
			api_hash = users[user]["api_hash"]
			
			# LOGIN USER
			user = TelegramClient("sessions/"+phone, api_id, api_hash)
			user.start()

			# FUNCTIONS
			@user.on(events.NewMessage(pattern='Hello'))
			async def start(event):
				sender = await event.get_sender()
				me = await event.client.get_me()
	            
				print (event)
				if sender.id == me.id:
					order = await event.edit(f'Hello, this is {me.first_name}')




		# RUN USER IN LOOP
		user.run_until_disconnected()
