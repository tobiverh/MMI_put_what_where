from MMI_project.audio_processing.audio_meta_classes import MetaRecorder
from MMI_project.audio_processing.audio_recorder2 import AudioRecorder
import time
import os
import sched
from threading import Thread


class Recorder(MetaRecorder):
    def __init__(self, audio_filename):
        """
        Initializes the recorder, and the thread it will be working in.\n
        - `audio_filename`: Name of output-file. Should include suffix `.wav`. The output file will be written to the project's `audio_files` folder.
        """
        # Define path of output audio file
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.abspath(os.path.join(path, os.pardir, 'audio_files', audio_filename))
        self.audio_file_path = path
        # Initialize recorder
        self.recorder = AudioRecorder(filename=self.audio_file_path)
        # Initialize thread to process recording 
        self.task = sched.scheduler(time.time, time.sleep) # Start scheduler
        self.recorder.set_task(self.task)
        self.task.enter(0.1, 1, self.recorder.recorder,  # Enter the given task
                   (self.recorder.is_started, self.recorder.p_thang, self.recorder.stream_in, self.recorder.frame_list))
        self.thread = None

    def start_recording(self):  
        self.thread = Thread(target=self.task.run, args=())
        self.thread.daemon = True
        self.thread.start()
        self.recorder.listener.on_press()

    def finish_recording(self):
        self.recorder.listener.on_release()
        self.thread.join()

    def is_listening(self):
        if self.recorder.is_started:
            return self.thread.is_alive() # True if recorder was started AND thread is still alive
        else:
            return False    # Recorder was never started

    def has_audio(self):
        return os.path.exists(self.audio_file_path)

    def get_audio(self):
        """Returns the filename of the stored audio clip."""
        assert self.has_audio(), "Couldn't get audio because the audio file didn't exist."
        return self.audio_file_path

    # def clear(self):
    #     """Removes existing file (if there is one) from the recorder's output path."""
    #     self.recorder.listener = None   # Can't remove file while the listener is writing to it
    #     os.remove(self.audio_file_path)
    #     self.recorder.listener = self.recorder.create_listener() # Create new listener

def test():
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.abspath(os.path.join(path, os.pardir, 'audio_files', 'recorder_test.wav'))
    print(f"""
    This should be the path of the recorder's output file:
    --------------------
    {path}
    --------------------
    """)

if __name__ == "__main__":
    test()