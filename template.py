from random import randint as rand

comp_num = '5216'
steps = 10


def is_correct_input(input_number):
    if not isinstance(input_number, int) or input_number < 1000 or input_number > 9999:
        return False
    
    digits = [int(d) for d in str(input_number)]
    if len(set(digits)) != 4:
        return False
    
    return True
    cats = check_cats(comp_num, user_num)
    dogs = check_dogs(comp_num, user_num)

    return f'{cats} кошечек, {dogs} собачек'

print(is_correct_input(int(input())))
# def check_number():
#     check_cats(comp_num, user_num)
#     check_dogs(comp_num, user_num)
#     return

def check_cats(comp_num, user_num):
    cats = 0
    for i in range(0,4):
        if comp_num[i] == user_num[i]:
            cats+=1

    return cats

def check_dogs(comp_num, user_num):
    dogs = 0
    for i in user_num:
        if i in comp_num:
            dogs += 1
    
    return dogs

