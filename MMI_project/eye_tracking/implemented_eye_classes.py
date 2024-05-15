from MMI_project.eye_tracking.eye_meta_classes import MetaEyeTracker


class PositionTracker(MetaEyeTracker):

    def __init__(self):
        super().__init__()

    def calibrate(self):
        return super().calibrate()

    def get_quadrant(self):
        return super().get_quadrant()

    def start_tracking(self):
        return super().start_tracking()

    def stop_tracking(self):
        return super().stop_tracking()

    def is_tracking(self):
        return super().is_tracking()