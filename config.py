ALIVE = 'Green'
DEAD = 'Blue'
ROCK = 'Gray'
LAKE = 'Lightblue'
PATH = 'Brown'
FULLSCREEN = False
DELAY = 60
NAME = "name"
INFO = "info"
CELL_S = "cell_size"
INST = "instructions"
KEY_BINDS = {
    "f" : "full_screen",
    "s" : "toggle show board information",
    "k" : "toggle show keybind information",
    "m" : "show territories",
    "c" : "create new instruction from existing board steps",
    "r" : "reset current board instructions",
    "ESCAPE" : "quit",
    "COMMA" : "prev command",
    "PERIOD" : "next command",
    "SPACE" : "execute selected_command",
    "TAB" : "perform_instruction",
    "UP" : "increse size of cell",
    "DOWN" : "decrese size of cell",
    "RIGH" : "next instruction",
    "LEFT" : "previous instruction"
}
territory_colours = [
    [242, 182, 182],
    [242, 207, 182],
    [242, 238, 182],
    [213, 242, 182],
    [182, 242, 196],
    [182, 242, 232],
    [182, 221, 242],
    [183, 182, 242],
    [205, 182, 242],
    [229, 182, 242],
    [207, 126, 83],
    [207, 170, 83],
    [174, 207, 83],
    [95, 207, 83],
    [83, 207, 162],
    [83, 178, 207],
    [143, 83, 207],
    [205, 83, 207],
    [82, 11, 40],
    [108, 110, 7],
]