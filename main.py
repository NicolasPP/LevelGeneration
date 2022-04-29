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
------------- MENU -------------
TODO Make menu
TODO Be able show key bindings
TODO Be able to create instructions in the menu
TODO Be able to save instructions
TODO Be able to delete instructions
------------- ---- -------------
"""

show_board_info = False
show_key_binds = False
done = False
perform = False
perform_index = 0
screen = Screen(1600,900, FULLSCREEN)
screen.display()
instruction_manager = Instructions_manager()

generate_cells(screen)
draw(screen.surface)   

func_index = 1
        
while not done:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_click(screen.surface)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                func = id_func[func_index]
                func(screen.surface)
            if event.key == pygame.K_n:
                func_index = handle_func_prev(func_index)
                draw(screen.surface)
            if event.key == pygame.K_m:
                func_index = handle_func_next(func_index)
                draw(screen.surface)
            if event.key == pygame.K_f:
                screen.toggle_full_screen()
                generate_cells(screen)
            if event.key == pygame.K_TAB and not perform:
                perform = not perform
                perform_index = 0
                instruction_manager.handle_optional_resize(screen)
            if event.key == pygame.K_UP:
                handle_cell_size_increase(5, screen)
                generate_cells(screen)
            if event.key == pygame.K_DOWN:
                handle_cell_size_decrease(5)
                generate_cells(screen)
            if event.key == pygame.K_LEFT:
                instruction_manager.decrease_index()
                draw(screen.surface)
            if event.key == pygame.K_RIGHT:
                instruction_manager.increase_index()
                draw(screen.surface)
            if event.key == pygame.K_s:
                show_board_info = not show_board_info
                draw(screen.surface)
            if event.key == pygame.K_k:
                show_key_binds = not show_key_binds
                draw(screen.surface)
    if perform:
        if regular_interval_tick_wait(DELAY):
            perform = instruction_manager.perform(perform_index, screen)
            perform_index += 1
            
    display_current_board_information(show_board_info)
    display_current_instruction_info(instruction_manager.get_current_instruction(), screen, show_board_info)
    display_key_binds(show_key_binds)
    display_current_command(screen, func_index)
    pygame.display.update()
    

        