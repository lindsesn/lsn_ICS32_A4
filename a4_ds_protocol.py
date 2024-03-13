# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Lindsey Nguyen
# lindsesn@uci.edu
# lindsesn

import json
from collections import namedtuple


# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
DataTuple = namedtuple('DataTuple', ['response','type'])

def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  
  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
  try:
    json_obj = json.loads(json_msg)
    response = json_obj['response']
    type = json_obj['response']['type']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(response, type)


class DS_PROTOCOL:
  '''consists of commands to format json, send files, and recieve/read files from the server'''

  def __init__(self, sock):
    self.sock = sock
  
  def write_cmd(self, msg):
    '''sends commands to the server'''
    try:
      send = self.sock.makefile('w')
      send.write(msg + '\r\n')
      send.flush()
    except Exception:
      return False
  
  def read_cmd(self):
    '''reads responses from the server'''
    recv = self.sock.makefile('r')

    resp = recv.readline()
    # print(resp)
    return resp


def build_cmd(key, value):
    '''formats regular dictionaries to json'''
    cmd = {key: value}
    jcmd = json.dumps(cmd, indent = 4)
    return jcmd


def sbuild_cmd(cmd):
  '''formats nested dictionaries to json'''
  jcmd = json.dumps(cmd, indent = 4)
  return jcmd
