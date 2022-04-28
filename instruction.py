import os
from cell import *
import json
from time_wait import regular_interval_tick_wait

func_id = {
    add_walls: 1,
    clean_up: 2,
    clean_up_bigger: 3,
    clean_up_huge: 4,
    randomise: 5,
    iterate: 6,
    iterate_new: 7,
}

id_func = {
    1: add_walls,
    2: clean_up,
    3: clean_up_bigger,
    4: clean_up_huge,
    5: randomise,
    6: iterate,
    7: iterate_new,
}

name = "name"
info = "info"
cell_S = "cell_size"
inst = "instructions"

class Instructions:
    current_instruction = ""
    def __init__(self):
        self.index = 0
        self.file = "instructions.json"
        self.read_instructions()
    
    def add(self, instruction):
        if instruction not in self.instructions:
            self.instructions.append(instruction)
        
    def read_instructions(self):
        with open(self.file, "r") as open_file:
            if os.stat(self.file).st_size == 0:
                self.instructions = []
                Instructions.current_instruction = "none"
            else:
                self.instructions = json.load(open_file)
                Instructions.current_instruction = self.instructions[self.index][name]

            open_file.close()
    
    def write_instructions(self):
        if len(self.instructions) < 1:
            return
        
        with open(self.file, "w") as out_file:
            json.dump(self.instructions, out_file)
    
    def perform(self, screen, show_info):
        current_instruction = self.instructions[self.index]
        optional_size_change  = current_instruction[info][cell_S]
        if optional_size_change != False: 
            handle_set_cell_size(current_instruction[info][cell_S], screen)
            generate_cells(screen)
            draw(screen.surface)
        instruction = current_instruction[info][inst]
        size = len(instruction) 
        index = 0
        while True:
            if index >= size: 
                break
            if regular_interval_tick_wait(DELAY):
                id = instruction[index]
                id_func[id](screen.surface)
                index += 1
                display_current_board_information(Instructions.current_instruction, show_info)
                pygame.display.update()
    
    def increase_index(self):
        if self.index + 1 < len(self.instructions):
            self.index += 1
            Instructions.current_instruction = self.instructions[self.index][name]

    def decrease_index(self):
        if self.index > 0:
            self.index -= 1
            Instructions.current_instruction = self.instructions[self.index][name]
            

instructions_trip = [
    "Trip",
    False,
    [randomise, 1],
    [clean_up_bigger, 7],
    [iterate_new, 25],
    [clean_up_bigger, 7],
    [iterate_new, 25],
    [clean_up_bigger, 7],
    [iterate_new, 25],
    [clean_up_bigger, 7],
    [iterate_new, 25]
]