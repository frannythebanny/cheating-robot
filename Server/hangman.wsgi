import sys, logging
logging.basicConfig(stream=sys.stderr)
sys.path.append('/home/pold/Documents/Radboud/HRI/cheating-robot/Server/run_flask.py')
from run_flask import app as application
