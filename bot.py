#NiceCoin Sigma
import telebot
from telebot import types
import pandas as pd  # Import the pandas library



# Rest of your code...

# Handler for the new command to show user data




# Токен вашего бота
TOKEN = ''

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения баланса пользователей
user_balance = {}
# Словарь для хранения количества кликов пользователя
click_count = {}

# Константы для стоимости и бонусов в магазине
BOOSTER_COST = {
    '1.5x': 50,
    '1.7x': 150,
    '2x': 450,
    'VIP': 100
}


# Функция для обновления баланса пользователя
def update_balance(user_id, amount):
    user_balance[user_id] += amount
# Load user data from the CSV file
user_data = pd.read_csv('user_data.csv')

# Handler for the /userdata command
@bot.message_handler(commands=['userdata'])
def show_user_data(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Here is the user data:")
    # Convert DataFrame to a string and send it
    bot.send_message(user_id, user_data.to_string(index=False))
    article = pd.read_csv('user_data.csv', delimiter=';',
                          names=['name', 'age'])
    print(article)
    bot.send_message(article)

def userdata(message):
    show_user_data(message)


# Функция для обработки клика
def handle_click(user_id):
    click_count[user_id] += 1
    update_balance(user_id, 1)

    # Проверяем, если пользователь накопил нужное количество кликов для получения бустера
    for booster, cost in BOOSTER_COST.items():
        if click_count[user_id] >= cost:
            if booster == 'VIP':
                bot.send_message(user_id,
                                 f"Поздравляем! Вы достигли {click_count[user_id]} кликов и можете купить VIP статус!")
            else:
                bot.send_message(user_id,
                                 f"Поздравляем! Вы достигли {click_count[user_id]} кликов и можете купить бустер {booster}!")


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_balance[user_id] = 0
    click_count[user_id] = 0

    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn_userdata = types.KeyboardButton('Userdata')
    btn_click = types.KeyboardButton('Click!')
    btn_balance = types.KeyboardButton('Balance')
    btn_shop = types.KeyboardButton('Catalog')
    markup.add(btn_click, btn_balance, btn_shop, btn_userdata)

    @bot.message_handler(func=lambda message: message.text == 'Click!')
    def click(message):
        user_id = message.chat.id
        handle_click(user_id)

    bot.send_message(user_id, "Добро пожаловать в NiceCoin Clicker!", reply_markup=markup)


# Обработчик кнопки Click!

# Обработчик кнопки Balance
@bot.message_handler(func=lambda message: message.text == 'Balance')
def balance(message):
    user_id = message.chat.id
    bot.send_message(user_id, f"Ваш текущий баланс: {user_balance.get(user_id, 0)}")


# Обработчик кнопки Shop
@bot.message_handler(func=lambda message: message.text == 'Catalog')
def shop(message):
    user_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for booster, cost in BOOSTER_COST.items():
        markup.add(types.KeyboardButton(f'{booster} - {cost} NiceCoin'))
    markup.add(types.KeyboardButton('Назад в меню'))
    bot.send_message(user_id, "Здесь можно посмотреть бустеры:", reply_markup=markup)


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ДОРАБОТАТЬ
def boost(message):
    if user_balance == 50:
        message * 1.5
    if user_balance == 100:
        message * 1.7
    if user_balance == 450:
        message * 2

# Обработчик кнопки "Назад в меню"
@bot.message_handler(func=lambda message: message.text == 'Назад в меню')
def back_to_menu(message):
    start(message)


btn_click = types.KeyboardButton('Back')


# Функция для обработки клика с учетом бустеров
def handle_click(user_id):
    click_count[user_id] += 1
    bonus_multiplier = 1.0  # Изначально устанавливаем коэффициент бонуса как 1.0

    # Проверяем, если пользователь купил какой-либо бустер, обновляем коэффициент бонуса соответственно
    for booster, cost in BOOSTER_COST.items():
        if click_count[user_id] >= cost:
            if booster == 'VIP':
                bonus_multiplier *= 2  # Например, VIP бустер удваивает количество монет за клик
            else:
                # Предположим, что все остальные бустеры увеличивают количество монет на указанный коэффициент
                bonus_multiplier *= float(booster.replace('x', ''))

    # Обновляем баланс пользователя с учетом бонуса
    update_balance(user_id, bonus_multiplier)


# Обработчик покупки бустера через кнопки
@bot.message_handler(func=lambda message: message.text in BOOSTER_COST.keys())
def buy_booster(message):
    user_id = message.chat.id
    selected_booster = message.text.split(' - ')[0]  # Получаем название бустера из текста кнопки
    cost = BOOSTER_COST[selected_booster]

    if user_id in user_balance and user_balance[user_id] >= cost:
        update_balance(user_id, -cost)
        bot.send_message(user_id, f"Вы успешно приобрели бустер {selected_booster} за {cost} NiceCoin!")
    else:
        bot.send_message(user_id, "У вас недостаточно средств для покупки этого бустера.")


# Запускаем бота
bot.polling()
