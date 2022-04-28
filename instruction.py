import os
from cell import *
import json

func_id = {
    add_walls: 1,
    clean_up: 2,
    clean_up_bigger: 3,
    clean_up_huge: 4,
    randomise: 5,
    iterate: 6,
    iterate_new: 7,
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
    
    def perform(self, screen):
        current_instruction = self.instructions[self.index]
        print(current_instruction[info][cell_S])
        # set_cell_size(current_instruction[info][cell_S])
        generate_cells(screen)
        draw(screen.surface)
    
    def increase_index(self):
        if self.index + 1 < len(self.instructions):
            self.index += 1
            Instructions.current_instruction = self.instructions[self.index][name]

    def decrease_index(self):
        if self.index > 0:
            self.index -= 1
            Instructions.current_instruction = self.instructions[self.index][name]
            
            
            
    
    

# def perform_instructions(instruction):
#     size = len(instruction) - 1
#     index = 0
#     count = 0
#     total = instruction[index][1]
#     while True:
#         if index >= size:
#             return 
#         if regular_interval_tick_wait(DELAY):
#             count += 1
#             if count == total:
#                 index+=1
#                 print(index, size)
#                 total += instruction[index][1]
#             instruction[index][0](screen.surface)
#             display_current_board_information(cell_size, 'trip', show_board_info)
#             pygame.display.update()
# good for tile size 30 to 40

# instructions_35 = [
#     "Instruction_35",
#     35,
#     [randomise, 1],
#     [clean_up, 1],
#     [iterate, 16],
#     [clean_up_bigger, 1],
#     [add_walls, 1]
# ]



#good for large open spaces
# instructions_10 = [
#     "Instruction_open_10",
#     10,
#     [randomise, 1],
#     [clean_up_huge, 1],
#     [iterate, 20],
#     [clean_up_bigger, 2],
#     [clean_up , 7],
#     [add_walls, 1]
# ]


# good for islands and more coast
# instructions_10 = [
#     "Instruction_island_10",
#     10, 
#     [randomise, 1],
#     [clean_up_bigger, 1],
#     [iterate, 20],
#     [clean_up_bigger, 2],
#     [clean_up , 5],
#     [add_walls, 1]
# ]

# instructions_5 = [
#     "Instruction_5",
#     5,
#     [randomise, 1],
#     [clean_up_bigger, 1],
#     [iterate, 25],
#     [clean_up_huge, 1],
#     [clean_up, 2],
#     [add_walls, 1]
# ]

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

# w = [
#     {
#     "name" : "Instruction_35",
#     "info" : {"cell_size" : 35,"instructions" : [5,2,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,3,1]}
#     },
#     {
#     "name" : "Instruction_open_10",
#     "info" : {"cell_size" : 10,"instructions" : [5, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 3, 3, 2, 2, 2, 2, 2, 2, 2, 1]}
#     },
#     {
#     "name" : "Instruction_island_10",
#     "info" : {"cell_size" : 10,"instructions" : [5, 3, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 3, 3, 2, 2, 2, 2, 2, 1]}
#     },
#     {
#     "name" : "Instruction_5",
#     "info" : {"cell_size" : 5,"instructions" : [5, 3, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 2, 2, 1]}
#     }
# ]
# manager = Instructions()
# for i in w:
#     manager.add(i)
    
# manager.write_instructions()
# print(len(manager.instructions))
