# Put What Where?
This is our project for the H2024 course *Multimodal User Interfaces*, given at the University of Fribourg.

The project is an adaptation of the classic *Put That There*, where gestures have been replaced with eye gaze.
If you want to read a more detailed description of our project, please refer to the [report](Final_Report.pdf).

Watch our demo video by clicking the image below:

[![Watch demo video](https://github.com/tobiverh/MMI_put_what_where/assets/126837440/0ffa956d-d09d-498c-9a3f-dfb9087542ad)](https://youtu.be/Y2lKr7QXI-k)


## Install project
To install the project, follow these instructions:
1. Clone this repository to your computer (or pull, if you already have cloned the project)
2. Make sure to have Python (version >=3.10) installed properly
3. Open a terminal
4. Navigate your directory to `...\MMI_put_what_where`
5. Run `pip install -e .`
   - The `-e` flag installs the project in editor mode, so you can change the source code (within the `MMI_project` folder)
   without having to re-install. If you don't intend to edit anything, running `pip install .` should be sufficient.
   - `.` refers to your current working directory.

You should now have the project installed.

## Running
1. Open a terminal
2. Navigate your directory to `...\MMI_put_what_where`
3. Run `python .\MMI_project\main_folder\main.py`

When performing step 3, a pygame-window should pop up, looking like this:

[![Watch demo video](https://github.com/tobiverh/MMI_put_what_where/assets/126837440/0ffa956d-d09d-498c-9a3f-dfb9087542ad)](https://youtu.be/Y2lKr7QXI-k)

Additionaly, your terminal should print a list of all the things you can do in the pygame program.
However, if you are a new user, here is a list of things that could be useful to know:
- When performing speech commands: Always give a moment of silence before and after performing the command, while pressing the space-button. This significantly improves the `SpeechRecognizer`'s performance.
- When giving eye gaze input: The closer to the middle of the screen you look, the worse the performance will be. Therefore, we recommend to look at the far corners of your screen to select a quadrant. The diagram below shows the accuracy of the `EyeTracker`, depending on where you are looking.
- Check out the demo video for examples of use! (See top of this README)

![eye_tracking_results](https://github.com/tobiverh/MMI_put_what_where/assets/126837440/04598f20-5ec0-4f85-a175-dcb5f22a5de3)
