# create a python virtual environment and install packages in requirements.txt
import os
import sys
import subprocess

# create virtual environment
subprocess.run(["python", "-m", "venv", "venv"])
# activate virtual environment
subprocess.run(["venv\\Scripts\\activate.bat"])
# install packages in requirements.txt
subprocess.run(["pip", "install", "-r", "requirements.txt"])
