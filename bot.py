from pyrogram import client , filters
import api

bot = client.Client('bot' , 9864076 , '075c2cba44408ef7d00748b4987d00f2' , bot_token='5465264321:AAE3_O1D1dT6N1u4ZJiBHUMbHt5ulm_ZcB4')
owner = 1
class step:
    send_pswd = filters.user()
    get_pswd = filters.user()

@bot.on_message(filters.command('start') , filters.private())
async def start(cl , message):
    uid = message.chat.id
    step.send_code.remove(uid)
    step.get_pswd.remove(uid)
    txt = '''
سلام ٬ خوش اومدید برای شروع میتونید شماره خودتونو بفرستید.💁‍♂️
    '''
    await bot.send_message(uid , txt)

async def send_pswd(cl , message):
    pass



async def get_pswd(cl , message):
    txt = message.text
    txt = txt.replace('\n' , '')
    txt = txt.split('This is your login code:')
    txt = txt[1]
    txt = txt.split('Do not give this code to anyone')
    txt = txt[0]
    txt = txt.replace(' ' , '')
    txt = txt.strip()
    
