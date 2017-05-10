# COMS 3101 Final Project
# Author: Wode "Nimo" Ni
# a lightweight, easy‐to‐use, command‐line GTD program,

from argparse import ArgumentParser
from utils import colors
# from json import load, dump, loads, dumps
from pickle import load, dump, loads, dumps
import subprocess as sp
import logging
import os


USER_NAME = None
tasks = []
get_color = {}
LOG_FORMAT = "%(levelname)s at %(asctime)s:%(message)s" 
COMMANDS = ['add', 'remove', 'clear', 'done', 'view']
CLASSES  = ['todo']
MODULE_MAIN_NAME = __name__

class task:
    "Main task class that represent a generic task"
    def __init__(self, id, desc):
        self._id = id
        self._desc = desc
        self._subtasks = []
    # Trying hard to be Pytonic here
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        self._id = id
    @property
    def desc(self):
        return self._desc
    @desc.setter
    def desc(self, d):
        self._desc = d
    @property
    def subtasks(self):
        return self._subtasks
    @subtasks.setter
    def subtasks(self, s):
        self._subtasks = s
    def __add__(self, r):
        self.subtasks.append(r)


class todo(task):
    "A todo task"
    def __init__(self, id, desc, done):
        super().__init__(id, desc)
        self._done = False

    @property
    def done(self):
        return self._done
    @done.setter
    def done(self, done):
        self._done = done
        def mark_done(task, v):
            if(len(task.subtasks) != 0):
                map(mark_done,task.subtasks)
        map(mark_done, self.subtasks)
    def __str__(self):
        global get_color
        res = ""
        if(self.done): res += "[x] "
        else : res += "[ ] "
        res += self.desc
        if(self.done): return get_color["done"](res)
        else: return get_color["undone"](res)


def init():
    "Called upon start up, populate information. If none is stored, ask for the user information"
    # Color settings
    global get_color, USER_NAME, tasks
    color_scheme = {"prompt" : [colors.HEADER, colors.BOLD], 
                    "done" : [colors.OKGREEN],
                    "undone" : [colors.UNDONE],
                    "warning": [colors.YELLOW]}
    get_color = { s: colors.get_color_wrapper(color_scheme[s]) for s in color_scheme}
    # Data folder initialization
    if not os.path.exists("donepy"):
        os.makedirs("donepy")
    # Logger settings
    logging.basicConfig(filename='donepy/donepy.log', \
            format = LOG_FORMAT, level=logging.DEBUG)
    logging.debug("Starting DonePy")
    # Parsing argument
    parser = ArgumentParser()
    parser.add_argument("name", help = "Your user name")
    parser.add_argument("--clear", "-c",  action='store_true', \
            help = "Clearing historical data")
    parse_result = parser.parse_args()
    name = parse_result.name
    clear = parse_result.clear
    # loading init info
    if(clear or not load_init_json(name)):
        print(get_color["prompt"]("Seems like you are here for the first time. Welcome! \nInitializing your info..."))
        USER_NAME = name
        while(not check_username(USER_NAME)):
            USER_NAME = input(get_color["prompt"]("Format error. Please input a name consisting only letters: "))
    print_prompt()
        
def write_init_json():
    global USER_NAME, tasks
    filename = "donepy/" + USER_NAME + "_donepy_init.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as opf:
        for t in tasks:
            if(t.done): tasks.remove(t)
        TO_SAVE = {"username": USER_NAME, "tasks":  \
                   # (t.toJSON() for t in tasks))}
                   tasks}
        dump(TO_SAVE, opf)
        # Exactly the same
        logging.debug("Written info to init file")

def load_init_json(name):
    "Load user info and todos from a json file"
    global USER_NAME, tasks
    try:
        with open("donepy/" + name + "_donepy_init.json", "rb") as ipf:
            loaded = load(ipf)
            USER_NAME = loaded["username"]
            tasks = loaded["tasks"]
            # Exactly the same
            logging.debug("Loaded info from init file for " + name)
            return True
    except FileNotFoundError:
        logging.debug("Cannot find init file for " + name)
        return False

def check_username(name):
    "Use regex to check the validity of the username"
    return True
def check_idx(idx):
    return True

def print_prompt():
    global tasks
    num_tasks = len(tasks)
    greeting = "Hey " + USER_NAME + ", you currently have " 
    if(num_tasks == 1): 
        greeting += str(num_tasks) + " task to do: "
    else: 
        greeting += str(num_tasks) + " tasks to do: "
    if(num_tasks == 0):
        greeting += "\n\tYou really have nothing to do?"
    print(get_color["prompt"](greeting))
    print("")
    print_tasks(tasks, 1, "")

def print_tasks(tasks, level, id):
    if(tasks == None): return
    for i, task in enumerate(tasks): 
        print('\t' * level + id + str(i) + " - " + str(task))
        print_tasks(task.subtasks, level + 1, id + "." + str(i))

def cmd(cmd):
    "main function that processes commands"
    cmd_arr = cmd.split()
    if(len(cmd_arr) == 0): return
    for i in range(0, len(cmd_arr)):
        s = cmd_arr[i]
        if(s in COMMANDS):
            process_cmd(s, cmd_arr[i+1:])

def process_cmd(cmd, args):
    "helper function that invokes the actual methods"
    if(cmd == 'add'):
        cmd_add(args[0])
    elif(cmd == 'remove'):
        cmd_remove(args)
    elif(cmd == 'clear'):
        clear()
    elif(cmd == 'done'):
        cmd_done(args[0])
    elif(cmd == 'view'):
        print_prompt()
    else:
        raise ValueError("Invalid command")

def cmd_add(task_class):
    if(task_class in CLASSES):
        if(task_class == "todo"):
            desc = input(get_color['prompt']("Description of the todo: "))
            t = todo(len(tasks), desc, False)
            tasks.append(t)
        print_prompt()

    else: 
        print(get_color['warning']("[ERROR]: Invalid argument to the add operation"))

def cmd_done(idx):
    if(check_idx(idx)):
        task = find_task(idx)
        task.done = True
        print_prompt()
    else:
        print(get_color['warning']("[ERROR]: Invalid argument to the done operation"))

def find_task(string):
    "given a string in the format like '1.1.1', find the correct object"
    arr = string.split(".")
    cur_tasks = tasks
    for i in arr:
        task = cur_tasks[int(i)]    
        if(len(task.subtasks) != 0): 
            cur_tasks = task.subtasks
    return task

def clear():
    "clear the console by calling the shell version of clear"
    tmp = sp.call('clear',shell=True)

def main():
    "The main loop of the program. Act like shell"
    init()
    input_str = ""
    while(input_str != "exit"):
        input_str = input(get_color["prompt"]("[DonePy] >> "))
        cmd(input_str)

    # Exiting the program
    logging.debug("Exiting DonePy")
    write_init_json()

if(__name__ == "__main__"):
    main()
