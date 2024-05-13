import telebot
import sqlite3
from random import randint as rand
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

bot = telebot.TeleBot("7091156263:AAFH9nMJrb8UOxQ4rFZ7txLpKnk6DsfB8Jw")


def user_input(message):
    if len(message.text) != 4 or not message.text.isdigit():
        bot.reply_to(message, "Введите четырехзначное число!")
        return False

    return message.text


def check_win(user_num, comp_num):
    return user_num == comp_num


def mask(user_num, comp_num):
    res = ""
    for i in range(4):
        if comp_num[i] == user_num[i]:
            res += "🟩"
        elif user_num[i] in comp_num:
            res += "🟨"
        else:
            res += "⬜️"

    return res


def tuples_to_df(tuples):
    df = pd.DataFrame(tuples, columns=["username", "score"])
    return df


def generate_pie_chart(results):
    labels = [result[0] for result in results]
    counts = [result[1] for result in results]
    total_count = sum(counts)
    proportions = [count / total_count for count in counts]
    areas = [prop**0.5 for prop in proportions]

    plt.switch_backend("agg")
    plt.figure(figsize=(8, 8))
    plt.pie(areas, labels=labels, autopct="%1.1f%%")
    plt.axis("equal")
    plt.title("Распределение попыток")

    image_stream = BytesIO()
    plt.savefig(image_stream, format="png")
    image_stream.seek(0)

    return image_stream


@bot.message_handler(commands=["start", "help"])
def main(message):
    bot.send_message(
        message.chat.id,
        f"Приветствую, {message.from_user.first_name}! Вот правила игры: \n\nКомпьютер загадывает четырехзначное число, которое необходимо отгадать.\nПосле каждого хода компьютер отправляет маску числа, в которой зеленым обозначены позиции, которые точно соответствуют загаданному числу, желтым – цифры, которые угаданы без совпадения позиции, а белым – позиции, которые вовсе не угаданы.\nКоличество попыток не ограничено.\n\nУдачи!",
    )
    connect = sqlite3.connect("game_db.db")
    cursor = connect.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS user_result(username VARCHAR(30), result INTEGER);"
    )
    connect.commit()
    connect.close()


@bot.message_handler(commands=["start_game"])
def game(message):
    comp_num = str(rand(1000, 9999))
    bot.reply_to(message, "Введите четырехзначное число")
    trials = 0

    @bot.message_handler(func=lambda m: True)
    def handle_user_input(message):
        nonlocal trials, comp_num
        user_num = user_input(message)

        if not user_num:
            return

        trials += 1

        if check_win(user_num, comp_num):
            msg = "🟩🟩🟩🟩"
            bot.reply_to(message, msg)
            bot.reply_to(
                message,
                f"Победа! Затрачено {trials} попыток. Чтобы сыграть еще, введите команду /start_game. Чтобы посмотреть статистику, введите /stats.",
            )

            connect = sqlite3.connect("game_db.db")
            cursor = connect.cursor()
            cursor.execute(
                "INSERT INTO user_result(username,result) VALUES(?,?);",
                [message.from_user.username, trials],
            )
            connect.commit()
            connect.close()

            trials = 0
            comp_num = str(rand(1000, 9999))

        else:
            msg = mask(user_num, comp_num)
            bot.reply_to(message, msg)
            bot.reply_to(message, "Попробуйте еще раз")


@bot.message_handler(commands=["stats"])
def main(message):
    connect = sqlite3.connect("game_db.db")
    cursor = connect.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM user_result WHERE username = ?",
        (message.from_user.username,),
    )
    count = cursor.fetchone()[0]

    games_played_message = f"Вами сыграно: {count} игр\n\n"

    cursor.execute(
        "SELECT ROUND(AVG(result),2) FROM user_result WHERE username = ?",
        (message.from_user.username,),
    )
    average_trials = count = cursor.fetchone()[0]

    average_trials_stats_message = f"Среднее количество попыток: {average_trials}\n\n"

    cursor.execute(
        "SELECT username, COUNT(result) FROM user_result GROUP BY username ORDER BY 2 DESC"
    )
    all_users_stats = cursor.fetchall()
    all_users_stats_message = "Топ пользователей по количеству игр:\n"

    for user_stat in all_users_stats:
        username, games_played = user_stat
        all_users_stats_message += f"{username} - {str(games_played)}\n"

    cursor.execute(
        "SELECT username, AVG(result) AS avg_trials FROM user_result GROUP BY username ORDER BY avg_trials ASC LIMIT 5"
    )
    top_users_stats = cursor.fetchall()
    top_users_stats_message = "\nТоп пользователей по среднему количеству попыток:\n"
    for user_stat in top_users_stats:
        username, avg_trials = user_stat
        top_users_stats_message += f"{username} - {str(round(avg_trials, 2))}\n"

    cursor.execute(
        "SELECT result, COUNT(result) FROM user_result WHERE username = ? GROUP BY result ORDER BY result",
        (message.from_user.username,),
    )
    user_results = cursor.fetchall()

    bot.send_message(
        message.chat.id,
        games_played_message
        + average_trials_stats_message
        + all_users_stats_message
        + top_users_stats_message,
        parse_mode="Markdown",
    )

    pie_chart_image = generate_pie_chart(user_results)

    bot.send_photo(message.chat.id, pie_chart_image)

    connect.close()


bot.infinity_polling()
