import telebot
import sqlite3
from random import randint as rand

bot = telebot.TeleBot('7091156263:AAFH9nMJrb8UOxQ4rFZ7txLpKnk6DsfB8Jw')

def user_input(message):
    if len(message.text) != 4 or not message.text.isdigit():
        bot.reply_to(message, 'Введите четырехзначное число!')
        return False
    
    return message.text

def check_win(user_num, comp_num):
    return user_num == comp_num

def mask(user_num, comp_num):
    res = ''
    for i in range(4):
        if comp_num[i] == user_num[i]:
            res += '🟩'
        elif user_num[i] in comp_num:
            res += '🟨'
        else:
            res += '⬜️'

    return res

@bot.message_handler(commands=['start', 'help'])
def main(message):
    bot.send_message(message.chat.id, f'Приветствую, {message.from_user.first_name}! Вот правила игры: \n\nКомпьютер загадывает четырехзначное число, которое необходимо отгадать.\nПосле каждого хода компьютер отправляет маску числа, в которой зеленым обозначены позиции, которые точно соответствуют загаданному числу, желтым – цифры, которые угаданы без совпадения позиции, а белым – позиции, которые вовсе не угаданы.\nКоличество попыток не ограничено.\n\nУдачи!')
    connect = sqlite3.connect('game_db.db')
    cursor = connect.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS user_result(username VARCHAR(30), result INTEGER)")
    connect.commit()

    #cursor.execute("INSERT INTO user_result(username) VALUES(?);",message.from_user.username)
    #connect.commit()

@bot.message_handler(commands=['start_game'])
def game(message):
    comp_num = str(rand(1000, 9999))
    bot.reply_to(message, 'Введите четырехзначное число')
    trials = 0

    @bot.message_handler(func=lambda m: True)
    def handle_user_input(message):
        nonlocal trials, comp_num
        user_num = user_input(message)

        if not user_num:
            return

        trials += 1

        if check_win(user_num, comp_num):
            msg = '🟩🟩🟩🟩'
            bot.reply_to(message, msg)
            bot.reply_to(message, f'Победа! Затрачено {trials} попыток. Чтобы сыграть еще, введи команду /start_game')
            trials = 0
            comp_num = str(rand(1000, 9999))
        else:
            msg = mask(user_num, comp_num)
            bot.reply_to(message, msg)
            bot.reply_to(message, 'Попробуйте еще раз')


@bot.message_handler(commands=['stats'])
def main(message):
    bot.send_message(message.chat.id, f'Статистика: \nВсего сыграно: 5 игр\nЛучший результат: 3 хода')



bot.infinity_polling()