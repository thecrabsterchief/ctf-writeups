#!/usr/bin/env python3
import random
import signal
import sys

MENU_GAMBLE     = 1
MENU_VERIFY     = 2
MENU_FLAG       = 3
MENU_LEAVE      = 4

money = 500
verified = False

def show_menu():
    print('=======================================')
    print('1. go to gamble')
    print('2. verify you\'re a robot')
    print('3. buy flag')
    print('4. leave')

def get_randn():
    return random.randint(0, 0xfffffffe)

def gamble():
    global money
    global verified

    if verified is False:
        print('you\'re are not verified as a robot ;[')
        return

    print('greetings, robot :]')

    bet = int(input('how much money do you want to bet (your money: ${0})? '.format(money)))
    if money < bet:
        print('you don\'t have enough money (your money: ${0}).'.format(money))
        return

    randn = get_randn()
    answer = randn % 5 + 1

    print('[1] [2] [3] [4] [5]')
    user_answer = int(input('pick one of the box > '))

    print('answer is [{0}]!'.format(answer))

    if user_answer == answer:
        print('you earned ${0}.'.format(bet))
        money += bet
    else:
        print('you lost ${0}.'.format(bet))
        money -= bet

    if money <= 0:
        print('you busted ;]')
        sys.exit()

class MyTimeoutError(Exception):
    def __init__(self):
        pass

def timeout_handler(signum, frame):
    raise MyTimeoutError()

def verify():
    global verified

    if verified is True:
        print('you have already been verified as a robot :]')
        return

    randn224 = (get_randn() | get_randn() << 32 | get_randn() << 64 |
                get_randn() << 96 | get_randn() << 128 | get_randn() << 160)

    challenge = randn224 ^ 0xdeaddeadbeefbeefcafecafe13371337DEFACED0DEFACED0

    signal.alarm(3)
    signal.signal(signal.SIGALRM, timeout_handler)

    try:
        print('please type this same: "{0}"'.format(challenge))
        user_challenge = input('> ')

        if user_challenge == str(challenge):
            verified = True
            print('you\'re are now verified as a robot :]')
        else:
            print('you\'re not a robot ;[')
        signal.alarm(0)

    except MyTimeoutError:
        print('\nyou failed to verify! robots aren\'t that slow ;[')

def flag():
    global money

    print('price of the flag is $10,000,000,000.')

    if money < 10000000000:
        print('you don\'t have enough money (your money: ${0}).'.format(money))
        return

    with open('./flag', 'rb') as f:
        print(b'flag is ' + f.read())
    sys.exit()

def main():
    while True:
        show_menu()
        menu = int(input('> '))

        if menu == MENU_GAMBLE:
            gamble()

        elif menu == MENU_VERIFY:
            verify()

        elif menu == MENU_FLAG:
            flag()

        elif menu == MENU_LEAVE:
            sys.exit()

        else:
            print('wrong menu :[')

if __name__ == '__main__':
    main()
