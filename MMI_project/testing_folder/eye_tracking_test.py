import sys
import pygame
from MMI_project.main_folder.pygame_program import centered_square
from MMI_project.recent_untidy_updates.quadrant_generation import init_quadrant_matrix as quads
from MMI_project.recent_untidy_updates.quadrant_generation import init_sub_quadrant_matrix as sub_quads
from MMI_project.recent_untidy_updates.quadrant_generation import get_sub_quadrant_center as quad_center
from MMI_project.audio_processing.implemented_recorder import Recorder
from MMI_project.audio_processing.implemented_speech_recognizer import SpeechRecognizer
from MMI_project.eye_tracking.implemented_eye_classes import EyeTracker

BLACK = (0,0,0)
GRAY = (100,100,100)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
MAGENTA = (255,0,255)

COLORS = [BLACK, GRAY, WHITE, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]
"""List of all predefined colors. Contains black, gray, white, as well as all primary and secondary colors."""
SHAPES = ['circle', 'square']
"""List of all drawable shapes. Contains `'circle'` and `'square'`."""
POSITIONS = [(x,y) for x in range(4) for y in range(4)]
"""All valid positions in the subquadrant grid. Tuples (x,y), where x and y range from 0 to 3."""
    
def draw_text(text: str, font: pygame.font.Font, color: tuple[int], text_surface: pygame.Surface) -> pygame.Rect:
    """Draws text in the center of the given surface."""
    # Render image of text to be displayed
    img = font.render(text, True, color)
    # Position the text image in the center of the given surface
    pos = ((text_surface.get_width() - img.get_width()) / 2, 
            (text_surface.get_height() - img.get_height()) / 2)
    # Add image to surface
    return text_surface.blit(img, pos)

def was_pressed(button, event: pygame.event.Event) -> bool:
    """Checks if the given button was pressed"""
    return event.type == pygame.KEYDOWN and pygame.key.name(event.key) == button

def draw_objects(objects_to_draw: dict[tuple[int], list[str, tuple[int]]], object_size_factor: float, image: pygame.Surface) -> pygame.Surface:
    # Find positions and size of subquadrants
    sub_quadrants = sub_quads(quads(image))
    _, _, quad_width, quad_height = sub_quadrants[0][0] # Sample size of subquadrants
    # Define size of objects
    max_object_size = min(quad_width, quad_height) # Max object size, so that objects stay whithin their quadrant
    object_size = max_object_size * object_size_factor # Actual size of objects
    
    for pos, object in objects_to_draw.items():
            x,y = pos
            shape, color = object
            assert shape in SHAPES, "Undefined shape"
            assert color in COLORS, "Undefined color"
            assert pos in POSITIONS, "Undefined position"
            if shape == "circle":
                pygame.draw.circle(image, color, quad_center(sub_quadrants[x][y]), object_size/2)
            elif shape == "square":
                pygame.draw.rect(image, color, centered_square(sub_quadrants[x][y], object_size))
            else:
                assert False, f"Missing implementation for drawing a {shape}!"
    return image

def run(INIT_WIDTH=1300, INIT_HEIGHT=700, FONT_NAME = "Times New Roman"):
    # Initialize pygame and main screen ------------------------------------
    pygame.init()
    screen = pygame.display.set_mode((INIT_WIDTH,INIT_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("EyeTracker test")
    # Initialize displayed text --------------------------------------------
    displayed_text = "Press space, and look at the circle until it moves."
    # Initialize object sizes ----------------------------------------------
    object_size_factor = 0.2 #Size of the drawn objects, compared to their quadrants
    text_height_factor = 0.1 #Size of text field compared to whole screen
    # Initialize set of objects --------------------------------------------
    objects_on_image = {(0,0): ('circle', YELLOW)}
    quadrants_to_test = [(0,0), (1,1), (2,2), (3,3), # Towards the corners of the screen
                         (0,3), (1,2), (2,1), (3,0)] # Towards the middle of the screen
    current_quadrant = 0
    centered = False
    count_edge_trials = 0
    count_edge_success = 0
    edge_success_rate = 0
    count_center_trials = 0
    count_center_success = 0
    center_success_rate = 0
    # Initialize EyeTracker ------------------------------------------------
    eye_tracker = EyeTracker()
    gaze_input = -1

    # --- GAME LOOP --- GAME LOOP --- GAME LOOP --- GAME LOOP --- GAME LOOP --- GAME LOOP --- #
    while True:
        # Check for events ------------------------------------------------------        
        for event in pygame.event.get():
            # Quiting --------------------------------------------
            if event.type == pygame.QUIT:
                pygame.quit()
                print(  f"{'Edge samples:':<20} {count_edge_trials}",
                        f"{'Hits:':<20} {count_edge_success}",
                        f"{'Misses:':<20} {count_edge_trials - count_edge_success}",
                        f"{'Edge success rate:':<20} {edge_success_rate:.2%}",
                        "",
                        f"{'Center samples:':<20} {count_center_trials}",
                        f"{'Hits:':<20} {count_center_success}",
                        f"{'Misses:':<20} {count_center_trials - count_center_success}",
                        f"{'Center success rate:':<20} {center_success_rate:.2%}",
                        "",
                        f"{'Total samples:':<20} {count_center_trials + count_edge_trials}",
                        f"{'Total hits:':<20} {count_edge_success + count_center_success}",
                        f"{'Total misses:':<20} {(count_center_trials + count_edge_trials) - (count_edge_success+count_center_success)}",
                        f"{'Total success rate:':<20} {(count_edge_success + count_center_success) / (count_edge_trials + count_center_trials):.2%}",
                        sep = '\n')
                sys.exit()
            # Choose quadrants to add/remove objects --------------
            # ...with eye gaze
            elif was_pressed('space', event):
                eye_tracker.start_tracking()
                eye_tracker.finish_tracking()
                gaze_input = eye_tracker.get_quadrant()
                if centered:
                    count_center_trials += 1
                    if gaze_input == quadrants_to_test[current_quadrant][0]:
                        count_center_success += 1
                    if count_center_trials > 0:
                        center_success_rate = count_center_success / count_center_trials
                else:
                    count_edge_trials += 1
                    if gaze_input == quadrants_to_test[current_quadrant][0]:
                        count_edge_success += 1
                    if count_edge_trials > 0:
                        edge_success_rate = count_edge_success / count_edge_trials
                current_quadrant = (current_quadrant + 1) % len(quadrants_to_test)
                centered = True if 4 <= current_quadrant < 8 else False
                objects_on_image = {quadrants_to_test[current_quadrant]: ('circle', YELLOW)}
                displayed_text = f"Corners: {edge_success_rate:.1%}, Center: {center_success_rate:.1%}"

        #------------------------------------------------------------------------

        # -----------------------------------------------------------------------
        # Update measures in case of resizing ----------------------
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        text_height = screen_height * text_height_factor # Height of text field
        font = pygame.font.SysFont(FONT_NAME, text_height.__floor__()) # Make font fit the height of text field
        # Resize image and text field
        image = pygame.Surface((screen_width, screen_height - text_height))
        text_field = pygame.Surface((screen_width, text_height))

        # Draw image -----------------------------------------------
        image.fill(BLACK)
        # Draw objects onto image
        image = draw_objects(objects_on_image, object_size_factor, image)

        # Draw text field -------------------------------------------
        text_field.fill(GRAY)
        # Write text to be displayed
        draw_text(displayed_text, font, BLACK, text_field)

        # Add image and text onto screen, and update display --------
        screen.blit(image, (0,0))
        screen.blit(text_field, (0, screen_height - text_height))
        pygame.display.update()

if __name__ == "__main__":
    run()