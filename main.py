import telebot
#import sqlite3

bot = telebot.TeleBot('7091156263:AAFH9nMJrb8UOxQ4rFZ7txLpKnk6DsfB8Jw')

@bot.message_handler(commands=['start', 'help'])
def main(message):
    bot.send_message(message.chat.id, f'Приветствую, {message.from_user.first_name}! Вот правила игры: \nКомпьютер загадывает четырехзначное число с неповторяющимися цифрами\nТы пытаешься угадать это число\nПосле каждого хода компьютер пишет, сколько цифр ты угадал, в формате "X кошечек, Y собачек", где X означает количество угаданных цифр, а Y - количество угаданных позиций\nУ тебя есть 10 попыток, чтобы угадать, иначе игра заканчивается')

@bot.message_handler(commands=['start_game'])
def main(message):
    bot.send_message(message.chat.id, f'Начнем! Введи первое число')

@bot.message_handler(commands=['stats'])
def main(message):
    bot.send_message(message.chat.id, f'Статистика: \nВсего сыграно: 5 игр\nЛучший результат: 3 хода')

bot.infinity_polling()