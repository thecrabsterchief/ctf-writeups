# from Crypto.Util.number import *
import string
import secrets
from hashlib import sha256
from random import randint, shuffle, choice

def proof_of_work():
    s = ''.join([secrets.choice(string.digits + string.ascii_letters)
                for _ in range(20)])
    print(f'sha256(XXXX+{s[4:]}) == {sha256(s.encode()).hexdigest()}')
    if input('Give me XXXX: ') != s[:4]:
        exit(1)

ROUND_NUM = 50
PREROUND_NUM = 14
CHEST_NUM = 6

with open('flag', 'r') as f:
    flag = f.read()

white_list = ['==','(',')','0','1','and','or','B0','B1','B2','B3','B4','B5']

def calc(ans, chests, expr):
    B0, B1, B2, B3, B4, B5 = chests
    return ans(eval(expr))

def round():
    chests = [choice((True, False)) for _ in range(CHEST_NUM)]
    print("Six chests lie here, with mimics or treasure hidden inside.")
    print("But don't worry. Skeleton Merchant knows what to do.")
    print("Be careful, Skeleton Merchant can lie twice!")

    truth = lambda r: not not r
    lie = lambda r: not r
    lie_num = randint(0, 2)
    lie_status = [truth] * (PREROUND_NUM - lie_num) + [lie] * lie_num
    shuffle(lie_status)

    for i in range(PREROUND_NUM):
        try:
            question = input('Question: ').strip()
            for word in question.split(' '):
                assert word in white_list, f"({word}) No treasure for dirty hacker!"
            result = calc(lie_status[i], chests, question)
            print(f'Answer: {result}!')
        except Exception as e:
            print("Skeleton Merchant fails to understand your words.")
            print(e)
    print('Now open the chests:')
    return chests == list(map(int, input().strip().split(' ')))


if __name__ == '__main__':

    proof_of_work()

    print('Terraria is a land of adventure! A land of mystery!')
    print('Can you get all the treasure without losing your head?')

    for i in range(ROUND_NUM):
        if not round():
            print('A chest suddenly comes alive and BITE YOUR HEAD OFF.')
            exit(0)
        else:
            print('You take all the treasure safe and sound. Head to the next vault!')

    print(f"You've found all the treasure! {flag}")
