from time_wait import regular_interval_tick_wait
import pygame
from config import FULLSCREEN, DELAY
from screen import Screen
from cell import *
from instruction import Instructions_manager

"""
------------- RESTRUCTURING -------------
TODO add event parser class if game loop gets too long
TODO make checking for event.key == --- into a switch statement
------------- ------------- -------------
------------- USER -------------
TODO make lable showing it record_instruction is recording or not
TODO show the instruction list being created on the left of the screen where
     current_board info goes
TODO when user hit the create button must check length of instruction, if 0 then
     dont create a new instruction, for now the current cell size will always be
     added to the new Instruction. For now we will have to generate a name for the
     instruction added. Maybe - f'{tile_size}_{count}'
TODO Be able to create instructions 
TODO Be able to delete instructions
------------- ---- -------------
"""

record_instruction = False
show_board_info = False
show_key_binds = False
done = False
perform = False
perform_index = 0
func_index = 1
screen = Screen(1600,900, FULLSCREEN)
manager = Instructions_manager()

screen.display()
generate_cells(screen)
draw(screen.surface)   

#helper functions to make game loop look cleaner
def toggle_perform(screen):
    global perform, perform_index
    perform = not perform
    perform_index = 0
    manager.handle_optional_resize(screen)
def toggle_show_board():
    global show_board_info
    show_board_info = not show_board_info
    draw(screen.surface)
def toggle_show_key():
    global show_key_binds
    show_key_binds = not show_key_binds
    draw(screen.surface)
def toggle_record_instructions():
    global record_instruction
    record_instruction = not record_instruction
    draw(screen.surface)
def handle_func_change(handler):
    global func_index
    func_index = handler(func_index)
    draw(screen.surface)
def handle_full_screen(screen):
    screen.toggle_full_screen()
    generate_cells(screen)
def handle_perform(screen):
    global perform, perform_index
    if perform:
        if regular_interval_tick_wait(DELAY):
            perform = manager.perform(perform_index, screen)
            perform_index += 1


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: not done
        if event.type == pygame.MOUSEBUTTONDOWN: handle_mouse_click(screen.surface)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: not done
            if event.key == pygame.K_SPACE: id_func[func_index](screen.surface)
            if event.key == pygame.K_UP: handle_cell_size_increase(5, screen)
            if event.key == pygame.K_DOWN: handle_cell_size_decrease(5, screen)
            if event.key == pygame.K_LEFT: manager.decrease_index(screen.surface)
            if event.key == pygame.K_RIGHT: manager.increase_index(screen.surface)
            if event.key == pygame.K_n: toggle_record_instructions()
            if event.key == pygame.K_s: toggle_show_board()
            if event.key == pygame.K_k: toggle_show_key()
            if event.key == pygame.K_COMMA: handle_func_change(handle_func_prev)
            if event.key == pygame.K_PERIOD: handle_func_change(handle_func_next)
            if event.key == pygame.K_f: handle_full_screen(screen)
            if event.key == pygame.K_TAB and not perform: toggle_perform(screen)
    
    handle_perform(screen)
    display_current_board_information(show_board_info and not record_instruction)
    display_current_instruction_info(manager.get_current_instruction(), screen, show_board_info)
    display_key_binds(show_key_binds, screen)
    display_current_command(screen, func_index)
    pygame.display.update()
pygame.quit()