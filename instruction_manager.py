import os
import json
from lable import Lable
from time_wait import regular_interval_tick_wait
from cell import *

from utils import time_func

class Instructions_manager:
    current_instruction = ""
    def __init__(self, id_func, screen, file = "data/instructions.json"):
        self.id_func = id_func
        self.index = 0
        self.perform = False
        self.perform_index = 0
        self.file = file
        self.read_instructions()
        self.current_board_steps = []
        self.show_del_alert = False
        self.yes, self.no, self.warn =  self.get_del_GUI(screen)
        
    def write_instructions(self):
        if len(self.instructions) < 1:
            return
        
        with open(self.file, "w") as outfile:
            json.dump(self.instructions, outfile)
            outfile.close()  
    def read_instructions(self):
        with open(self.file, "r") as open_file:
            if os.stat(self.file).st_size == 0:
                self.instructions = []
                Instructions_manager.current_instruction = "none"
            else:
                self.instructions = json.load(open_file)
                Instructions_manager.current_instruction = self.get_current_instruction()[NAME]

            open_file.close()
    
    #helper functions
    def add(self, instruction):
        if instruction not in self.instructions:
            self.instructions.append(instruction)
    def get_current_instruction(self):
        return self.instructions[self.index]
    def handle_optional_resize(self, screen):
        self.current_instruction = self.get_current_instruction()
        optional_size_change  = self.current_instruction[INFO][CELL_S]
        if optional_size_change != False: 
            handle_cell_size_change(self.current_instruction[INFO][CELL_S], screen)
            generate_cells(screen)
    def increase_index(self):
        if self.index + 1 < len(self.instructions):
            self.index += 1
            Instructions_manager.current_instruction = self.get_current_instruction()[NAME]
            Cell.draw_all()
    def decrease_index(self):
        if self.index > 0:
            self.index -= 1
            Instructions_manager.current_instruction = self.get_current_instruction()[NAME]
            Cell.draw_all()

    #execution

    def handle_perform(self, screen):
        if self.perform:
            if regular_interval_tick_wait(DELAY):
                self.perform = self.perform_step(screen)
                self.perform_index += 1
    def toggle_perform(self, screen):
        self.perform = not self.perform
        self.perform_index = 0
        self.handle_optional_resize(screen)
        if self.perform: self.current_board_steps = []
    def perform_step(self, screen):
        steps = self.current_instruction[INFO][INST]
        current_func_id = steps[self.perform_index]
        #function call
        self.id_func[current_func_id](screen)
        self.current_board_steps.append(current_func_id)
        if self.perform_index == len(steps) -1:
            return False
        return True
    
    def get_formatted_steps(self, steps):
        if len(steps) == 0:
            return False
        result = []
        last = steps[0]
        result.append([last, 1])
        for func_name in steps[1:]:
            if func_name == last:
                result[-1][1] += 1
            else:
                result.append([func_name, 1])
            last = func_name
        return result

    def get_title(self):
        if len(self.current_board_steps) == 0: return f"[ Current Board Steps : empty ] size: {Cell.cell_size}"
        return f"[ Current Board Steps ] size: {Cell.cell_size}"

    def add_step(self, func_name):
        self.current_board_steps.append(func_name)

    def create_new_instruction(self):
        print('name instruction "n" to cancel')
        name = input().strip()
        if name == 'n':
            print('canceled')
            return
        info = {CELL_S : Cell.cell_size, INST : self.current_board_steps}
        instruction = {NAME : name, INFO : info}
        self.add(instruction)
        self.write_instructions()
        self.read_instructions()
    def delete_instruction(self):
        instruction = self.get_current_instruction()
        self.instructions.remove(instruction)
        self.check_index()
        self.show_del_alert
        self.toggle_show_delete()
        self.write_instructions()
        self.read_instructions()
    

    def check_index(self):
        inst_size = len(self.instructions)
        if inst_size <= self.index: self.index = inst_size - 1


    def get_del_GUI(self, screen):
        current_instruction = self.get_current_instruction()
        instruction_name = current_instruction[NAME]
        yes = Lable('Yes', (screen.current_width // 2) + 15, (screen.current_height // 2) + 30, 20, 'Red')
        no = Lable('No', (screen.current_width // 2) - 15, (screen.current_height // 2) + 30, 20, 'Green')
        warn = Lable(f'Do you want to delete instruction: {instruction_name}', (screen.current_width // 2), (screen.current_height // 2), 20, 'Red')
        warn.center()
        return yes, no, warn
    def display_del_alert(self, screen):
        if self.show_del_alert:
            self.yes.draw(screen.surface)
            self.no.draw(screen.surface)
            self.warn.draw(screen.surface)
    def toggle_show_delete(self):
        self.show_del_alert = not self.show_del_alert
        Cell.draw_all()
    def handle_del_mouse_click(self, pos):
        if self.yes.handle_click(pos): self.delete_instruction()
        elif self.no.handle_click(pos): self.toggle_show_delete()
        
    #Draw functions
    def show_new_instruction(self, show_info):
        if show_info:
            pos_x = pos_y = 10
            title = self.get_title()
            display_info(title, pos_x, pos_y)
            pos_y += 20
            f_steps = self.get_formatted_steps(self.current_board_steps)
            if f_steps:
                for step in f_steps:
                    pos_y += 20
                    name = step[0]
                    amount = step[1]
                    func_info = f'{name} : {amount}'
                    display_info(func_info, pos_x, pos_y)
    def show_current_instruction(self, screen, show_info):
        if show_info: 
            pos_x = screen.current_width - 200
            pos_y = 10
            instruction = self.get_current_instruction()
            ids = instruction[INFO][INST]
            info_name = "--- Current Instruction ---"
            instruction_name = instruction[NAME]
            instruction_info = f'name : {instruction_name}'
            display_info(info_name, pos_x, pos_y)
            pos_y += 20
            display_info(instruction_info, pos_x, pos_y) 
            if len(ids) > 0:
                instructions_num = self.get_formatted_steps(instruction[INFO][INST])
                for info in instructions_num:
                    pos_y += 20
                    name = info[0]
                    amount = info[1]
                    func_info = f'{name} : {amount}'
                    display_info(func_info, pos_x, pos_y)