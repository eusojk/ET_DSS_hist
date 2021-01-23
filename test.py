import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

Wdir_path = "dssat_files_dir/"
os.chdir(Wdir_path) 

path = os.getcwd() 
print("Current Directory", path)

# prints parent directory 
# print("parent")
# print(os.path.abspath(os.path.join(path, os.pardir))) 

parent = os.path.abspath(os.path.join(path, os.pardir))
os.chdir(parent) 

path = os.getcwd() 
print("Current Directory", path)