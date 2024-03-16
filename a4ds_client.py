# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Lindsey Nguyen
# lindsesn@uci.edu
# lindsesn

import socket
import time
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
      if (message == '0: initially connecting user to the server') and (bio is None): # if the conditions are satisfied (or when the user initially connnects to the server),  the console will print 'Welcome back' 
        return_resp(server_data)
    else: # send() returns False if server_data.type is not 'ok'
      return False

    rectime = time.time()

    keycmds = ('0: initially connecting user to the server', '3: user wants to send a direct message to another user')

    # send a direct message functionality
    if (message == '3: user wants to send a direct message to another user') and (bio is None):
      recipient = input('Who do you want to send the message to?: ')
      the_msg = input('Write a message to send: ')

      send_resp = dm_send_cmd(dsp, token, the_msg, recipient, rectime)
      send_data = extract_json(send_resp)

      if send_data.type == "ok":
        return_resp(send_data) # implement Profile class
      elif send_data.type == "error":
        return_resp(send_data)

  # add post functionality
    if (message != '') and (message not in keycmds) and (bio is None):
      send_resp = send_cmd(dsp, token, 'post', message, rectime)
      send_data = extract_json(send_resp)

      if send_data.type == "ok":
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
        return_resp(send_data)
      elif send_data.type == "error":
        return_resp(send_data)
      else:
        return False

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
  except Exception:
    return None


def return_resp(response):
  '''prints the response messages from the server'''
  if response.type == "ok":
    print(response.response['message'] + "\n")
  elif response.type == "error":
    print(response.response['message'] + "\n")


def send_cmd(dsp, token, cmd_type, message, timestamp):
  '''builds a command to send to the server, EXCEPT for when the user sends direct messages'''
  cmd = sbuild_cmd({'token': token, cmd_type: {'entry': message, 'timestamp': timestamp}})
  dsp.write_cmd(cmd)
  return dsp.read_cmd()


def dm_send_cmd(dsp, token, msg, recipient, timestamp):
  '''builds a command to send to the server to send direct messages'''
  direct_msg_dict = {"entry": msg,"recipient": recipient, "timestamp": timestamp}
  cmd = sbuild_cmd({"token": token, "directmessage": direct_msg_dict})
  dsp.write_cmd(cmd)
  return dsp.read_cmd()