# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Lindsey Nguyen
# lindsesn@uci.edu
# lindsesn

import socket
import time
import io
from pathlib import Path
from a4Profile import Profile, Post
from a4ds_protocol import DS_PROTOCOL, build_cmd, sbuild_cmd, extract_json

def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
  #TODO: return either True or False depending on results of required operation
  try:
    sock = connect_to_server(server, port)
    dsp = DS_PROTOCOL(sock)
    join_cmd = build_cmd('join', {'username': username, 'password': password, 'token': ''})
    dsp.write_cmd(join_cmd)
    server_resp = dsp.read_cmd()
    server_data = extract_json(server_resp)

    token = ''

    if server_data.type == "ok":
      token = server_data.response['token']
      user = create_user(server, username, password) # creates a Profile class instance from user info
      dsu_file = save_user(user) # saves user's profile in a dsu
      if (message == '0: initially connecting user to the server') and (bio is None): # if the conditions are satisfied (or when the user initially connnects to the server),  the console will print 'Welcome back' 
        return_resp(server_data)
    else: # send() returns False if server_data.type is not 'ok'
      return False
    
    rectime = time.time()

    keycmds = ('0: initially connecting user to the server', '3: user wants to send a direct message to another user')
   
  # add post functionality
    if (message != '') and (message not in keycmds) and (bio is None):
      send_resp = send_cmd(dsp, token, 'post', message, rectime)
      send_data = extract_json(send_resp)
    
      if send_data.type == "ok":
        post = Post(message)
        Profile()
        user.add_post(post)
        user.save_profile(dsu_file)
        return_resp(send_data)
      elif send_data.type == "error":
        return_resp(send_data)
      else:
        return False

  # edit bio functionality
    if bio is not None:
      send_resp = send_cmd(dsp, token, 'bio', bio, rectime)
      send_data = extract_json(send_resp)

      if send_data.type == "ok":
        Profile()
        user.bio = bio
        user.save_profile(dsu_file)
        return_resp(send_data)
      elif send_data.type == "error":
        return_resp(send_data)
      else:
        return False

  # send a direct message functionality
    if (message == '3: user wants to send a direct message to another user') and (bio is None):
      recipient = input('Who do you want to send the message to?: ')
      the_msg = input('Write a message to send:')

  except Exception as e:
    print(e)
    return False
  else:
    return True


def connect_to_server(server, port):
  '''creates a socket to connect to the server'''
  try:
    server_address = (server, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    return sock
  except:
    return None
  

def create_user(server, username, password):
  '''instantiates Profile class to store user information'''
  user = Profile(server, username, password)
  return user


def save_user(profile):
  '''saves the user's information in a dsu file by calling on the save_profile() method in Profile class'''
  dsu_file_path = input('Provide the entire file path of where you would like to save your user information (must be a .dsu file): ')
  dsu_exists = check_dsu_exists(dsu_file_path)
  if dsu_exists is False:
    created_dsu_file = create_dsu(dsu_file_path)
    profile.save_profile(created_dsu_file)
    return created_dsu_file
  elif dsu_exists is True:
    profile.save_profile(dsu_file_path)
    return dsu_file_path


def check_dsu_exists(path):
  '''checks to see if the dsu file path exists'''
  p = Path(path)
  if p.exists():
    return True


def create_dsu(p):
  '''creates a new dsu file based on the user's input about where they want to store their user information'''
  with open(p, "w") as my_file:
    try:
        for line in my_file:
            print(line)
    except io.UnsupportedOperation: # reason why "import io" was placed in line 2
        pass
    except NameError:
        print("NameError: please try again.")
    except FileExistsError:
        print("Error: file already exists, please try again")
  return p


def return_resp(response):
  '''prints the response messages from the server'''
  if response.type == "ok":
    print(response.response['message'] + "\n")
  elif response.type == "error":
    print(response.response['message'] + "\n")


def send_cmd(dsp, token, cmd_type, message, time):
  '''builds a command to send to the server'''
  cmd = sbuild_cmd({'token': token, cmd_type: {'entry': message, 'timestamp': time}})
  dsp.write_cmd(cmd)
  return dsp.read_cmd()