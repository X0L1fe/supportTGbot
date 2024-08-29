import telebot
import logging
import sqlite3

from telebot import types

TOKEN = '7114623875:AAExJMAuoMl1vSFMSt0OfntoM9-JzDRq0M4'

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(TOKEN)

# Удаление вебхука перед использованием getUpdates
bot.remove_webhook()

ADMIN_ID = 843044049
user_chat_ids = {}# Словарь для хранения динамических chat_id пользователей
target_user_chat_id = None # Переменная для хранения chat_id пользователя
current_page = 0  # Хранение текущей страницы

USERS_PER_PAGE = 2  # Количество пользователей на одну страницу

def create_tables():
    conn = sqlite3.connect('DATABASE.db')
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, 
            user_name VARCHAR(100)
        )
        '''
    )
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            problem TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        '''
    )
    conn.commit()
    cur.close()
    conn.close()

def insert_user(user_id, user_name):
    conn = sqlite3.connect('DATABASE.db')
    cur = conn.cursor()
    try:
        cur.execute(
            '''INSERT INTO users (id, user_name) 
               VALUES (?, ?) 
               ON CONFLICT(id) DO NOTHING''',  # Добавляем только если пользователя еще нет
            (user_id, user_name)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
    finally:
        cur.close()
        conn.close()

def insert_problem(user_id, problem):
    conn = sqlite3.connect('DATABASE.db')
    cur = conn.cursor()
    try:
        cur.execute(
            '''INSERT INTO problems (user_id, problem) 
               VALUES (?, ?)''', 
            (user_id, problem)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
    finally:
        cur.close()
        conn.close()

def get_users(offset=0, limit=USERS_PER_PAGE):
    conn = sqlite3.connect('DATABASE.db')
    cur = conn.cursor()
    try:
        cur.execute('SELECT id, user_name FROM users LIMIT ? OFFSET ?', (limit, offset))
        users = cur.fetchall()
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
        users = []
    finally:
        cur.close()
        conn.close()
    return users

def get_total_users():
    conn = sqlite3.connect('DATABASE.db')
    cur = conn.cursor()
    try:
        cur.execute('SELECT COUNT(*) FROM users')
        total_users = cur.fetchone()[0]
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
        total_users = 0
    finally:
        cur.close()
        conn.close()
    return total_users

def get_problems_by_user(user_id):
    conn = sqlite3.connect('DATABASE.db')
    cur = conn.cursor()
    try:
        cur.execute('SELECT problem FROM problems WHERE user_id = ?', (user_id,))
        problems = cur.fetchall()
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
        problems = []
    finally:
        cur.close()
        conn.close()
    return problems

@bot.message_handler(commands=['start'])
def main(message):
    create_tables()
    
    markup = types.InlineKeyboardMarkup()
    support_user = types.InlineKeyboardButton("Част задаваемые вопросы", callback_data='support')  # кнопка поддержки
    markup.row(support_user)
    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name} !\nВы попали в поддержку *название*, работаем с 11:00 до 21:00.\n Опишите свою проблему и отправьте сообщение.', reply_markup=markup)

@bot.message_handler(commands=['users'])
def list_users(message):
    if message.chat.id == ADMIN_ID:
        global current_page
        current_page = 0
        send_user_list(message.chat.id, current_page, new_message=True)

def send_user_list(chat_id, page, message_id=None, new_message=False):
    users = get_users(offset=page*USERS_PER_PAGE)
    total_users = get_total_users()
    markup = types.InlineKeyboardMarkup()
    if users:
        for user in users:
            user_button = types.InlineKeyboardButton(f"{user[1]} ({user[0]})", callback_data=f"user_{user[0]}")
            markup.add(user_button)
        if total_users > USERS_PER_PAGE:
            navigation_buttons = []
            if page > 0:
                navigation_buttons.append(types.InlineKeyboardButton("⬅️", callback_data=f"prev_{page-1}"))
            if (page + 1) * USERS_PER_PAGE < total_users:
                navigation_buttons.append(types.InlineKeyboardButton("➡️", callback_data=f"next_{page+1}"))
            if navigation_buttons:
                markup.row(*navigation_buttons)
        if new_message:
            sent_message = bot.send_message(chat_id, "Выберите пользователя:", reply_markup=markup)
            return sent_message.message_id
        else:
            bot.edit_message_text("Выберите пользователя:", chat_id=chat_id, message_id=message_id, reply_markup=markup)
    else:
        bot.send_message(chat_id, "Пользователи не найдены.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('user_'))
def callback_user(call):
    global target_user_chat_id
    if call.message.chat.id == ADMIN_ID:
        user_id = int(call.data.split('_')[1])
        target_user_chat_id = user_chat_ids.get(user_id)
        if target_user_chat_id:
            problems = get_problems_by_user(user_id)
            problems_list = "\n".join([f"- {problem[0]}" for problem in problems])
            bot.send_message(ADMIN_ID, f"Проблемы пользователя {user_id}:\n{problems_list}")
        else:
            bot.send_message(ADMIN_ID, "Пользователь не найден в активных сессиях.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('prev_') or call.data.startswith('next_'))
def callback_navigation(call):
    global current_page
    if call.message.chat.id == ADMIN_ID:
        if call.data.startswith('prev_'):
            current_page = int(call.data.split('_')[1])
        elif call.data.startswith('next_'):
            current_page = int(call.data.split('_')[1])
        send_user_list(call.message.chat.id, current_page, message_id=call.message.message_id)

@bot.message_handler(content_types=["text"])
def messanger(message):
    global target_user_chat_id

    sender_chat_id = message.chat.id
    text = message.text

    # Если отправитель - администратор
    if sender_chat_id == ADMIN_ID:
        # Если у администратора уже выбран конкретный пользователь, то отправляем сообщение этому пользователю
        if target_user_chat_id is not None:
            bot.send_message(target_user_chat_id, text)
            bot.send_message(ADMIN_ID, "Сообщение успешно отправлено пользователю.")
            # Сбрасываем target_user_chat_id, чтобы не отправлять сообщения другим пользователям
            target_user_chat_id = None
        else:
            bot.send_message(ADMIN_ID, "Выберите пользователя командой /users.")
    else:
        bot.send_message(ADMIN_ID, f"<b>ID</b>: {message.from_user.id}\n<b>Username:</b> {message.from_user.first_name}\n<b>Login:</b> https://t.me/{message.from_user.username}\n<b>Сообщение</b>: {message.text}", parse_mode='HTML')
        
        # Добавляем динамические chat_id в словарь
        if sender_chat_id not in user_chat_ids.values():
            user_chat_ids[message.from_user.id] = sender_chat_id

        # Вставляем пользователя и его проблему в базу данных
        insert_user(message.from_user.id, message.from_user.username)
        insert_problem(message.from_user.id, text)

        # Сохраняем chat_id пользователя, которому администратор хочет отправить сообщение
        if target_user_chat_id is None:
            target_user_chat_id = sender_chat_id
            bot.send_message(ADMIN_ID, "<b>Пользователь выбран.</b>", parse_mode='HTML')


bot.polling(non_stop=True)