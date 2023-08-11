#!/usr/bin/env python3

def main():
    flag = open("flag.txt").read()
    while True:
        pwd = input("Enter your password: ").ljust(len(flag))
        if pwd == "exit":
            exit()
        count = sum(pwd[i] != c for i, c in enumerate(flag))
        if count == 0:
            print("Logged in successfully!")
            exit()
        else:
            print(f"Close! You're just {count} character{'s' if count else ''} off of your password.")


if __name__ == '__main__':
    main()