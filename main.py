import telebot
#import sqlite3

bot = telebot.TeleBot('7091156263:AAFH9nMJrb8UOxQ4rFZ7txLpKnk6DsfB8Jw')

@bot.message_handler(commands=['start', 'help'])
def main(message):
    bot.send_message(message.chat.id, f'Приветствую, {message.from_user.first_name}! Вот правила игры: \n\nКомпьютер загадывает четырехзначное число\nТы пытаешься угадать это число\nПосле каждого хода компьютер отправляет маску числа, в которой зеленым обозначены позиции, которые точно соответствуют загаданному числу, желтым – цифры, которые ты угадал без совпадения позиции, а белым – цифры, которые ты вовсе не угадал. Количество попыток не ограничено')

@bot.message_handler(commands=['start_game'])
def main(message):
    bot.send_message(message.chat.id, f'Начнем! Введи первое число')

@bot.message_handler(commands=['stats'])
def main(message):
    bot.send_message(message.chat.id, f'Статистика: \nВсего сыграно: 5 игр\nЛучший результат: 3 хода')

bot.infinity_polling()