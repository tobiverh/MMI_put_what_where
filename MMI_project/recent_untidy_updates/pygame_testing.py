import sys
import pygame
from MMI_project.recent_untidy_updates.quadrant_generation import init_quadrant_matrix as quads
from MMI_project.recent_untidy_updates.quadrant_generation import init_sub_quadrant_matrix as sub_quads
from MMI_project.recent_untidy_updates.quadrant_generation import get_sub_quadrant_center as quad_center

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
SHAPES = []
"""List of all drawable shapes.\n
`SHAPES[type_of_shape]` is a list of all quadrant positions of that type of shape"""

def next(list, elem=None):
    """Returns the next element from the given list. If no specific element is passed, the first element in the list is returned."""
    if elem:
        previous_index = list.index(elem)
        new_index = (previous_index + 1) % len(list)
    else:
        new_index = 0
    return list[new_index]
    
def next_color(color=None):
    """Returns the next color from the list of colors. If no argument is passed, the first color in the list is returned."""
    return next(COLORS, color)
    
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

def when_num_pressed(num, selecting, quadrant, sub_quadrant, shapes):
    """
    Handles the event of when a user presses a number button.
    - `num`: int - Number that was pressed
    - `selecting`: bool - True if selecting shape, False if de-selecting/releasing
    - `quadrant`: int - current chosen qudrant index
    - `sub_quadrant`: int - current chosen subquadrant index
    - `shapes`: [(quad, sub_quad)] - list of positions in the subquadrant-grid, where there currently exists shapes
    
    - returns `(text, quadrant, sub_quadrant, shapes)`, where text is the text to display to the screen, and the rest is for updating the indexes and the list of shapes.
    """
    if num > 3: # Invalid number
        text = "Only numbers 0-3 is valid"
    elif quadrant < 0: # Quadrant not chosen yet
        quadrant = num
        text = f"Quadrant number {num} is selected"
    elif sub_quadrant < 0: # Subquadrant not chosen yet
        sub_quadrant = num
        chosen_index_pair = (quadrant, sub_quadrant)
        if selecting: # Remove shape is selecting
            try:
                shapes.remove(chosen_index_pair)
                text = f"Removed shape from {(quadrant, sub_quadrant)}"
            except ValueError:
                text = f"{(quadrant, sub_quadrant)} does not contain the selected shape."
        else:   # Add shape if de-selecting
            shapes.append(chosen_index_pair)
            text = f"Added shape at {(quadrant, sub_quadrant)}"
        # Reset values for next action
        quadrant = -1
        sub_quadrant = -1
    
    return text, quadrant, sub_quadrant, shapes

def centered_square(rectangle, side_length):
    """Returns the Rect-object of a square, with the same center as the given rectangle.\n
    `side_length` decides the size of the square."""
    left_x, top_y, width, height = rectangle
    new_left_x = left_x + (width - side_length) / 2
    new_top_y = top_y + (height - side_length) / 2
    return new_left_x, new_top_y, side_length, side_length

def run(INIT_WIDTH=1300, INIT_HEIGHT=700, TEXT_HEIGHT_FRACTION=0.1, FONT_NAME = "Times New Roman"):
    # Initialize pygame and main screen ------------------------------------
    pygame.init()
    screen = pygame.display.set_mode((INIT_WIDTH,INIT_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Getting to know pygame!")
    # Initialize displayed text --------------------------------------------
    DISPLAYED_TEXT = "Hello World!"
    # Initialize shape sizes -----------------------------------------------
    SHAPE_SIZE_FACTOR = 0.9 #Size of the drawn shapes, as a fraction of their quadrants
    # Initialize quadrant indexes and boolean for selection/release --------
    QUAD_INDEX = -1
    SUBQUAD_INDEX = -1
    SELECTING = True
    # Initialize sets of shapes --------------------------------------------
    CIRCLES = [(0,3), (1,0)]
    SQUARES = [(2,1)]
    SHAPES.append(CIRCLES)
    SHAPES.append(SQUARES)
    SHAPE_NAMES = ['Circle', 'Square']
    SELECTED_SHAPE = 0 # Index to be used for SHAPES, SHAPE_COLORS or SHAPE_NAMES
    # Initialize colors ----------------------------------------------------
    IMAGE_BACKGROUND = YELLOW
    TEXT_BACKGROUND = GRAY
    TEXT_COLOR = BLACK
    SHAPE_COLORS = [BLUE, RED]

    while True:
        # Check for events ------------------------------------------------------        
        for event in pygame.event.get():
            # Quiting --------------------------------------------
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Changing colors ------------------------------------
            elif was_pressed('t', event):
                TEXT_BACKGROUND = next_color(TEXT_BACKGROUND)
            elif was_pressed('y', event):
                TEXT_COLOR = next_color(TEXT_COLOR)
            elif was_pressed('u', event):
                SHAPE_COLORS[SELECTED_SHAPE] = next_color(SHAPE_COLORS[SELECTED_SHAPE])
            elif was_pressed('i', event):
                IMAGE_BACKGROUND = next_color(IMAGE_BACKGROUND)
            # Shape selection ------------------------------------
            elif was_pressed('q', event):
                DISPLAYED_TEXT = f"Current selected shape is {SHAPE_NAMES[SELECTED_SHAPE]}"
            elif was_pressed('w', event):
                SELECTED_SHAPE = (SELECTED_SHAPE + 1) % len(SHAPES)
            # Set mode to Selecting / De-selecting ---------------
            elif was_pressed('s', event):
                SELECTING = True
            elif was_pressed('d', event):
                SELECTING = False
            # Change size of drawn shapes ------------------------
            elif was_pressed('+', event):
                SHAPE_SIZE_FACTOR += 0.01
            elif was_pressed('-', event):
                SHAPE_SIZE_FACTOR -= 0.01
            # Choose quadrants to add/remove shapes --------------
            elif event.type == pygame.KEYDOWN and event.unicode.isdigit():
                num = int(event.unicode)
                DISPLAYED_TEXT, QUAD_INDEX, SUBQUAD_INDEX, SHAPES[SELECTED_SHAPE] = when_num_pressed(num, SELECTING, QUAD_INDEX, SUBQUAD_INDEX, SHAPES[SELECTED_SHAPE])
        #------------------------------------------------------------------------
        
        # Update measures in case of resizing ----------------------
        WIDTH = screen.get_width()
        HEIGHT = screen.get_height()
        TEXT_HEIGHT = HEIGHT * TEXT_HEIGHT_FRACTION # Height of text field
        TEXT_FONT = pygame.font.SysFont(FONT_NAME, TEXT_HEIGHT.__floor__()) # Make font fit the height of text field
        # Resize image and text field
        image = pygame.Surface((WIDTH, HEIGHT - TEXT_HEIGHT))
        text_field = pygame.Surface((WIDTH, TEXT_HEIGHT))
        # Update size of shapes
        sub_quadrants = sub_quads(quads(image))
        _, _, quad_width, quad_height = sub_quadrants[0][0]
        MAX_SHAPE_SIZE = min(quad_width, quad_height) # Max shape size, so that shapes stay whithin their quadrant
        SHAPE_SIZE = MAX_SHAPE_SIZE * SHAPE_SIZE_FACTOR # Actual size of shapes

        # Draw image -----------------------------------------------
        image.fill(IMAGE_BACKGROUND)
        # Draw shapes onto image
        for x,y in CIRCLES:
            pygame.draw.circle(image, SHAPE_COLORS[SHAPES.index(CIRCLES)], quad_center(sub_quadrants[x][y]), SHAPE_SIZE/2)
        for x,y in SQUARES:
            pygame.draw.rect(image, SHAPE_COLORS[SHAPES.index(SQUARES)], centered_square(sub_quadrants[x][y], SHAPE_SIZE))

        # Draw text field -------------------------------------------
        text_field.fill(TEXT_BACKGROUND)
        # Write text to be displayed
        draw_text(DISPLAYED_TEXT, TEXT_FONT, TEXT_COLOR, text_field)

        # Add image and text onto screen, and update display --------
        screen.blit(image, (0,0))
        screen.blit(text_field, (0, HEIGHT - TEXT_HEIGHT))
        pygame.display.update()

if __name__ == "__main__":
    print("""
    Commands:
          q - print selected shape
          w - change selected shape
          
          t - change color of text background
          y - change color of text
          u - change color of selected shapes
          i - change color of image background

          s - set mode to 'select' (pick up/remove shapes)
          d - set mode to 'deselect' (release/add shapes)

          + - make shapes bigger
          - - make shapes smaller

          numbers 0-3 - select quadrants and subquadrants
    """)
    run()