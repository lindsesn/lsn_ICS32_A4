# a4ds_dsuhandler.py
# receives user information from a4 in a dsu file, separate from the send function and a4ds_client.py

import io
from pathlib import Path
from a4Profile import Profile, Post

def create_user(server, username, password):
  '''instantiates Profile class to store user information'''
  user = Profile(server, username, password)
  return user


def save_user(user):
  '''saves the user's information in a dsu file by calling on the save_profile() method in Profile class'''
  dsu_file_path = input('Provide the entire file path of where you would like to save your user information (must be a .dsu file): ')
  dsu_exists = check_dsu_exists(dsu_file_path)
  if dsu_exists is False:
    created_dsu_file = create_dsu(dsu_file_path)
    user.save_profile(created_dsu_file)
    return created_dsu_file
  if dsu_exists is True:
    user.save_profile(dsu_file_path)
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


def save_post(user, dsu, message):
  '''saves a post to the user's instantiation of the Profile class and in their dsu file'''
  post = Post(message)
  Profile()
  user.add_post(post)
  user.save_profile(dsu)


def save_bio(user, dsu, bio):
  '''saves the user's bio to the user's isntantiation of the Profile class and in their dsu file'''
  Profile()
  user.bio = bio
  user.save_profile(dsu)