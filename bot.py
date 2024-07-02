import os
import json
import telebot
import asyncio
from telethon import TelegramClient, functions, types, errors
from datetime import datetime
import json
import random
from telethon import TelegramClient, errors, functions, types
import aiohttp
import string
import telebot
from telebot import types

API_ID = '20331403'
API_HASH = '85124e7aef89185e581aa2169f974dcf'
BOT_TOKEN = '7336165609:AAETLxakoyboqjOHh5VAd7FzPvy_GOrObVE'
ADMIN_CHAT_ID = '1534317836'
SESSIONS_DIR = './sessions'

bot = telebot.TeleBot(BOT_TOKEN)

VIP_USERS_FILE = 'vip_users.txt'
BANNED_USERS_FILE = 'banned_users.txt'
ADMINS_FILE = 'admins.txt'
SESSIONS_FILE = './sessions'

def get_session_files():
    session_files = [f for f in os.listdir('.') if f.endswith('.session')]
    return session_files

def load_user_sessions(user_id):
    if not os.path.exists(SESSIONS_FILE):
        return []

    with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data.get(str(user_id), [])

def save_user_sessions(user_id, sessions):
    if os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {}

    data[str(user_id)] = sessions

    with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
if not os.path.exists('sessions'):
    os.makedirs('sessions')

if not os.path.exists('users'):
    with open('users', 'w') as f:
        f.write('')
        
if not os.path.exists(VIP_USERS_FILE):
    with open(VIP_USERS_FILE, 'w') as f:
        f.write('')

if not os.path.exists(BANNED_USERS_FILE):
    with open(BANNED_USERS_FILE, 'w') as f:
        f.write('')

if not os.path.exists(ADMINS_FILE):
    with open(ADMINS_FILE, 'w') as f:
        f.write('')

def is_admin(user_id):
    with open(ADMINS_FILE, 'r') as f:
        admins = f.read().splitlines()
    return str(user_id) in admins

def add_admin(user_id):
    with open(ADMINS_FILE, 'a') as f:
        f.write(str(user_id) + '\n')

def remove_admin(user_id):
    with open(ADMINS_FILE, 'r') as f:
        admins = f.read().splitlines()
    with open(ADMINS_FILE, 'w') as f:
        for admin in admins:
            if admin != str(user_id):
                f.write(admin + '\n')
                
def is_vip(user_id):
    with open(VIP_USERS_FILE, 'r') as f:
        vip_users = f.read().splitlines()
    return str(user_id) in vip_users

def is_banned(user_id):
    with open(BANNED_USERS_FILE, 'r') as f:
        banned_users = f.read().splitlines()
    return str(user_id) in banned_users

def add_vip(user_id):
    with open(VIP_USERS_FILE, 'a') as f:
        f.write(str(user_id) + '\n')

def remove_vip(user_id):
    with open(VIP_USERS_FILE, 'r') as f:
        vip_users = f.read().splitlines()
    with open(VIP_USERS_FILE, 'w') as f:
        for user in vip_users:
            if user != str(user_id):
                f.write(user + '\n')

def add_banned(user_id):
    with open(BANNED_USERS_FILE, 'a') as f:
        f.write(str(user_id) + '\n')

def remove_banned(user_id):
    with open(BANNED_USERS_FILE, 'r') as f:
        banned_users = f.read().splitlines()
    with open(BANNED_USERS_FILE, 'w') as f:
        for user in banned_users:
            if user != str(user_id):
                f.write(user + '\n')
                
if os.path.exists('data.json'):
    with open('data.json', 'r') as file:
        data = json.load(file)
else:
    data = {"usernames": [], "files": []}

def save_data():
    with open('data.json', 'w') as file:
        json.dump(data, file)
if not os.path.exists('sessions'):
    os.makedirs('sessions')

if not os.path.exists('users'):
    with open('users', 'w'):
        pass

main_loop = asyncio.get_event_loop()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_banned(message.chat.id):
        bot.send_message(message.chat.id, "أنت محظور من استخدام هذا البوت 🚫")
        return

    if not is_vip(message.chat.id):
        markup = telebot.types.InlineKeyboardMarkup()
        subscribe_vip = telebot.types.InlineKeyboardButton(text="اشترك VIP", callback_data="subscribe_vip")
        markup.add(subscribe_vip)
        bot.send_message(message.chat.id, "هذا البوت مخصص للمشتركين VIP فقط. اشترك الآن للاستفادة من كافة الميزات.", reply_markup=markup)
        return

    markup = telebot.types.InlineKeyboardMarkup()
    login = telebot.types.InlineKeyboardButton(text="اضافة حساب ➕", callback_data="login")
    accounts = telebot.types.InlineKeyboardButton(text="حساباتك 👤", callback_data="session_files")
    add_user = telebot.types.InlineKeyboardButton(text="قسم الخاصيه 👨‍🔧", callback_data="fahs")
    check_file = telebot.types.InlineKeyboardButton(text="فحص ملف 📂", callback_data="check_file")
    files = telebot.types.InlineKeyboardButton(text="ملفاتي 🗃", callback_data="files")
    wevy = telebot.types.InlineKeyboardButton(text="صيد عشوائي 🔀", callback_data="random_capture")
    dev = telebot.types.InlineKeyboardButton(text="المبرمج بيرو 🌊", url="t.me/bk_zt")
    channel = telebot.types.InlineKeyboardButton(text="قناتنا ⚡", url="t.me/Wevy_Python")
    markup.add(login, accounts)
    markup.add(wevy)
    markup.add(check_file, files)
    markup.add(add_user)
    markup.add(dev, channel)
    bot.send_message(message.chat.id, "مرحبا بك في سورس بيرو لفحص وصيد اليوزرات 🌊\n\n① بوت فحص وصيد يوزرات 👨‍🔧\n② صيد يوزرات خاصيه 🕵️‍♂️\n③ صيد يوزرات حذف 🗑\n④ صيد عشوائي مفحوص ✅\n\n⑤ يتم حجز اليوزر المتاح في قناة 🚀", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "subscribe_vip")
def subscribe_vip(call):
    msg = bot.send_message(call.message.chat.id, "أرسل 40 أسيا إلى الرقم التالي : 07759464628\nثم أرسل الرقم الذي أرسلت منه الرصيد او راسل المطور @K570k")
    bot.register_next_step_handler(msg, process_vip_subscription)

def process_vip_subscription(message):
    user_id = message.chat.id
    sent_number = message.text
    markup = telebot.types.InlineKeyboardMarkup()
    approve_vip = telebot.types.InlineKeyboardButton(text="منح اشتراك VIP", callback_data=f"approve_vip_{user_id}")
    reject_vip = telebot.types.InlineKeyboardButton(text="رفض العملية", callback_data=f"reject_vip_{user_id}")
    markup.add(approve_vip, reject_vip)
    bot.send_message(ADMIN_CHAT_ID, f"طلب جديد لاشتراك VIP:\n\nايدي المستخدم : {user_id}\nالرقم المرسل منه: {sent_number}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_vip_"))
def approve_vip(call):
    user_id = call.data.split("_")[2]
    add_vip(user_id)
    bot.send_message(user_id, "تمت الموافقة على اشتراك VIP الخاص بك. يمكنك الآن استخدام البوت.")
    bot.send_message(call.message.chat.id, f"تم منح اشتراك VIP للمستخدم {user_id}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("reject_vip_"))
def reject_vip(call):
    user_id = call.data.split("_")[2]
    bot.send_message(user_id, "تم رفض طلب اشتراك VIP الخاص بك.")
    bot.send_message(call.message.chat.id, f"تم رفض اشتراك VIP للمستخدم {user_id}")

@bot.callback_query_handler(func=lambda call: call.data == "fahs")
def fahs(call):
    markup = telebot.types.InlineKeyboardMarkup()
    add_user_button = telebot.types.InlineKeyboardButton(text="اضف يوزر خاصيه 👤", callback_data="add_user")
    saved_users_button = telebot.types.InlineKeyboardButton(text="يوزرات الخاصيه 📜", callback_data="show_users")
    check_users_button = telebot.types.InlineKeyboardButton(text="فحص خاصيه 🟢", callback_data="check_users")
    back = telebot.types.InlineKeyboardButton(text="رجـــوع 🔙", callback_data="back")
    markup.add(add_user_button, check_users_button)
    markup.add(saved_users_button)
    markup.add(back)
    bot.edit_message_text("مرحبا بك! في قسم الخاصيه 🌊👨‍🔧\n\n• عندما يصبح يوزر متاح يرسل البوت لك رسالة بوقت اليوزر وعند انتهاء مدة التعليق يحجزه في قناة فوراً 🚀", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "login")
def login(call):
    bot.send_message(call.message.chat.id, "أرسل رقم الحساب الذي تريد اضافته مع رمز الدولة 📞\n\n مثال : +9647759464628")
    bot.register_next_step_handler(call.message, process_phone_number)

def process_phone_number(message):
    phone = message.text
    bot.send_message(message.chat.id, "⏳")
    main_loop.run_until_complete(handle_phone_number(message, phone))

async def handle_phone_number(message, phone):
    client = TelegramClient(f'sessions/{phone}', API_ID, API_HASH)
    await client.connect()
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone)
            bot.send_message(message.chat.id, "تم ارسال كود تحقق الى الحساب .. ارسله لي 💬")
            bot.register_next_step_handler(message, lambda m: main_loop.run_until_complete(handle_code(m, client)))
        except Exception as e:
            bot.send_message(message.chat.id, f"An error occurred: {str(e)}")
    else:
        bot.send_message(message.chat.id, "هذا الرقم مسجل بالفعل ⚠️")
    await client.disconnect()

async def handle_code(message, client):
    code = message.text
    try:
        await client.connect()
        await client.sign_in(code=code)
        if await client.is_user_authorized():
            bot.send_message(message.chat.id, "تم تسجيل الحساب بنجاح ✅")
        else:
            bot.send_message(message.chat.id, "الحساب محمي بالتحقق بخطوتين .. أرسل كلمة المرور لاستكمال عملية تسجيل الدخول 🔐")
            bot.register_next_step_handler(message, lambda m: main_loop.run_until_complete(handle_password(m, client)))
    except errors.SessionPasswordNeededError:
        bot.send_message(message.chat.id, "الحساب محمي بالتحقق بخطوتين .. ارسل كلمة السر 🔐")
        bot.register_next_step_handler(message, lambda m: main_loop.run_until_complete(handle_password(m, client)))
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")
    finally:
        await client.disconnect()

async def handle_password(message, client):
    password = message.text
    try:
        await client.connect()
        await client.sign_in(password=password)
        bot.send_message(message.chat.id, "تم اضافة الحساب بنجاح ✅")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")
    finally:
        await client.disconnect()

@bot.callback_query_handler(func=lambda call: call.data == "add_user")
def add_user(call):
    bot.send_message(call.message.chat.id, "أرسل اليوزر لإضافته إلى قائمة الفحص ⚡")
    bot.register_next_step_handler(call.message, save_user)

def save_user(message):
    username = message.text
    with open('users', 'a') as f:
        f.write(username + '\n')
    bot.send_message(message.chat.id, f"تم إضافة اليوزر إلى قائمة الفحص ✅\n\n• اليوزر : @{username}\n\nعندما يتوفر سأحجزه في القناة 🚀")

@bot.callback_query_handler(func=lambda call: call.data == "show_users")
def show_users(call):
    markup = telebot.types.InlineKeyboardMarkup()
    back_button = telebot.types.InlineKeyboardButton(text="Back 🔙", callback_data="private_section")
    markup.add(back_button)
    with open('users', 'r') as f:
        users = f.readlines()
    if users:
        users_list = "• ".join(users)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"يوزراتك المضافه للفحص 📜\n\n• {users_list}", reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, "لم يتم اضافة اي يوزرات بعد ❌")

@bot.callback_query_handler(func=lambda call: call.data == "check_users")
def check_users(call):
    bot.send_message(call.message.chat.id, "تم بدأ فحص الخاصيه ⏳")
    with open('users', 'r') as f:
        users = f.readlines()
    main_loop.run_until_complete(check_usernames(users))

@bot.callback_query_handler(func=lambda call: call.data == "check_file")
def check_file(call):
    bot.send_message(call.message.chat.id, "ارسل الملف الذي تريد فحص اليوزرات الموجوده بداخله 📂")
    bot.register_next_step_handler(call.message, process_file)

def process_file(message):
    if message.document:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open('downloaded_users.txt', 'wb') as f:
            f.write(downloaded_file)
        
        with open('downloaded_users.txt', 'r') as f:
            users = f.readlines()
        
        main_loop.run_until_complete(check_usernames(users))
    else:
        bot.send_message(message.chat.id, "ادعم ملفات .txt فقط ⚠️.")

async def check_usernames(users):
    async with TelegramClient('anon', API_ID, API_HASH) as client:
        for username in users:
            username = username.strip()
            try:
                result = await client(functions.contacts.ResolveUsernameRequest(username))
                if result.users:
                
                    return False
                    
            except errors.UsernameNotOccupiedError:
                channel_title = f"SouRce WeVy 🌊"
                try:
                    channel = await client(functions.channels.CreateChannelRequest(
                        title=channel_title,
                        about='تم حجز هذه القناة بواسطة سورس بيرو لصيد الخاصيه والفحص لشراء او الاشتراك في السورس ~» @K570k',
                        megagroup=False
                    ))
                    await client(functions.channels.UpdateUsernameRequest(
                        channel=channel.chats[0].id,
                        username=username
                    ))
                    now = datetime.now()
                    current_time = now.strftime("%H:%M")
                    bot.send_message(call.message.chat.id, f"تم صيد يوزر متاح ✅\n\n• اليوزر : @{username} \n• الوقت : {current_time}\n\nوتم حجزه في قناة اضغط على اليوزر لزيارتها 🚀")
                    bot.send_message(ADMIN_CHAT_ID, f"قام مشترك بصيد يوزر عشوائي 🔀\n\n• اليوزر : @{username} \n• وقت الصيد : {current_time}\n\nوتم حجزه في قناة اضغط على اليوزر لزيارتها 🚀")
                except Exception as e:
                    bot.send_message(ADMIN_CHAT_ID, f"Error creating channel for username @{username}: {e}")
            except errors.FloodWaitError as e:
                bot.send_message(ADMIN_CHAT_ID, f"Flood wait error: must wait {e.seconds} seconds.")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                bot.send_message(ADMIN_CHAT_ID, f"Error checking username @{username}: {e}")

@bot.callback_query_handler(func=lambda call: call.data == "random_capture")
def random_capture(call):
    bot.send_message(call.message.chat.id, "تم بدأ الصيد العشوائي 1000 محاولة تخمين ⏳")
    asyncio.run(check_usernames(call))

async def check_usernames(call):
    # الحصول على جميع ملفات الجلسات من الدليل المحدد
    sessions = [f for f in os.listdir(SESSIONS_DIR) if f.endswith('.session')]

    if not sessions:
        print("لم يتم العثور على حسابات مسجله لك ❌.")
        return

    async def check_username_with_session(session_file, username):
        async with TelegramClient(os.path.join(SESSIONS_DIR, session_file), API_ID, API_HASH) as client:
            try:
                result = await client(functions.contacts.ResolveUsernameRequest(username))
                if result.users:
                
                    return False
         
            except errors.UsernameNotOccupiedError:
                # إنشاء قناة جديدة
                channel_title = f"صيد عشوايي »Wevy«"
                try:
                    channel = await client(functions.channels.CreateChannelRequest(
                        title=channel_title,
                        about='تم حجز هذه القناة بواسطة سورس بيرو لصيد الخاصيه والفحص لشراء او الاشتراك في السورس ~» @K570k',
                        megagroup=False
                    ))
                    await client(functions.channels.UpdateUsernameRequest(
                        channel=channel.chats[0].id,
                        username=username
                    ))
                    now = datetime.now()
                    current_time = now.strftime("%H:%M")
                    bot.send_message(ADMIN_CHAT_ID, f"قام مشترك بصيد يوزر عشوائي 🔀\n\n• اليوزر : @{username} \n• الوقت : {current_time}\n\nوتم حجزه في قناة اضغط على اليوزر لزيارتها 🚀")
                    bot.send_message(call.message.chat.id, f"تم صيد يوزر عشوائي ✅\n\n• اليوزر : @{username} \n• الوقت : {current_time}\n\nوتم حجزه في قناة اضغط على اليوزر لزيارتها 🚀")
                    return True
                except Exception as e:
                    bot.send_message(ADMIN_CHAT_ID, f"Error creating channel for username @{username}: {e}")
                    return False
            except errors.FloodWaitError as e:
                bot.send_message(ADMIN_CHAT_ID, f"Flood wait error: must wait {e.seconds} seconds.")
                await asyncio.sleep(e.seconds)
                return False
            except Exception as e:
                bot.send_message(ADMIN_CHAT_ID, f"Error checking username @{username}: {e}")
                return False

    for _ in range(1000):
        random_pattern = random.randint(1, 21)
        random_username = generate_random_username(random_pattern)
        random_session = random.choice(sessions)
        if await check_username_with_session(random_session, random_username):
            break

def generate_random_username(pattern_type):
    letters = string.ascii_letters
    digits = string.digits

    if pattern_type == 1:
        return f"T_{random.choice(digits)}_{random.choice(letters)}"
    elif pattern_type == 2:
        return f"T_{random.choice(letters)}_{random.choice(letters)}"
    elif pattern_type == 3:
        return f"vip{random.choice(digits)}{random.choice(digits)}"
    elif pattern_type == 4:
        return f"vip{random.choice(digits)}{random.choice(digits)}{random.choice(digits)}"
    elif pattern_type == 5:
        return f"{random.choice(letters)*3}{random.choice(digits)}{random.choice(letters)}"
    elif pattern_type == 6:
        return f"{random.choice(letters)}{random.choice(digits)}{random.choice(letters)}{random.choice(digits)}{random.choice(letters)}"
    elif pattern_type == 7:
        return f"{random.choice(letters)*3}{random.choice(digits)}{random.choice(letters)*2}"
    elif pattern_type == 8:
        return f"{random.choice(letters)}{random.choice(digits)}{random.choice(letters)}{random.choice(digits)}{random.choice(letters)*2}"
    elif pattern_type == 9:
        return f"sa{random.choice(digits)*4}"
    elif pattern_type == 10:
        return f"{random.choice(letters)*3}{random.choice(letters)}{random.choice(letters)}"
    elif pattern_type == 11:
        return f"{random.choice(letters)}{random.choice(letters)}{random.choice(letters)*3}"
    elif pattern_type == 12:
        return f"{random.choice(letters)}{random.choice(letters)*3}{random.choice(letters)}"
    elif pattern_type == 13:
        return f"{random.choice(letters)}{random.choice(digits)}_{random.choice(digits)}{random.choice(letters)}"
    elif pattern_type == 14:
        return f"{random.choice(letters)*3}BOT"
    elif pattern_type == 15:
        return f"{random.choice(letters)*2}{random.choice(letters)}BOT"
    elif pattern_type == 16:
        return f"{random.choice(letters)}{random.choice(letters)*2}BOT"
    elif pattern_type == 17:
        return f"{random.choice(letters)}{random.choice(digits)}_{random.choice(digits)*2}"
    elif pattern_type == 18:
        return ''.join(random.choices(string.ascii_lowercase, k=5))
    elif pattern_type == 19:
        return ''.join(random.choices(string.ascii_lowercase, k=6))
    elif pattern_type == 20:
        return ''.join(random.choices(string.ascii_lowercase, k=7))
    elif pattern_type == 21:
        return ''.join(random.choices(string.ascii_lowercase, k=8))

@bot.callback_query_handler(func=lambda call: call.data == "back")
def back_to_main(call):
    send_welcome(call.message)

def load_admins():
    if os.path.exists('admins.txt'):
        with open('admins.txt', 'r') as file:
            admins = file.read().splitlines()
            return [int(admin) for admin in admins]
    return []

admins = load_admins()
ADMIN_CHAT_ID = '1534317836'

@bot.message_handler(commands=['start'])
def admin_panel(message):
    if message.chat.id != int(ADMIN_CHAT_ID) and message.chat.id not in admins:
        return

    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    ban_user = telebot.types.InlineKeyboardButton(text="حظر مستخدم", callback_data="ban_user")
    unban_user = telebot.types.InlineKeyboardButton(text="إلغاء حظر مستخدم", callback_data="unban_user")
    grant_vip = telebot.types.InlineKeyboardButton(text="منح اشتراك VIP", callback_data="grant_vip")
    revoke_vip = telebot.types.InlineKeyboardButton(text="إلغاء اشتراك VIP", callback_data="revoke_vip")
    promote_admin = telebot.types.InlineKeyboardButton(text="رفع ادمن", callback_data="promote_admin")
    demote_admin = telebot.types.InlineKeyboardButton(text="تنزيل ادمن", callback_data="demote_admin")
    markup.add(ban_user, unban_user)
    markup.add(grant_vip, revoke_vip)
    markup.add(promote_admin, demote_admin)
    bot.send_message(message.chat.id, "مرحبا بك في لوحة التحكم الخاصه بسورس بيرو 🌊\n\n• تحكم من الازرار الموجوده بالاسفل ⚡", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "ban_user")
def handle_ban_user(call):
    msg = bot.send_message(call.message.chat.id, "أرسل ايدي المستخدم لحظره من استخدام البوت")
    bot.register_next_step_handler(msg, process_ban_user)

def process_ban_user(message):
    user_id = message.text
    add_banned(user_id)
    bot.send_message(message.chat.id, f"تم حظر المستخدم من البوت 🚫\n\n• ايديه : {user_id}")

@bot.callback_query_handler(func=lambda call: call.data == "unban_user")
def handle_unban_user(call):
    msg = bot.send_message(call.message.chat.id, "أرسل ايدي المستخدم لإلغاء حظره")
    bot.register_next_step_handler(msg, process_unban_user)

def process_unban_user(message):
    user_id = message.text
    remove_banned(user_id)
    bot.send_message(message.chat.id, f"تم إلغاء حظر المستخدم من البوت ✅\n\n• ايديه :{user_id}")

@bot.callback_query_handler(func=lambda call: call.data == "grant_vip")
def handle_grant_vip(call):
    msg = bot.send_message(call.message.chat.id, "أرسل ايدي المستخدم لمنحه اشتراك VIP")
    bot.register_next_step_handler(msg, process_grant_vip)

def process_grant_vip(message):
    user_id = message.text
    add_vip(user_id)
    bot.send_message(message.chat.id, f"تم منح المستخدم اشتراك VIP بنجاح ✅\n\n• ايديه : {user_id}")

@bot.callback_query_handler(func=lambda call: call.data == "revoke_vip")
def handle_revoke_vip(call):
    msg = bot.send_message(call.message.chat.id, "أرسل معرف المستخدم لإلغاء اشتراك VIP")
    bot.register_next_step_handler(msg, process_revoke_vip)

def process_revoke_vip(message):
    user_id = message.text
    remove_vip(user_id)
    bot.send_message(message.chat.id, f"تم إلغاء اشتراك VIP للمستخدم بنجاح \n\n• ايديه : {user_id}")

@bot.callback_query_handler(func=lambda call: call.data == "promote_admin")
def handle_promote_admin(call):
    msg = bot.send_message(call.message.chat.id, "أرسل ايدي المستخدم لرفعه إلى أدمن")
    bot.register_next_step_handler(msg, process_promote_admin)

def process_promote_admin(message):
    user_id = message.text
    add_admin(user_id)
    bot.send_message(message.chat.id, f"تم رفع المستخدم الى ادمن في البوت 👨‍✈️\n\n• ايديه : {user_id}")

@bot.callback_query_handler(func=lambda call: call.data == "demote_admin")
def handle_demote_admin(call):
    msg = bot.send_message(call.message.chat.id, "أرسل ايدي المستخدم لتنزيله إلى من الادمن")
    bot.register_next_step_handler(msg, process_demote_admin)

def process_demote_admin(message):
    user_id = message.text
    remove_admin(user_id)
    bot.send_message(message.chat.id, f"تم تنزيل المستخدم من رتبة ادمن في البوت ⚡\n\n• ايديه : {user_id}")
                
@bot.callback_query_handler(func=lambda call: call.data == "files")
def handle_lnline_button(call):
    markup = telebot.types.InlineKeyboardMarkup()
    for i in range(0, len(data["files"]), 2):
        file_buttons = []
        for j in range(2):
            if i + j < len(data["files"]):
                file_buttons.append(telebot.types.InlineKeyboardButton(
                    text=data["files"][i + j]["filename"], callback_data=f"file_{i + j}"))
        markup.add(*file_buttons)

    bot.send_message(call.message.chat.id, "مرحبا بك عزيزي المستخدم\n• هذه هي ملفاتك في بوت فحص سورس بيرو 🌊\n• اضغط على الزر الخاص بالملف للتحكم به", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("file_"))
def handle_file(call):
    file_index = int(call.data.split('_')[1])
    file_info = data["files"][file_index]

    markup = telebot.types.InlineKeyboardMarkup()
    if file_info["checking"]:
        stop_check_button = telebot.types.InlineKeyboardButton(text="ايقاف الفحص 🔴", callback_data=f"stop_check_{file_index}")
        markup.add(stop_check_button)
    else:
        start_check_button = telebot.types.InlineKeyboardButton(text="تشغيل الفحص 🟢", callback_data=f"start_check_{file_index}")
        markup.add(start_check_button)
    delete_file_button = telebot.types.InlineKeyboardButton(text="حذف الملف 🗑", callback_data=f"delete_file_{file_index}")
    back = telebot.types.InlineKeyboardButton(text="رجـــوع 🔙", callback_data="back")
    markup.add(delete_file_button)
    markup.add(back)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"تحكم في ملف {file_info['filename']} من الزرار الموجوده بالاسفل ↙️", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("start_check_"))
def start_check(call):
    file_index = int(call.data.split('_')[2])
    data["files"][file_index]["checking"] = True
    save_data()
    bot.answer_callback_query(call.id, "تم تشغيل الفحص على الملف 🟢")
    handle_file(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith("stop_check_"))
def stop_check(call):
    file_index = int(call.data.split('_')[2])
    data["files"][file_index]["checking"] = False
    save_data()
    bot.answer_callback_query(call.id, "تم ايقاف الفحص على الملف")
    handle_file(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_file_"))
def delete_file(call):
    file_index = int(call.data.split('_')[2])
    del data["files"][file_index]
    save_data()
    bot.answer_callback_query(call.id, "تم حذف الملف وازالته من الفحص 🗑")
    send_welcome(call.message)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    filename = message.document.file_name

    data["files"].append({"filename": filename, "file_id": message.document.file_id, "checking": True, "user_id": message.chat.id})
    save_data()

    bot.send_message(message.chat.id, f"الملف {filename} يتم فحصه 🚀.")
    send_welcome(message)
    
@bot.callback_query_handler(func=lambda call: call.data == "session_files")
def show_session_files(call):
    session_files = get_session_files()

    if not session_files:
        bot.send_message(call.message.chat.id, "لا يوجد جلسات مسجله في البوت ❌.")
        return

    markup = telebot.types.InlineKeyboardMarkup()
    for session_file in session_files:
        phone_number = session_file.split('.')[0]
        session_button = telebot.types.InlineKeyboardButton(text=phone_number, callback_data=f"session_{session_file}")
        markup.add(session_button)

    back_button = telebot.types.InlineKeyboardButton(text="رجـــوع 🔙", callback_data="back")
    markup.add(back_button)
    bot.edit_message_text("اختر جلسة الرقم الذي تريد التحكم فيه عن طريق الضغط على الزر الخاص بالرقم 🌊", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("session_"))
def manage_session(call):
    session_file = call.data.split("_")[1]

    markup = telebot.types.InlineKeyboardMarkup()
    delete_button = telebot.types.InlineKeyboardButton(text="حذف الرقم", callback_data=f"delete_{session_file}")
    back_button = telebot.types.InlineKeyboardButton(text="رجـــوع 🔙", callback_data="session_files")
    markup.add(delete_button, back_button)
    bot.edit_message_text(f"إدارة الجلسة : {session_file}", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_"))
def delete_session(call):
    session_file = call.data.split("_")[1]

    if os.path.exists(session_file):
        os.remove(session_file)
        bot.send_message(call.message.chat.id, f"تم حذف الرقم وانهاء جلسته من البوت 🗑")
    else:
        bot.send_message(call.message.chat.id, "هذه الجلسة محذوفه بالفعل ⚠️.")

    show_session_files(call)
    
@bot.callback_query_handler(func=lambda call: call.data == "back")
def back(call):
    send_welcome(call.message)
    
if __name__ == "__main__":
    bot.polling()