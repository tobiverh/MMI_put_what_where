from implemented_classes import Recorder, SpeechRecognizer
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
            recorder.start_listening()

        # Handle space key being released!
        if event.type == pygame.KEYUP and pygame.key.name(event.key) == 'space':         
            recorder.stop_listening()                  
            recording = False
            break

        pygame.display.update()

recognizer = SpeechRecognizer(audio_filename=recorder.audio_filename)
recognizer.start_recognizing_audio()

recognizer.stop_recognizing_audio()
assert recognizer.has_recognized_message()
print(f"Recognized message: {recognizer.get_message()}")