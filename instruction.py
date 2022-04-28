import os
from cell import *
import json
from time_wait import regular_interval_tick_wait

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
                Instructions.current_instruction = self.get_current_instruction()[NAME]

            open_file.close()
    def get_current_instruction(self):
        return self.instructions[self.index]
    
    def write_instructions(self):
        if len(self.instructions) < 1:
            return
        
        with open(self.file, "w") as out_file:
            json.dump(self.instructions, out_file)
    
    def perform(self, screen, show_info):
        current_instruction = self.get_current_instruction()
        optional_size_change  = current_instruction[INFO][CELL_S]
        if optional_size_change != False: 
            handle_set_cell_size(current_instruction[INFO][CELL_S], screen)
            generate_cells(screen)
            draw(screen.surface)
        instruction = current_instruction[INFO][INST]
        size = len(instruction) 
        index = 0
        while True:
            if index >= size: 
                break
            if regular_interval_tick_wait(DELAY):
                id = instruction[index]
                id_func[id](screen.surface)
                index += 1
                display_current_board_information(show_info)
                pygame.display.update()
    
    def increase_index(self):
        if self.index + 1 < len(self.instructions):
            self.index += 1
            Instructions.current_instruction = self.get_current_instruction()[NAME]

    def decrease_index(self):
        if self.index > 0:
            self.index -= 1
            Instructions.current_instruction = self.get_current_instruction()[NAME]
            

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