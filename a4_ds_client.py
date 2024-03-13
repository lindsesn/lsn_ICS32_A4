# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Lindsey Nguyen
# lindsesn@uci.edu
# lindsesn

import socket
import time
from a4_Profile import Profile, Post
from a4_ds_protocol import DS_PROTOCOL, build_cmd, sbuild_cmd, extract_json


def send(server:str, port:int, username:str, password:str, message:str, bio:str=None, recipient:str=None):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
  # TODO: return either True or False depending on results of required operation
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
      user = create_user(server, username, password)
      if (message == '') and (bio is None) and (recipient is None):
        return_resp(server_data)
    else:
      return False
    
    rectime = time.time()

  # see unread or all direct messages functionality
    if recipient is None and message != '' and message in ('keyto4:userwantstogetunreaddms', 'keyto5:userswantstogetalldms'):
      send_resp = read_dms_cmd(dsp, token)
      send_data = extract_json(send_resp)
      if send_data.type == "ok":
        return_resp(send_data)
      elif send_data.type == "error":
        return_resp(send_data)
      else:
        return False

  # direct message functionality
    if (recipient is not None) and (message != ''):
      dm_send_resp = dm_send_cmd(dsp, token, message, recipient, rectime)
      dm_send_data = extract_json(dm_send_resp)
      if dm_send_data.type == "ok":
        return_resp(dm_send_data)
      elif dm_send_data.type == "error":
        return_resp(dm_send_data)
      else:
        return False

  # add post functionality
    if (message != '') and (bio is None) and (recipient is None):
      send_resp = send_cmd(dsp, token, 'post', message, rectime)
      send_data = extract_json(send_resp)
    
      if send_data.type == "ok":
        post = Post(message)
        Profile()
        user.add_post(post)
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
        return_resp(send_data)
      elif send_data.type == "error":
        return_resp(send_data)
      else:
        return False

  except Exception:
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
  

def create_user(server, username, password):
  '''calls on the Profile class for a new instance'''
  user = Profile(server, username, password)
  return user


def return_resp(response):
  '''prints the response message from the server'''
  if response.type == "ok":
    print(response.response['message'] + "\n")
  elif response.type == "error":
    print(response.response['message'] + "\n")


def send_cmd(dsp, token, cmd_type, message, current_time):
  '''builds a json based on the user's command and sends it to the server'''
  cmd = sbuild_cmd({'token': token, cmd_type: {'entry': message, 'timestamp': current_time}})
  dsp.write_cmd(cmd)
  return dsp.read_cmd()


def dm_send_cmd(dsp, token, message, recipient, current_time):
  '''builds a json based on the user's command to direct message and sends it to the server'''
  cmd = sbuild_cmd({"token": token, "directmessage": {"entry": message,"recipient": recipient, "timestamp": current_time}})
  dsp.write_cmd(cmd)
  return dsp.read_cmd()

def read_dms_cmd(dsp, token):
  '''builds a json based on the user's command to read unread or all direct messages and sends it to the server'''
  cmd = dsp.build_cmd({"token": token, "directmessage": "new"})
  dsp.write_cmd(cmd)
  return dsp.read_cmd()