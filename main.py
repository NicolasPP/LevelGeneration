from time_wait import regular_interval_tick_wait
import pygame
from screen import Screen
from cell import *
from instruction_manager import Instructions_manager
from generator_functions import func_manager, func_id, id_func
"""
------------- RESTRUCTURING -------------
TODO Make a dict with all repeated rendered things eg. function name
     instruction name.
------------- ------------- -------------
"""
show_board_info = False
show_key_binds = False
show_territories = False
done = False
screen = Screen(1600,900, FULLSCREEN)
manager = Instructions_manager(id_func, screen)

screen.display()
generate_cells(screen)
Cell.draw_all()   

#helper functions to make game loop look cleaner
def toggle_show_territories():
    global show_territories
    show_territories = not show_territories
    Cell.draw_all()
def toggle_show_board():
    global show_board_info
    show_board_info = not show_board_info
    Cell.draw_all()


def toggle_show_key():
    global show_key_binds
    show_key_binds = not show_key_binds
    Cell.draw_all()
def handle_full_screen():
    screen.toggle_full_screen()
    generate_cells(screen)
def handle_func_perform():
    func_name = func_manager.get_current_func_name()
    id_func[func_name](screen)
    manager.add_step(func_name)    
def display_GUI_info():
    manager.show_new_instruction(show_board_info)
    manager.show_current_instruction(screen, show_board_info)
    display_key_binds(show_key_binds, screen)
    func_manager.display_current_command(screen)
def handle_mouse_click():
    if manager.show_del_alert:
        manager.handle_del_mouse_click(pygame.mouse.get_pos())


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True
        if event.type == pygame.MOUSEBUTTONDOWN: handle_mouse_click()
        if event.type == pygame.KEYDOWN and not manager.show_del_alert:
            if event.key == pygame.K_ESCAPE: done = True
            if event.key == pygame.K_SPACE: handle_func_perform()
            if event.key == pygame.K_UP: handle_cell_size_increase(5, screen)
            if event.key == pygame.K_DOWN: handle_cell_size_decrease(5, screen)
            if event.key == pygame.K_LEFT: manager.decrease_index()
            if event.key == pygame.K_RIGHT: manager.increase_index()
            if event.key == pygame.K_COMMA: func_manager.handle_index_decrease()
            if event.key == pygame.K_PERIOD: func_manager.handle_index_increase()
            if event.key == pygame.K_TAB and not manager.perform: manager.toggle_perform(screen)
            if event.key == pygame.K_s: toggle_show_board()
            if event.key == pygame.K_k: toggle_show_key()
            if event.key == pygame.K_f: handle_full_screen()
            if event.key == pygame.K_m: toggle_show_territories()
            if event.key == pygame.K_c: manager.create_new_instruction()
            if event.key == pygame.K_p: manager.toggle_show_delete()
    
    manager.handle_perform(screen)
    manager.display_del_alert(screen)
    display_GUI_info()
    display_territories(screen, show_territories)
    pygame.display.flip()
pygame.quit()