# test_helpers.py

from utils.helpers import greet_user

if __name__ == "__main__":
    name = input("Bitte gib deinen Namen ein: ")
    print(greet_user(name))
