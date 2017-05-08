# COMS 3101 Final Project
# Author: Wode "Nimo" Ni
# a lightweight, easy‐to‐use, command‐line GTD program,

from utils import colors
from json import load, dump, loads, dumps
import logging


USER_NAME = None
tasks = []
get_color = {}
LOG_FORMAT = "%(levelname)s at %(asctime)s:%(message)s" 
MODULE_MAIN_NAME = __name__

class task:
    "Main task class that represent a generic task"
    def __init__(self, id, desc):
        self.id = id
        self.desc = desc
    # Trying hard to be Pytonic here
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, id):
        self.__id = id
    @property
    def desc(self):
        return self._desc
    @desc.setter
    def desc(self):
        return self._desc

class todo(task):
    "A todo task with a due date"
    def __init__(self, id, desc, done):
        super().__init__(id, desc)

    @property
    def done(self):
        return self.__done
    @done.setter
    def done(self, done):
        self.__done = done



def init():
    "Called upon start up, populate information. If none is stored, ask for the user information"
    # Color settings
    global get_color, USER_NAME, tasks
    color_scheme = {"prompt" : [colors.HEADER, colors.BOLD]}
    get_color = { s: colors.get_color_wrapper(color_scheme[s]) for s in color_scheme}
    # Logger settings
    logging.basicConfig(filename='donepy.log', \
            format = LOG_FORMAT, level=logging.DEBUG)
    logging.debug("Starting DonePy")
    # loading init info
    if(not load_init_json()):
        USER_NAME = input(get_color["prompt"]("Welcome to DonePy. May I have your name please: "))
        while(not check_username(USER_NAME)):
            USER_NAME = input(get_color["prompt"]("Format error. Please input a name consisting only letters: "))
    else:
        print_prompt()
        

def main():
    "The main loop of the program. Act like shell"
    init()
    input_str = ""
    while(input_str != "exit"):
        input_str = input(get_color["prompt"]("[DonePy] >> "))

    # Exiting the program
    logging.debug("Exiting DonePy")
    write_init_json()

def write_init_json():
    global USER_NAME, tasks
    with open("donepy_init.json", "w") as opf:
        TO_SAVE = {"username": USER_NAME, "tasks": tasks}
        dump(TO_SAVE, opf)
        # Exactly the same
        logging.debug("Written info to init file")

def load_init_json():
    "Load user info and todos from a json file"
    global USER_NAME, tasks
    try:
        with open("donepy_init.json", "r") as ipf:
            loaded = load(ipf)
            USER_NAME = loaded["username"]
            tasks = loaded["tasks"]
            # Exactly the same
            logging.debug("Loaded info from init file")
            return True
    except FileNotFoundError:
        logging.debug("Cannot find init file.")
        return False

def check_username(name):
    return True

def print_prompt():
    num_tasks = len(tasks)
    greeting = "Hey " + USER_NAME + ", you currently have " + \
            str(num_tasks) + " tasks to do: "
    if(num_tasks == 0):
        greeting += "\n\tYou really have nothing to do?"

    print(get_color["prompt"](greeting))
    


if(__name__ == "__main__"):
    main()
    
