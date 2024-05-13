from random import randint as rand
import pandas as pd
def user_input():
    input_number = input('Введите число:')

    if len(input_number)!=4:
        print('Введите четырехзначное число!')
        user_input()
        return
    
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    for digit in input_number:
        if digit not in digits:
            print('Введите число!')
            user_input()
            return
    
    return str(input_number)

def check_win(user_num,comp_num):
    return user_num == comp_num

def mask(user_num,comp_num):
    res = ''
    for i in range(4):
        if comp_num[i] == user_num[i]:
            res += '🟩'
        elif user_num[i] in comp_num:
                res += '🟨'
        else:
            res += '⬜️'

    return res

def game():
    comp_num = str(rand(1000,9999))
    
    while True:
        user_num = user_input()
        if check_win(user_num,comp_num):
            msg = '🟩🟩🟩🟩\nwin win!'
            print(msg)
            return 
        
        msg = mask(user_num,comp_num)
        print(msg)
        



'''
connection = sqlite3.connect('users.db')
	cursor = connection.cursor()
	cursor.execute(f'UPDATE users SET total_score = total_score + ? WHERE username LIKE ?', [current_score, message.chat.username])
'''

results = [('kktshit', 9), ('kktshit', 5), ('kktshit', 6), ('imnotkatt', 9), ('imnotkatt', 5), ('imnotkatt', 4), ('imnotkatt', 4), ('kktshit', 8), ('jewishhgirl', 9), ('jewishhgirl', 3), ('jewishhgirl', 5), ('jewishhgirl', 4), ('jewishhgirl', 9), ('kktshit', 5), ('kktshit', 4), ('kktshit', 8), ('kktshit', 5), ('kktshit', 4), ('kktshit', 4), ('kktshit', 5), ('kktshit', 5)]

def tuples_to_df(tuples):
    df = pd.DataFrame(tuples,columns=['username','score'])
    return df

dataframe = tuples_to_df(results)
print(dataframe)