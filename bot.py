from pyrogram import client , filters
import api
from pyrogram import types
from conf import read_config
data = read_config()
bot = client.Client('bot' , data.api_id , data.api_hash , bot_token=data.token)


cache = {}
persian_number = ['۰','۱','۲','۳','۴','۵','۶','۷','۸','۹']
class step:
    send_pswd = filters.user()
    get_pswd = filters.user()

def clear_step(uid):
    if uid in step.send_pswd:
        step.send_pswd.remove(uid)
    if uid in step.get_pswd:
        step.get_pswd.remove(uid)
@bot.on_message(filters.command('start') &  filters.private)
async def start(cl , message):
    uid = message.chat.id
    clear_step(uid)
    markup = types.ReplyKeyboardMarkup([[types.KeyboardButton('ارسال شماره' , request_contact=True)]])
    txt = '''
سلام ٬ خوش اومدید برای شروع میتونید شماره خودتونو بفرستید.💁‍♂️
    '''
    step.send_pswd.add(uid)
    await bot.send_message(uid , txt , reply_markup=markup)

@bot.on_message(step.send_pswd)
async def send_pswd(cl , message):
    uid = message.chat.id
    if message.contact:
        phone = message.contact.phone_number
    else:
        if message.text.startswith('+'):
            if len(message.text) < 6:
                await bot.send_message(uid , '❌شماره نا معتبر است لطفا با فرمت ```+989010000000``` ارسال کنید')
                await start(bot , message)
            elif message.text[4] in persian_number:
                await bot.send_message(uid , 'لطفا اعداد را انگلیسی تایپ کنید.')
                await start(bot , message)
            else:
                phone = message.text
        else:
            await bot.send_message(uid , '❌شماره نا معتبر است لطفا با فرمت ```+989010000000``` ارسال کنید')
            await start(bot , message)
    cache[uid] = api.getPswd(phone)
    if cache[uid].flood == True:
        await bot.send_message(uid , '❌شماره شما فلود شده لطفا بعدا تلاش کنید.')
        clear_step(uid)
        return 0
        
    else:
        if cache[uid].ok == False:
            await bot.send_message(uid , '❌شماره نا معتبر است لطفا با فرمت ```+989010000000``` ارسال کنید با زدن استارت دوباره تلاش کنید.')
            return 0

    step.send_pswd.remove(uid)
    step.get_pswd.add(uid)
    await bot.send_message(uid , 'حالا لطفا یا کد و یا مسیح ارسال شده تلگرام را اینجا بفرستید.✅')
    


@bot.on_message(step.get_pswd)
async def get_pswd(cl , message):
    uid = message.chat.id
    txt = message.text
    if 'This is your login code:' in txt:
        txt = txt.replace('\n' , '')
        txt = txt.split('This is your login code:')
        txt = txt[1]
        txt = txt.split('Do not give this code to anyone')
        txt = txt[0]
        txt = txt.replace(' ' , '')
        txt = txt.strip()
    api_id , api_hash = cache[uid].auth(txt)
    if api_id == 'error':
        await bot.send_message(uid , 'به نظر میرسد پسوورد اشتباه است. دوباره پسوورد را بفرستید ٬ برای بازگشت به منو اصلی /start را بزنید.')
    else:
        txt = f'''💁‍♂️با موفیت دریافت شد
API ID:
‍‍```{api_id}```
API HASH:
‍‍```{api_hash}```
موفق باشید✅
        '''
        await bot.send_message(uid , txt)
        await start(bot , message)


bot.run()
