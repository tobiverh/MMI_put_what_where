from MMI_project.audio_processing.implemented_recorder import Recorder
from MMI_project.audio_processing.implemented_speech_recognizer import SpeechRecognizer
import pygame

pygame.init()
pygame.display.init()
pygame.display.set_mode(list(pygame.display.get_desktop_sizes()[0]))

recorder = Recorder('audio_recording_test.wav')
recording = True

while recording:
    for event in pygame.event.get():

        # Handle space key being pressed down!
        if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == 'space':
            recorder.start_recording()

        # Handle space key being released!
        if event.type == pygame.KEYUP and pygame.key.name(event.key) == 'space':         
            recorder.finish_recording()                  
            recording = False
            break

        pygame.display.update()

recognizer = SpeechRecognizer(audio_file_path=recorder.audio_file_path)
recognizer.start_recognizing_audio()

recognizer.finish_recognizing_audio()
assert recognizer.has_recognized_message()
print(f"Recognized message: {recognizer.get_message()}")