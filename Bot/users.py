from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.functions.messages import GetMessagesRequest
from telethon.tl.functions.messages import EditMessageRequest
from telethon.tl.types import ReplyInlineMarkup
from telethon.tl.types import KeyboardButtonRow
from telethon.tl.types import KeyboardButtonCallback
import asyncio, time



async def UsersDashboard(event, sender):
    Keyboard = ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text='⚙️  Set up account  ⚙️', data=b'setup')])])
    dashboard = await event.client(SendMessageRequest(sender.id, 'Hello, user your dashboard to complete you registrations.', reply_markup=Keyboard))
    
    
async def SetUp(event, sender_id, actionEdit, timer, setup_id):
    Keyboard = ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text='✅  Confirm Phone  ✅', data=b'confirm_phone')])])
    if actionEdit == False:
        setup = await event.client(SendMessageRequest(sender_id, f'❕ Plaese send your phone number ( ex : +212xxxxxxxxx )', reply_markup=Keyboard))
    else:
        try:
            setup = await event.client(EditMessageRequest(peer=sender_id, id=setup_id, message=f'❕ Plaese send your phone number ( ex : +212xxxxxxxxx ) {timer} sec', reply_markup=Keyboard))
        except:
            setup = False
    return setup
    
    
async def SetUp_api_id(event, sender_id, actionEdit, timer, setup_id):
    Keyboard = ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text='✅  Confirm Api Id  ✅', data=b'confirm_id')])])
    if actionEdit == False:
        SetUp_api_id = await event.client(SendMessageRequest(sender_id, f'❕ Plaese send your Api id', reply_markup=Keyboard))
    else:
        try:
            SetUp_api_id = await event.client(EditMessageRequest(peer=sender_id, id=setup_id, message=f'❕ Plaese send your Api id {timer} sec', reply_markup=Keyboard))
        except:
            SetUp_api_id = False
    return SetUp_api_id
    
    
async def SetUp_api_hash(event, sender_id, actionEdit, timer, setup_id):
    Keyboard = ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text='✅  Confirm Api Hash  ✅', data=b'confirm_hash')])])
    if actionEdit == False:
        SetUp_api_hash = await event.client(SendMessageRequest(sender_id, f'❕ Plaese send your Api hash', reply_markup=Keyboard))
    else:
        try:
            SetUp_api_hash = await event.client(EditMessageRequest(peer=sender_id, id=setup_id, message=f'❕ Plaese send your Api hash {timer} sec', reply_markup=Keyboard))
        except:
            SetUp_api_hash = False
    return SetUp_api_hash
    
    
async def Spam(event, sender_id):
    CancelKeyboard = ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text='❌  Cancel  ❌', data=b'cancel')])])
    spam_back = await event.client(SendMessageRequest(sender_id, '❕ Plaese send information before confirmation', reply_markup=CancelKeyboard))
    return spam_back
    
   
async def LongResponde(event, sender_id):
    CancelKeyboard = ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text='❌  Cancel  ❌', data=b'cancel')])])
    took_long = await event.client(SendMessageRequest(sender_id, '❕ You took a long time to responde.', reply_markup=CancelKeyboard))
    return took_long
    
    
async def PasswordIncorrect(event, sender_id):
    CancelKeyboard = ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text='❌  Cancel  ❌', data=b'cancel')])])
    Incorrect = await event.client(SendMessageRequest(sender_id, '❕ Password incorrect.', reply_markup=CancelKeyboard))
    return Incorrect
    
    
async def UserAlreadyExist(event, sender_id):
    CancelKeyboard = ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text='❌  Back  ❌', data=b'cancel')])])
    UserExist = await event.client(SendMessageRequest(sender_id, '❕ Phone number already registred', reply_markup=CancelKeyboard))
    return UserExist
    
    
async def LoggedSuccessfully(event, sender_id):
    CancelKeyboard = ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text='✅  Finish  ✅', data=b'cancel')])])
    LoggedIn = await event.client(SendMessageRequest(sender_id, '❕ You have logged in successfully. Now you can test commands outside the bot.', reply_markup=CancelKeyboard))
    return LoggedIn
    
    
async def finish_login(event, sender_id):
    ConfirmKeyboard = ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text='✅  Confirm Code  ✅', data=b'confirm_code')])])
    confirm_login = await event.client(SendMessageRequest(sender_id, '❕ Send the code you have received', reply_markup=ConfirmKeyboard))
    return confirm_login
    
    
async def finish_login_password(event, sender_id):
    ConfirmKeyboard = ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text='✅  Confirm Password  ✅', data=b'confirm_password')])])
    confirm_login_password = await event.client(SendMessageRequest(sender_id, '❕ Two-steps verification is enabled, Send your password', reply_markup=ConfirmKeyboard))
    return confirm_login_password
    
    
async def worker(event, last_id):
    if last_id != None:
        message_list = await event.client(GetMessagesRequest(id=[last_id]))
        for message in message_list.messages:
            Target = message.message
            user_id = message.peer_id.user_id
            
        return Target
    else:
        return False
          
            
async def Timer(event, sender_id, actionEdit, timer, setup_id, range_count, king_def):
    timer = range_count
    for x in range(0, range_count):
        edit = await king_def(event, sender_id, actionEdit, timer, setup_id)
        if edit != False:
            for item in edit.updates:
                setup_id = item.message.id
            timer -= 1
            time.sleep(1)
        else:
            break
    return [timer, setup_id]
    
    
async def fixer(timer):
    if timer <= 0:
        return True
        
        
