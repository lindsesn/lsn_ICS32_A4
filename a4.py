# a3.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Lindsey Nguyen
# lindsesn@uci.edu
# lindsesn

from a4_ds_client import send


def options(server, port, usern, pwd, msg):
    '''asks user what they want to do on the server'''
    quit_program = False
    while quit_program is False:
        action = input("\nWhat would you like to do?\n1. Add a post\n2. Edit your bio\n3. Direct message\n4. See unread direct messages\n5. See all your direct messages\n\nSelect the number(s) from the list of actions above to continue\nType 'q' if you would like to quit the program\n")
        
        if "1" in action: # ("add" in action) or ("add post" in action):
            msg = input("Write a message for your post: ")
            send(server, port, usern, pwd, msg)
        if "2" in action: # "edit bio" in action:
            bio = input("Write your new bio: ")
            msg = ''
            send(server, port, usern, pwd, msg, bio)
        if "3" in action: # "dm" in action:
            recipient = input("Who would you like to message? (Type the recipient's username): ")
            msg = input("Write a message: ")
            bio = None
            send(server, port, usern, pwd, msg, bio, recipient)
        if "4" in action:
            msg = 'keyto4:userwantstogetunreaddms'
            send(server, port, usern, pwd, msg)
        if "5" in action:
            msg = 'keyto5:userswantstogetalldms'
            send(server, port, usern, pwd, msg)
        if action in ('q', 'Q'):
            quit_program = True


def main():
    '''takes server, port, and login info input from the user '''
    try:
        server = input('What is the address of the server you would like to join: ') # '168.235.86.101'
        port = int(input('What is the port number of the server you would like to join: ')) # 3021
        usern =  input('Enter your username: ')
        pwd = input('Enter your password: ')
        msg = ''


        response = send(server, port, usern, pwd, msg)
    except Exception:
        print("\nAn error occured while trying to connect to the server. Please try again")
    else:
        if response is True:
            options(server, port, usern, pwd, msg)
        else:
            print("\nAn error occured while trying to connect to the server. Please try again")

if __name__ == "__main__":
    main()