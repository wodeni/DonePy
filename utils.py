MODULE_MAIN_NAME = __name__

class colors:
    # color codes adopted from http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def get_color_wrapper(start = [], end = [RESET]):
        start_str = ''
        end_str   = ''
        for s in start: start_str += s
        for s in end: end_str += s
        return (lambda x: start_str + x + end_str)
