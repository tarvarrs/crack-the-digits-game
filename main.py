import telebot
#import sqlite3
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

@bot.message_handler(commands=['start_game'])
def game(message):
    comp_num = str(rand(1000, 9999))
    bot.reply_to(message, 'Введите четырехзначное число')
    
    @bot.message_handler(func=lambda m: True)
    def handle_user_input(message):
        user_num = user_input(message)
        if not user_num:
            return

        if check_win(user_num, comp_num):
            msg = '🟩🟩🟩🟩'
            bot.reply_to(message, msg)
            bot.reply_to(message, 'Победа!')
        else:
            msg = mask(user_num, comp_num)
            bot.reply_to(message, msg)
            bot.reply_to(message, 'Попробуйте еще раз')


@bot.message_handler(commands=['stats'])
def main(message):
    bot.send_message(message.chat.id, f'Статистика: \nВсего сыграно: 5 игр\nЛучший результат: 3 хода')



bot.infinity_polling()