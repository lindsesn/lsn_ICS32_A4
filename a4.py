# a3.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Lindsey Nguyen
# lindsesn@uci.edu
# lindsesn

from a4_profilehandler import create_user, save_user, save_post, save_bio
from a4ds_client import send


def options(server, port, usern, pwd, msg, user, dsu):
    '''gives the user options to do things on the server like add a post, edit their bio, etc.'''
    quit_program = False
    while quit_program is False:
        action = input("\nWhat would you like to do?\n1. Add a post\n2. Edit your bio\n3. Send a direct message\n\nType the number(s) for your desired actions to continue or type 'q' if you would like to quit the program\n") 
        if "1" in action:
            msg = input("Write a message for your post: ")
            response = send(server, port, usern, pwd, msg)
            if response is True:
                save_post(user, dsu, msg)
        if "2" in action:
            bio = input("Write your new bio: ")
            msg = ''
            response = send(server, port, usern, pwd, msg, bio)
            if response is True:
                save_bio(user, dsu, bio)
        if "3" in action:
            msg = '3: user wants to send a direct message to another user'
            send(server, port, usern, pwd, msg)
        if action in ("q", "Q"):
            quit_program = True


def main():
    '''takes user input to log onto the server and sends the information to the send() function in a4ds_client'''
    try:
        server = input('What is the address of the server you would like to join: ') # '168.235.86.101'
        port = int(input('What is the port number of the server you would like to join: ')) # 3021
        usern =  input('Enter your username: ')
        pwd = input('Enter your password: ')
        msg = '0: initially connecting user to the server'
        response = send(server, port, usern, pwd, msg)
    except Exception:
        print("\nAn error occured while trying to connect to the server. Please try again")
    else:
        if response is True:
            user = create_user(server, usern, pwd)
            dsu = save_user(user)
            options(server, port, usern, pwd, msg, user, dsu)
        else:
            print("\nAn error occured while trying to connect to the server. Please try again")

if __name__ == "__main__":
    main()