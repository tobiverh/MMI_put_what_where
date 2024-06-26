import pygame

BLACK = (0,0,0)
GRAY = (150,150,150)
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
ACTIONS = ['select', 'go back', 'pick up', 'collect', 'release', 'new object', 'delete']
"""All performable actions, either for navigating to a specific position in the image, or making an action in the current position."""
POSITIONS = [(x,y) for x in range(4) for y in range(4)]
"""All valid positions in the subquadrant grid. Tuples (x,y), where x and y range from 0 to 3."""

def get_color_name(color):
    for name, value in globals().items():
        if value == color:
            return name.lower()
    return 'unknown color'

def next(list, elem=None):
    """Returns the next element from the given list. If no specific element is passed, the first element in the list is returned."""
    if elem:
        previous_index = list.index(elem)
        new_index = (previous_index + 1) % len(list)
    else:
        new_index = 0
    return list[new_index]

def prev(list, elem=None):
    """Returns the previous element from the given list. If no specific element is passed, the last element in the list is returned."""
    if elem:
        elem_index = list.index(elem)
        prev_index = (elem_index - 1) % len(list)
    else:
        prev_index = -1
    return list[prev_index]
    
def next_color(color=None):
    """Returns the next color from the list of colors. If no argument is passed, the first color in the list is returned."""
    return next(COLORS, color)

def prev_color(color=None):
    """Returns the previous color from the list of colors. If no argument is passed, the last color in the list is returned."""
    return prev(COLORS, color)

def next_shape(shape=None):
    """Returns the next shape from the list of shapes. If no argument is passed, the first shape in the list is returned."""
    return next(SHAPES, shape)

def prev_shape(shape=None):
    """Returns the previous shape from the list of shapes. If no argument is passed, the last shape in the list is returned."""
    return prev(SHAPES, shape)
    
def draw_text(text: str, font: pygame.font.Font, color: tuple[int], text_surface: pygame.Surface) -> pygame.Rect:
    """Draws text in the center of the given surface."""
    # Render image of text to be displayed
    img = font.render(text, True, color)
    # Position the text image in the center of the given surface
    pos = ((text_surface.get_width() - img.get_width()) / 2, 
            (text_surface.get_height() - img.get_height()) / 2)
    # Add image to surface
    return text_surface.blit(img, pos)

def get_measures(screen: pygame.Surface, text_height_factor: float, font_name: str) -> tuple[pygame.Surface, pygame.Surface, pygame.font.Font]:
    """
    Updates the sizes of the `image`, the `text_field`, and the text `font`.\n
    They are all adapted to fit the size of the given `screen`, and returned in the order above.
    """
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    text_height = screen_height * text_height_factor # Height of text field
    font = pygame.font.SysFont(font_name, text_height.__floor__()) # Make font fit the height of text field
    # Resize image and text field
    image = pygame.Surface((screen_width, screen_height - text_height))
    text_field = pygame.Surface((screen_width, text_height))
    return image, text_field, font

def was_pressed(button: int, event: pygame.event.Event) -> bool:
    """Checks if the given button was pressed"""
    return event.type == pygame.KEYDOWN and event.key == button

def was_released(button, event: pygame.event.Event) -> bool:
    """Checks if the given button was released"""
    return event.type == pygame.KEYUP and event.key == button

def quads(screen):
    """
    This divides the provided screen into 4 equal parts in the following order: Upper-left, Upper-right, Lower-left,
    Lower-right
    :param screen: display object with get_width() and get_height() calls available
    :return: list of tuples of pygame rectangle requirements (left_x, top_y, width, height) in the following order:
           @index 0: left, up, 1: right, up, 2: left, down, 3: right, down
    """
    return [(0, 0, screen.get_width()/2, screen.get_height()/2),  # left, up
            (screen.get_width() / 2, 0, screen.get_width() / 2, screen.get_height() / 2),  # right, up
            (0, screen.get_height()/2, screen.get_width()/2, screen.get_height()/2),  # left, down
            (screen.get_width()/2, screen.get_height()/2, screen.get_width()/2, screen.get_height()/2)  # right, down
           ]  # 0: left, up, 1: right, up, 2: left, down, 3: right, down

def sub_quads(quadrants):
    """
    This iteratively subdivides the provided quadrants into 4 equal parts in the following order: Upper-left,
    Upper-right, Lower-left, Lower-right
    :param quadrants: list of tuples with pygame rectangle requirements (left_x, top_y, width, height)
    :return: 2D list of tuples of pygame rectangle requirements (left_x, top_y, width, height) in the following order:
           @index 0: left, up, 1: right, up, 2: left, down, 3: right, down
    """
    sub_quads = []
    for left, top, width, height in quadrants:
        top_left = (left, top, width / 2, height / 2)
        top_right = (left + width / 2, top, width / 2, height / 2)
        bottom_left = (left, top + height / 2, width / 2, height / 2)
        bottom_right = (left + width / 2, top + height / 2, width / 2, height / 2)
        sub_quads.append(
            [top_left, top_right, bottom_left, bottom_right]
        )
    return sub_quads

def quad_center(rectangle):
    """
    Function unpacks contents of the parameters and returns the center of the object
    :param rectangle: pygame rectangle with requirements (left_x, top_y, width, height)
    :return: tuple like: center_x, center_y
    """
    left, top, width, height = rectangle
    return left + width/2, top + height/2

def select_quadrant(num: int, position: tuple[int]):
    """
    Takes a numeric input, and changes the position accordingly.\n
    Returns `(position, text)` - The updated position, together with a text to display to user
    """
    quad, sub_quad = position
    if num > 3:
        text = "Only numbers 0-3 is valid"
    elif quad < 0: # Quadrant not selected yet
        quad = num
        text = f"Quadrant {quad} selected"
    elif sub_quad < 0: # Subquadrant not selected yet
        sub_quad = num
        text = f"Subquadrant {(quad, sub_quad)} selected"
    else: # Both are selected, so we should reset to select a new position
        quad = num
        sub_quad = -1
        text = f"Quadrant {quad} selected"

    # Update position
    position = (quad, sub_quad)
    return position, text

def undo_selection(position: tuple[int]):
    """
    Removes the last step of selection from a position. 
    That is, if the user only have selected a quadrant, this is reset to -1.
    If the user have selected both a quadrant and a subquadrant, only the ladder is reset.
    """
    quad, sub_quad = position

    if quad < 0: # Quadrant not selected yet
        text = f"No selection to undo"
    elif sub_quad < 0: # Subquadrant not selected yet
        quad = -1
        text = f"Undid quadrant selection"
    else: # Both are selected, so we should reset subquadrant
        sub_quad = -1
        text = f"Quadrant {quad} selected"
    
    #Update position
    position = (quad, sub_quad)
    return position, text

def action_at_position(action: str, position: tuple[int], objects_on_image: dict, object_in_hand: tuple[str, tuple[int]], new_object: tuple[str, tuple[int]] = ('circle', YELLOW)):
    """
    Performs an action at the given position in the image. Updates `objects_on_image`, and `object_in_hand` accordingly.
    \n
    `new_object` defines what kind of object should be added with the action "new object". Default is a yellow circle.
    \n
    Returns `(objects_on_image, object_in_hand, text)` with updated values after the action is performed, where text is supposed to be displayed to user.
    """
    object_at_position = position in objects_on_image.keys()

    if action not in ACTIONS:
        text = "You tried to perform a non-defined action."
    elif position not in POSITIONS:
        text = f"Can't {action} without a position"
    elif action == 'pick up' or action == 'collect':
        if object_in_hand:
            text = "Can't pick up because your hand is full"
        elif not object_at_position:
            text = f"No object to pick up at {position}"
        else:
            object_in_hand = objects_on_image.pop(position)
            shape, color = object_in_hand
            text = f"Picked up the {get_color_name(color)} {shape} from {position}"
    elif action == 'release':
        if not object_in_hand:
            text = "You have no object to release."
        elif object_at_position:
            text = f"Can't release. {position} is occupied"
        else:
            shape, color = object_in_hand
            objects_on_image[position] = object_in_hand
            object_in_hand = None
            text = f"Released the {get_color_name(color)} {shape} at {position}"
    elif action == 'new object':
        if object_at_position:
            text = f"Can't put anything here. {position} is occupied"
        else:
            objects_on_image[position] = new_object
            shape, color = new_object
            text = f"Put a {get_color_name(color)} {shape} at {position}"
    elif action == 'delete':
        if not object_at_position:
            text = f"No object to delete at {position}"
        else:
            deleted_object = objects_on_image.pop(position)
            shape, color = deleted_object
            text = f"Deleted {get_color_name(color)} {shape} from {position}"
    else:
        text = f"The action '{action}' isn't implemented yet."
    return objects_on_image, object_in_hand, text

def draw_quadrant(position: tuple[int], image: pygame.Surface, color: tuple[int] = WHITE, alpha_value : int = 50) -> pygame.Surface:
    """
    Draws the chosen quadrant onto the image.
    - `quad_index`: int - Chosen index for first-layer quadrant
    - `subquad_index`: int - Chosen index for subquadrant
    - `image`: pygame.Surface - Image to draw the chosen quadrant onto
    - `color`: tuple[int] - Color, with which to highlight the quadrant
    - `alpha_value` : int = 50 - Transparency of the drawn quadrant
    \n
    Returns:
    - The updated `image`, after the chosen quadrant has been highlighted
    """
    quadrants = quads(image)
    sub_quadrants = sub_quads(quadrants)
    quad_index, subquad_index = position
    chosen_quadrant = None # The quadrant corresponding to the given indices
    if quad_index >= 0:
        if subquad_index >= 0:
            chosen_quadrant = sub_quadrants[quad_index][subquad_index]
        else:
            chosen_quadrant = quadrants[quad_index]
    if chosen_quadrant:    
        left_x, top_y, width, height = chosen_quadrant
        quad_surf = pygame.Surface((width, height))
        quad_surf.set_alpha(alpha_value)
        quad_surf.fill(color)
        image.blit(quad_surf, (left_x, top_y))
    return image

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

def centered_square(rectangle, side_length):
    """Returns the Rect-object of a square, with the same center as the given rectangle.\n
    `side_length` decides the size of the square."""
    left_x, top_y, width, height = rectangle
    new_left_x = left_x + (width - side_length) / 2
    new_top_y = top_y + (height - side_length) / 2
    return new_left_x, new_top_y, side_length, side_length
