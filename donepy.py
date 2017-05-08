# COMS 3101 Final Project
# Author: Wode "Nimo" Ni
# a lightweight, easy‐to‐use, command‐line GTD program,

from utils import colors
import logging


numtasks = 0
username = ""
get_color = {}
LOG_FORMAT = "%(levelname)s at %(asctime)s:%(message)s" 
MODULE_MAIN_NAME = __name__

class task:
    "Main task class that represent a generic task"
    _desc = None
    _id = None
    _due = None

    def __init__(self):
        pass


def init():
    "Called upon start up, populate information. If none is stored, ask for the user information"
    # Color settings
    global get_color
    color_scheme = {"prompt" : [colors.HEADER, colors.BOLD]}
    get_color = { s: colors.get_color_wrapper(color_scheme[s]) for s in color_scheme}
    # Logger settings
    logging.basicConfig(filename='donepy.log', \
            format = LOG_FORMAT, level=logging.DEBUG)
    logging.debug("Starting DonePy")

def main():
    "The main loop of the program. Act like shell"
    init()
    input_str = ""
    while(input_str != "exit"):
        input_str = input(get_color["prompt"]("[DonePy] >> "))

    # Exiting the program
    logging.debug("Exiting DonePy")

def load_json():
    "Load user info and todos from a json file"
    pass

if(__name__ == "__main__"):
    main()
    
