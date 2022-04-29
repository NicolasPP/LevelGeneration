import os
from cell import *
import json
from time_wait import regular_interval_tick_wait

class Instructions_manager:
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
                Instructions_manager.current_instruction = "none"
            else:
                self.instructions = json.load(open_file)
                Instructions_manager.current_instruction = self.get_current_instruction()[NAME]

            open_file.close()
    def get_current_instruction(self):
        return self.instructions[self.index]
    
    def write_instructions(self):
        if len(self.instructions) < 1:
            return
        
        with open(self.file, "w") as out_file:
            json.dump(self.instructions, out_file)

    def handle_optional_resize(self, screen):
        self.current_instruction = self.get_current_instruction()
        optional_size_change  = self.current_instruction[INFO][CELL_S]
        if optional_size_change != False: 
            handle_set_cell_size(self.current_instruction[INFO][CELL_S], screen)
            generate_cells(screen)
            draw(screen.surface)
        
    def perform(self, index, screen):
        ids = self.current_instruction[INFO][INST]
        current_func_id = ids[index]
        func = id_func[current_func_id]
        func(screen.surface)
        if index == len(ids) -1:
            return False
        return True
    
    def increase_index(self):
        if self.index + 1 < len(self.instructions):
            self.index += 1
            Instructions_manager.current_instruction = self.get_current_instruction()[NAME]

    def decrease_index(self):
        if self.index > 0:
            self.index -= 1
            Instructions_manager.current_instruction = self.get_current_instruction()[NAME]
            