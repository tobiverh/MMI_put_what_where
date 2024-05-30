import sys
import pygame
from MMI_project.audio_processing.recorder import Recorder
from MMI_project.audio_processing.speech_recognizer import SpeechRecognizer
from MMI_project.eye_tracking.eye_tracker import EyeTracker
from MMI_project.main_folder.useful_functions import *

def print_commands():
    print("""
    Welcome to 'Put What Where?'!
    Commands:
          check your (H)and for objects
          
          change color of (T)ext field
          change color of (F)ont
          change color of (I)mage background

          Arrow up/down : change shape of object in hand
          Arrow left/right : change color of object in hand

          0-3 - select position (NB: two numbers needed)
          or select position with your (E)ye gaze

          Go (B)ack one step in position selection
          (P)ick up object from chosen position to your hand
          (C)ollect object from chosen position to your hand (equivalent to '(P)ick up')
          (R)elease object from your hand to chosen position
          Put (N)ew object onto chosen position
          (D)elete object at chosen position

          - - make objects smaller
          + - make objects bigger
          z - make text smaller
          x - make text bigger

          'space' - hold down while performing speech command
          Possible speech commands: 
    """)
    print(ACTIONS)

def run(INIT_WIDTH=1300, INIT_HEIGHT=700, FONT_NAME = "Times New Roman"):
    # Initialize pygame and main screen ------------------------------------
    pygame.init()
    screen = pygame.display.set_mode((INIT_WIDTH,INIT_HEIGHT), pygame.RESIZABLE)
    resized = False
    pygame.display.set_caption("Put what where...?")
    # Initialize displayed text --------------------------------------------
    displayed_text = "Hello World!"
    # Initialize size factors ----------------------------------------------
    object_size_factor = 0.9 #Size of the drawn objects, compared to their quadrants
    text_height_factor = 0.1 #Size of text field compared to whole screen
    # Initialize indices for selecting quadrant ----------------------------
    current_position = (-1, -1)
    # Initialize different regions of screen, and text font ----------------
    image, text_field, font = get_measures(screen, text_height_factor, FONT_NAME)
    # Initialize set of objects --------------------------------------------
    objects_on_image = {
        (0,3): ('circle', YELLOW),
        (1,0): ('circle', RED),
        (2,1): ('square', BLUE),
        (3,3): ('square', GREEN)}
    object_in_hand = ()
    # Initialize colors ----------------------------------------------------
    image_background = BLACK
    text_background = GRAY
    font_color = BLACK
    # Initialize Recorder and SpeechRecognizer -----------------------------
    recorder = None
    speech_recognizer = None
    speech_input = '' # Recognized speech input
    # Initialize EyeTracker ------------------------------------------------
    eye_tracker = EyeTracker() # Initiate here for faster response later
    gaze_input = None # Tracked gaze input: [top-left, top-right, bottom-left, bottom-right] --> [0,1,2,3]

    ###################################### GAME LOOP ##########################################
    while True:
        # Check for events ------------------------------------------------------        
        for event in pygame.event.get():
            # Quiting --------------------------------------------
            if event.type == pygame.QUIT:
                eye_tracker.terminate()
                pygame.quit()
                sys.exit()
            # Handle resizing of the window ----------------------
            if event.type == pygame.VIDEORESIZE:
                resized = True
            # Choose quadrants to add/remove objects -------------
            # ...by pressing number buttons
            elif event.type == pygame.KEYDOWN and event.unicode.isdigit():
                number = int(event.unicode)
                current_position, displayed_text = select_quadrant(number, current_position)
            # ...with eye gaze
            elif was_pressed(pygame.K_e, event):
                eye_tracker.start_tracking() # Start tracking
                eye_tracker.finish_tracking()  # Make sure it finishes
                number = eye_tracker.get_quadrant()
                current_position, displayed_text = select_quadrant(number, current_position)
            # Actions --------------------------------------------
            elif was_pressed(pygame.K_b, event):
                current_position, displayed_text = undo_selection(current_position)
            elif was_pressed(pygame.K_p, event):
                objects_on_image, object_in_hand, displayed_text = action_at_position('pick up', current_position, objects_on_image, object_in_hand)
            elif was_pressed(pygame.K_c, event):
                objects_on_image, object_in_hand, displayed_text = action_at_position('collect', current_position, objects_on_image, object_in_hand)
            elif was_pressed(pygame.K_r, event):
                objects_on_image, object_in_hand, displayed_text = action_at_position('release', current_position, objects_on_image, object_in_hand)
            elif was_pressed(pygame.K_n, event):
                objects_on_image, object_in_hand, displayed_text = action_at_position('new object', current_position, objects_on_image, object_in_hand)
            elif was_pressed(pygame.K_d, event):
                objects_on_image, object_in_hand, displayed_text = action_at_position('delete', current_position, objects_on_image, object_in_hand)
            # Changing colors ------------------------------------
            elif was_pressed(pygame.K_t, event):
                text_background = next_color(text_background)
            elif was_pressed(pygame.K_f, event):
                font_color = next_color(font_color)
            elif was_pressed(pygame.K_i, event):
                image_background = next_color(image_background)
            # Checking hand --------------------------------------
            elif was_pressed(pygame.K_h, event):
                if object_in_hand:
                    shape, color = object_in_hand
                    displayed_text = f"Object in hand: A {get_color_name(color)} {shape}"
                else:
                    displayed_text = "No objects in hand"
            # Changing color/shape of object in hand -------------
            elif was_pressed(pygame.K_RIGHT, event):
                if object_in_hand:
                    shape, old_color = object_in_hand
                    new_color = next_color(old_color)
                    object_in_hand = (shape, new_color)
                    displayed_text = f"Made your {get_color_name(old_color)} {shape} {get_color_name(new_color)}!"
                else:
                    displayed_text = "No object in hand -> Can't change color"
            elif was_pressed(pygame.K_LEFT, event):
                if object_in_hand:
                    shape, old_color = object_in_hand
                    new_color = prev_color(old_color)
                    object_in_hand = (shape, new_color)
                    displayed_text = f"Made your {get_color_name(old_color)} {shape} {get_color_name(new_color)}!"
                else:
                    displayed_text = "No object in hand -> Can't change color"
            elif was_pressed(pygame.K_DOWN, event):
                if object_in_hand:
                    old_shape, color = object_in_hand
                    new_shape = next_shape(old_shape)
                    object_in_hand = (new_shape, color)
                    displayed_text = f"Made your {get_color_name(color)} {old_shape} a {new_shape}!"
                else:
                    displayed_text = "No object in hand -> Can't change shape"
            elif was_pressed(pygame.K_UP, event):
                if object_in_hand:
                    old_shape, color = object_in_hand
                    new_shape = prev_shape(old_shape)
                    object_in_hand = (new_shape, color)
                    displayed_text = f"Made your {get_color_name(color)} {old_shape} a {new_shape}!"
                else:
                    displayed_text = "No object in hand -> Can't change shape"
            # Change sizes ---------------------------------------
            elif was_pressed(pygame.K_PLUS, event):
                object_size_factor += 0.05
            elif was_pressed(pygame.K_MINUS, event):
                object_size_factor -= 0.05
            elif was_pressed(pygame.K_z, event):
                text_height_factor -= 0.01
                resized = True # We have to resize image and textfield before updating screen
            elif was_pressed(pygame.K_x, event):
                text_height_factor += 0.01
                resized = True # We have to resize image and textfield before updating screen
            # Record multimodal input ----------------------------
            elif was_pressed(pygame.K_SPACE, event):
                recorder = Recorder('speech_input.wav')
                recorder.start_recording()
                displayed_text = "Recording..."
                # Notice where user is looking
                eye_tracker.start_tracking()
            # Process multimodal input ---------------------------
            elif was_released(pygame.K_SPACE, event):
                # Finish audio recording
                recorder.finish_recording()
                # Attach SpeechRecognizer to the recorded audio file
                speech_recognizer = SpeechRecognizer(recorder.audio_file_path)
                speech_recognizer.start_recognizing_audio()
                # Finish processing input
                eye_tracker.finish_tracking()
                speech_recognizer.finish_recognizing_audio()
                # Store input command
                gaze_input = eye_tracker.get_quadrant()
                speech_input = speech_recognizer.get_message()
                # Display the recognized message to the user
                displayed_text = f"Recognized: {speech_input}" # (will be overwritten if input was a valid action)
        # Event check done ------------------------------------------------------

        # Check for modal commands (speech/gaze) -------------------
        if speech_input in ACTIONS:
            # Update selected position
            if speech_input == 'select':
                current_position, displayed_text = select_quadrant(gaze_input, current_position)
            elif speech_input == 'go back':
                current_position, displayed_text = undo_selection(current_position)
            # All other actions requires a specified position
            elif current_position in POSITIONS:
                objects_on_image, object_in_hand, displayed_text = action_at_position(speech_input, current_position, objects_on_image, object_in_hand)
            else:
                displayed_text = f"You can't {speech_input} with no position" 
        speech_input = '' #Reset speech_input

        # Update measures in case of resizing ----------------------
        if resized:
            image, text_field, font = get_measures(screen, text_height_factor, FONT_NAME)
            resized = False #Reset boolean

        # Draw image -----------------------------------------------
        image.fill(image_background)
        # Draw objects onto image
        image = draw_objects(objects_on_image, object_size_factor, image)
        # Highlight chosen quadrant in image
        image = draw_quadrant(current_position, image, color=next_color(image_background))

        # Draw text field -------------------------------------------
        text_field.fill(text_background)
        # Write text to be displayed
        draw_text(displayed_text, font, font_color, text_field)

        # Add image and text onto screen, and update display --------
        screen.blit(image, (0,0))
        screen.blit(text_field, (0, screen.get_height() * (1 - text_height_factor)))
        pygame.display.update()

if __name__ == "__main__":
    print_commands()
    run()