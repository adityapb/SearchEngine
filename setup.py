import sys
import os

os.system("wget https://bootstrap.pypa.io/get-pip.py")
os.system("python get-pip.py")
os.system("pip install pyenchant")
os.system("echo 'To run use \"python main.py\" in the search folder')