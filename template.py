from random import randint as rand

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
        

game()