from MMI_project.audio_processing.audio_meta_classes import MetaRecorder
from MMI_project.audio_processing.audio_recorder2 import AudioRecorder
import time
import os
import sched
from threading import Thread


class Recorder(MetaRecorder):
    def __init__(self, audio_filename):
        # Define path of output audio file
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.abspath(os.path.join(path, os.pardir, 'audio_files', audio_filename))
        self.audio_filename = path
        # Initialize recorder
        self.recorder = AudioRecorder(filename=self.audio_filename)
        # Initialize thread to process recording 
        task = sched.scheduler(time.time, time.sleep) # Start scheduler
        self.recorder.set_task(task)
        task.enter(0.1, 1, self.recorder.recorder,  # Enter the given task
                   (self.recorder.is_started, self.recorder.p_thang, self.recorder.stream_in, self.recorder.frame_list))
        self.thread = Thread(target=task.run, args=())
        self.thread.daemon = True

    def start_listening(self):
        self.thread.start()
        self.recorder.listener.on_press()

    def stop_listening(self):
        self.recorder.listener.on_release()
        while self.is_listening() or not self.has_audio():
            time.sleep(0.05)    # Waiting for recording to finish

    def is_listening(self):
        return self.recorder.is_started

    def has_audio(self):
        return os.path.exists(self.audio_filename)

    def get_audio(self):
        """Returns the filename of the stored audio clip."""
        assert self.has_audio(), "Couldn't get audio because the audio file didn't exist."
        return self.audio_filename

    def clear(self):
        """Removes existing file (if there is one) from the recorder's output path."""
        self.recorder.listener = None
        os.remove(self.audio_filename)
        self.recorder.listener = self.recorder.create_listener()


#TODO: Remove when done testing:
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.abspath(os.path.join(path, os.pardir, 'audio_files', 'output.wav'))
print(f"""
This should be the path of the recorder's output file:
--------------------
{path}
--------------------
""")